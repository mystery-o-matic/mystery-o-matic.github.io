#!/usr/bin/python3

from sys import argv, exit
from argparse import ArgumentParser
from random import seed, random, shuffle
from datetime import date as Date
from hashlib import sha256
from os.path import isfile
import json

from mystery_o_matic.output.html import produce_html_output
from mystery_o_matic.output.text import produce_text_output
from mystery_o_matic.output.latex import produce_tex_output
from mystery_o_matic.output.llm import produce_llm_output
from mystery_o_matic.echidna import create_outdir
from mystery_o_matic.location import Locations, TutorialLocations, get_location_data
from mystery_o_matic.weapons import get_available_weapons
from mystery_o_matic.mystery import CHARACTER_NAMES, Mystery, get_intervals_length_from_events
from mystery_o_matic.model import Model
from mystery_o_matic.solidity import read_solidity_from_text
from mystery_o_matic.clue_selection import select_clues
from mystery_o_matic.solver import AmbiguousCluesError, order_clues
from mystery_o_matic.seasonal import get_seasonal_theme
from mystery_o_matic.traits import get_trait_pool


MAX_CLUE_ATTEMPTS = 10


def read_story(season, date, language="en"):
    # season 3 onwards keeps one file per language; season 1 used a flat
    # layout with a single (english) file for all languages
    filenames = [
        "story/season-" + str(season) + "/" + language + "/" + date + ".html",
        "story/season-" + str(season) + "/" + date + ".html",
    ]
    for filename in filenames:
        if isfile(filename):
            with open(filename, "r") as f:
                return f.read()
    return ""


def hash256(data):
    hash_obj = sha256(str(data).encode("utf-8"))
    return int(hash_obj.hexdigest(), 16)


def write_clue_analysis(out_dir, mystery, attempts, max_clues):
    """Save the native solver's counts alongside a book export for later rechecks."""
    report = {
        "answer": mystery.get_answer(),
        "generator_seed": mystery.used_seed,
        "selection_attempts": attempts,
        "max_clues": max_clues,
        "analyses": {},
    }
    for label, attribute, key in (
        ("truthful", "additional_clues", "minimumClues"),
        ("lying", "additional_clues_with_lies", "minimumCluesWithLies"),
    ):
        result = mystery.clue_analysis.get(attribute)
        report[key] = result.minimum if result is not None else None
        if result is not None:
            report["analyses"][label] = {
                "status": result.status,
                "minimum_clues": result.minimum,
                "total_clues": result.total,
                "redundant_clues": len(result.redundant),
                "omitted_clues": len(result.omitted),
                "pool_size": result.pool_size,
                "prefix_fraction": result.necessary_ratio,
                "sampled_core_sizes": list(result.trial_sizes),
            }
    with open(out_dir + "/clue-analysis.json", "w", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")


def main() -> int:
    """
    The main function of the mystery-o-matic program.

    Parses command line arguments, generates a mystery scenario, solves it,
    and produces the output based on the specified mode.

    Returns:
        int: The exit code of the program.
    """
    parser = ArgumentParser(description="mystery-o-matic")
    parser.add_argument(
        "scenario", type=str, action="store", help="path to mystery scenario"
    )
    parser.add_argument(
        "static_dir", type=str, action="store", help="path to HTML static files (unused for LaTeX)"
    )
    parser.add_argument(
        "out_dir", type=str, action="store", help="path to output folder"
    )

    parser.add_argument("--seed", type=int, action="store", help="seed for randomness")

    parser.add_argument(
        "--today",
        action="store_const",
        const=True,
        help="generate the mystery for the day",
    )

    parser.add_argument(
        "--date", type=Date.fromisoformat,
        help="mystery date (YYYY-MM-DD); defaults to the saved date or today; also used by --today",
    )

    parser.add_argument(
        "--llm",
        action="store_const",
        const=True,
        help="generate a llms.txt file with the mystery",
    )

    parser.add_argument("--season", action="store", default=1, help="season number")
    parser.add_argument(
        "--difficulty", action="store", default="hard", help="difficulty level"
    )
    parser.add_argument(
        "--nplaces", type=int, action="store", default=4, help="number of rooms"
    )
    parser.add_argument(
        "--nchars", type=int, action="store", default=None, help="number of characters (default: 3)"
    )
    parser.add_argument(
        "--characters", nargs="+", type=str.lower, choices=CHARACTER_NAMES,
        help="fixed cast in CHAR1, CHAR2, ... order; sets --nchars when omitted",
    )
    parser.add_argument(
        "--location", action="store", default=None, help="use a specific location"
    )
    parser.add_argument(
        "--nmoves", type=int, action="store", default=1, help="minimum number of moves"
    )

    parser.add_argument("--mode", action="store", default="html", help="output mode")
    parser.add_argument(
        "--no-appearance-clues", action="store_true",
        help="disable appearance-based sightings (always disabled for LaTeX)",
    )
    parser.add_argument(
        "--clue-shuffles", type=int, default=100,
        help="number of deletion orders sampled when selecting necessary clues (default: 100)",
    )
    parser.add_argument(
        "--min-necessary-ratio", type=float, default=1 / 3,
        help="legacy option accepted for compatibility; all extra clues are always retained",
    )
    parser.add_argument(
        "--max-clues", type=int, default=None,
        help="reject a clue pool above this size without discarding clues (default: no limit)",
    )

    parser.add_argument(
        "--telegram-api-key",
        type=str,
        action="store",
        default=None,
        help="telegram api key to start a bot",
    )

    parser.add_argument(
        "--workers", type=int, action="store", default=6, help="number of workers"
    )

    parser.add_argument(
        "--max-time-slots",
        type=int,
        action="store",
        default=10,
        help="max number of time slots",
    )

    parser.add_argument(
        "--save-state",
        type=str,
        action="store",
        default=None,
        help="path to JSON file where to save a precomputed state for fast reloading",
    )

    parser.add_argument(
        "--load-state",
        type=str,
        action="store",
        default=None,
        help="path to JSON file with a previously saved state (skips solving and reuses it)",
    )

    args = parser.parse_args()

    if args.clue_shuffles < 1:
        parser.error("--clue-shuffles must be positive")
    if not 0 < args.min_necessary_ratio <= 1:
        parser.error("--min-necessary-ratio must be greater than 0 and at most 1")

    if args.characters:
        if len(set(args.characters)) != len(args.characters):
            parser.error("--characters must contain distinct names")
        if len(args.characters) < 3:
            parser.error("--characters requires at least three names")
        if args.nchars is not None and args.nchars != len(args.characters):
            parser.error("--nchars must match the number of --characters")

    if args.save_state is not None and args.load_state is not None:
        print("Cannot use both --save-state and --load-state at the same time")
        return -1

    state = {}
    if args.load_state:
        with open(args.load_state, "r", encoding="utf-8") as f:
            state = json.load(f)
    try:
        mystery_date = args.date or (
            Date.fromisoformat(state["mystery_date"])
            if state.get("mystery_date") else Date.today()
        )
    except (TypeError, ValueError):
        parser.error("saved mystery_date must be a valid date in YYYY-MM-DD format")
    max_clues = args.max_clues if args.max_clues is not None else state.get("max_clues")
    if max_clues is not None and (type(max_clues) is not int or max_clues < 1):
        parser.error("--max-clues must be a positive integer")

    # Saved cases can carry declarative clue and print choices. LaTeX embeds
    # its map, so separate map images are optional.
    latex_options = dict(state.get("latex", {})) if args.mode == "latex" else {}
    latex_languages = latex_options.pop("languages", ["en", "es"])
    render_maps = latex_options.pop("render_maps", args.mode != "latex")
    clue_selection = latex_options.pop("clue_selection", None)
    lying_selection = latex_options.pop("clue_selection_with_lies", None)
    clue_seed = latex_options.pop("clue_seed", state.get("seed"))
    if not latex_languages or any(language not in ("en", "es") for language in latex_languages):
        parser.error("LaTeX languages must be en and/or es")
    if lying_selection is not None and clue_selection is None:
        parser.error("clue_selection_with_lies also requires clue_selection for the truthful variant")
    if clue_selection is not None:
        latex_options.setdefault("shuffle_clues", False)
        latex_options.setdefault("write_lies", lying_selection is not None)
        if latex_options["write_lies"] and lying_selection is None:
            parser.error("selected truthful clues need clue_selection_with_lies to export a lying variant")
        if lying_selection is not None and not latex_options["write_lies"]:
            parser.error("clue_selection_with_lies requires write_lies")

    print("Welcome to mystery-o-matic!")
    solidity_file = args.scenario
    static_dir = args.static_dir
    out_dir = args.out_dir
    used_seed = args.seed
    workers = args.workers
    season = args.season
    number_places = state.get("number_places", args.nplaces)
    characters = args.characters
    number_characters = len(characters) if characters else (args.nchars or 3)
    date = mystery_date.strftime("%d-%m-%Y")
    mode = args.mode
    llm_output = args.llm
    difficulty = args.difficulty
    max_time_slots = args.max_time_slots
    telegram_api_key = args.telegram_api_key

    if args.nmoves < 1:
        print("Invalid number of moves")
        return -1

    nmoves = args.nmoves

    # Check if the mode is valid
    if mode not in ["html", "text", "latex"]:
        print("Invalid mode", mode)
        print("Only html and text is accepted")
        return -1

    # Profiles and their identifying clues belong to the website/LLM exports.
    # Resolve the pool before generation, including when reloading a saved date.
    trait_theme = get_seasonal_theme(mystery_date) if mode == "html" or llm_output else ""
    cast_size = len(state["initial_locations_pairs"]) if args.load_state else number_characters
    try:
        get_trait_pool(trait_theme, cast_size)
    except ValueError as error:
        parser.error(str(error))

    if args.today:
        print(f"Generating mystery for {date} (season {season})")
        assert used_seed is None
        used_seed = abs(hash256(str(date)))

    if used_seed is None:
        used_seed = state.get("seed")

    if used_seed is not None:
        seed(used_seed)
    else:
        used_seed = abs(hash256(random()))

    create_outdir(out_dir)
    location_name, location_data = get_location_data(
        args.location or state.get("location_name"), args.mode
    )
    print("Location selected is:", location_name)
    weapons_available, weapon_labels = get_available_weapons(
        number_places, location_name
    )

    _, tutorial_location_data = get_location_data("mansion", args.mode)
    tutorial_locations = TutorialLocations(tutorial_location_data)
    # Unused for now
    # tutorial_locations.render_locations(out_dir + "/tutorial")

    # Only export cases whose remaining clues uniquely solve every requested
    # variant. Removing hearing clues can leave a candidate ambiguous, so
    # fresh generation tries another seed. Explicit saved cases must not be
    # silently replaced, and repeated ambiguity must eventually fail CI.
    for clue_attempt in range(1, MAX_CLUE_ATTEMPTS + 1):
        weapon_used = None
        if args.load_state:
            print("Loaded precomputed state from:", args.load_state)

            # Use location from state if not explicitly specified
            if "location_name" in state:
                if args.location is not None and state["location_name"] != location_name:
                    print(
                        "Warning: loaded state location_name differs from requested location:",
                        state["location_name"],
                    )
                location_name = state["location_name"]
                location_name, location_data = get_location_data(location_name, args.mode)
                number_places = state.get("number_places", number_places)

            # Use weapons from state if available, to match the saved mystery
            if "weapons_available" in state:
                weapons_available = state["weapons_available"]
            if "weapon_labels" in state:
                weapon_labels = state["weapon_labels"]

            solidity_file = args.scenario
            locations = Locations(
                mode, location_name, number_places, location_data, weapons_available.keys()
            )
            if "location_indices" in state:
                locations.restore_layout(state["location_indices"], state["location_edges"])
            # override weapon locations / activities if provided in the saved state
            if "weapon_locations" in state:
                locations.weapon_locations = state["weapon_locations"]
            activities = state.get("activities", locations.get_activities())
            stay_activities = locations.get_stay_activities()

            initial_locations_pairs = [tuple(x) for x in state["initial_locations_pairs"]]
            if (args.nchars is not None or args.characters) and number_characters != len(initial_locations_pairs):
                parser.error("requested cast size does not match the loaded state")
            number_characters = len(initial_locations_pairs)
            if characters is None:
                characters = state.get("characters")
            used_weapon_location = state.get("used_weapon_location")
            weapon_used = state.get("weapon_used")
            txs = state["txs"]
            events = state.get("events", [])

            model = Model("StoryModel", locations, nmoves, out_dir, solidity_file)
            model.generate_enums(number_characters)
            # reconstruct parsed source object from saved source_text if available
            if "source_text" in state and state.get("source_text") is not None:
                model.source = read_solidity_from_text(state.get("source_text"))
            else:
                model.source = state.get("source", model.source)

            time_slots = get_intervals_length_from_events(model.source, "StoryModel", events)
            if time_slots > max_time_slots:
                print("Loaded solution is too large:", int(time_slots))
                return -1

        else:
            while True:
                solidity_file = args.scenario
                locations = Locations(
                    mode, location_name, number_places, location_data, weapons_available.keys()
                )
                print("Sorted locations:", locations.sort_locations())

                weapon_locations = locations.weapon_locations
                activities = locations.get_activities()
                stay_activities = locations.get_stay_activities()

                model = Model("StoryModel", locations, nmoves, out_dir, solidity_file)
                model.generate_enums(number_characters)
                (initial_locations_pairs, used_weapon_location) = model.generate_conditions()
                solidity_file = model.generate_solidity()

                print("Running the simulation..")
                result = model.solve(used_seed, workers)

                if result is None:
                    print("No result at all!, restarting..")
                    used_seed += 1
                    seed(used_seed)
                    continue

                txs = result["tests"][0]["transactions"]
                events = []
                if "events" in result["tests"][0]:
                    events = result["tests"][0]["events"]

                time_slots = get_intervals_length_from_events(
                    model.source, "StoryModel", events
                )

                if time_slots <= max_time_slots:
                    break

                print("Solution is too large:", int(time_slots))
                used_seed += 1
                seed(used_seed)

        weapon_locations = locations.weapon_locations

        # Determine the weapon for this candidate, never a rejected attempt.
        if weapon_used is None:
            if used_weapon_location is not None:
                weapon_used = weapon_locations[used_weapon_location]
            else:
                weapon_used = list(weapon_locations.values())[0]

        mystery = Mystery(
            difficulty,
            initial_locations_pairs,
            weapon_locations,
            weapon_used,
            activities,
            model.source,
            txs,
            stay_activities=stay_activities,
            used_seed=used_seed,
            characters=characters,
            appearance_clues=(mode != "latex" and not args.no_appearance_clues),
            trait_theme=trait_theme,
        )
        if args.load_state and "initial_time" in state:
            from mystery_o_matic.time import Time
            mystery.initial_time = Time(state["initial_time"])
        mystery.load_events(events)
        try:
            selected_clues = (
                select_clues(mystery, clue_selection) if clue_selection is not None else None
            )
            selected_lies = (
                select_clues(mystery, lying_selection, with_lies=True)
                if lying_selection is not None else None
            )
        except (ValueError, KeyError, TypeError) as error:
            parser.error(f"Invalid saved clue selection: {error}")
        mystery.process_clues()
        if selected_clues is not None:
            # Render wording with its own recorded seed, independent of random
            # pruning/alibi construction in process_clues.
            seed(clue_seed if clue_seed is not None else used_seed)
            mystery.clue_objects = selected_clues
            mystery.additional_clues = [clue.string() for clue in selected_clues]
        if selected_lies is not None:
            seed(clue_seed if clue_seed is not None else used_seed)
            mystery.clue_objects_with_lies = selected_lies
            mystery.additional_clues_with_lies = [clue.string() for clue in selected_lies]

        try:
            order_clues(
                mystery,
                locations.graph,
                include_lies=(mode == "html" or llm_output or
                              (mode == "latex" and latex_options.get("write_lies", True))),
                killer_leaves=(mode != "latex"),
                attempts=args.clue_shuffles,
                min_ratio=args.min_necessary_ratio,
                max_clues=max_clues,
            )
        except AmbiguousCluesError as error:
            if args.load_state:
                parser.error(f"Saved case is not uniquely solvable: {error}")
            if clue_attempt == MAX_CLUE_ATTEMPTS:
                parser.error(
                    f"No uniquely solvable mystery after {MAX_CLUE_ATTEMPTS} candidates: {error}"
                )
            print(f"Clues allow another answer; generating another mystery ({clue_attempt}/{MAX_CLUE_ATTEMPTS})")
            used_seed += 1
            seed(used_seed)
            continue
        except ValueError as error:
            parser.error(str(error))
        break

    story_clue = read_story(season, date)
    story_clues = dict(
        (language, read_story(season, date, language))
        for language in ["en", "es", "ru"]
    )

    # Save only a case that passed the clue checks in every requested variant.
    if args.save_state:
        # read solidity file text if available so we don't try to serialize parser objects
        source_text = None
        try:
            with open(solidity_file, "r") as _f:
                source_text = _f.read()
        except Exception:
            source_text = None

        state = {
            "initial_locations_pairs": initial_locations_pairs,
            "used_weapon_location": used_weapon_location,
            "weapon_used": weapon_used,
            "weapon_locations": weapon_locations,
            "activities": activities,
            "source_text": source_text,
            "txs": txs,
            "events": events,
            "weapons_available": weapons_available,
            "weapon_labels": weapon_labels,
            "seed": used_seed,
            "mystery_date": mystery_date.isoformat(),
            "location_name": location_name,
            "number_places": number_places,
            "max_clues": max_clues,
            "location_indices": locations.indices,
            "location_edges": list(locations.graph.edges()),
            "characters": mystery.get_characters(),
            "initial_time": str(mystery.initial_time),
            "number_characters": number_characters,
        }
        with open(args.save_state, "w") as f:
            json.dump(state, f, indent=2)
        print("Saved precomputed state to:", args.save_state)

    if llm_output:
        produce_llm_output(
            static_dir,
            out_dir,
            "en",
            mystery,
            weapons_available,
            weapon_labels,
            locations,
            mystery_date=mystery_date,
        )

    if mode == "html":
        produce_html_output(
            static_dir,
            out_dir,
            ["en", "es", "ru"],
            mystery,
            weapons_available,
            weapon_labels,
            locations,
            story_clues,
            mystery_date=mystery_date,
        )
    elif mode == "latex":
        produce_tex_output(
            out_dir,
            latex_languages,
            mystery,
            weapons_available,
            weapon_labels,
            locations,
            **latex_options,
        )
        write_clue_analysis(out_dir, mystery, args.clue_shuffles, max_clues)
    elif mode == "text":
        produce_text_output(
            static_dir,
            out_dir,
            mystery,
            locations,
            story_clue,
            telegram_api_key,
        )
    else:
        print("Invalid mode")
        return -1
    # The book (latex) is only generated for en/es, so skip ru location renders.
    location_languages = latex_languages if mode == "latex" else None
    if render_maps:
        locations.render_locations(out_dir, location_languages)

    print("Characters:")
    for i, char in enumerate(mystery.get_characters()):
        print("  * {} is {}".format("CHAR" + str(i + 1), char.lower()))

    print("Locations:")
    for room, name in locations.indices.items():
        print("  * {} is {}".format(room, name))

    print("Solution:", mystery.get_answer())
    print(" Initial locations:")
    for c, p in mystery.initial_locations:
        print("  * {} was in the {}".format(c, p))

    for action in mystery.solution:
        print(action)
    return 0


if __name__ == "__main__":
    exit(main())

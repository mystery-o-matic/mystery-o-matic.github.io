#!/usr/bin/python3

from sys import argv, exit
from argparse import ArgumentParser
from random import seed, random, shuffle
from datetime import datetime
from hashlib import sha256
from os.path import isfile

from mystery_o_matic.output.html import produce_html_output
from mystery_o_matic.output.text import produce_text_output
from mystery_o_matic.echidna import create_outdir
from mystery_o_matic.location import Locations, get_location_data
from mystery_o_matic.weapons import get_available_weapons
from mystery_o_matic.mystery import Mystery, get_intervals_length_from_events
from mystery_o_matic.model import Model


def read_story(season, date):
    filename = "story/season-" + str(season) + "/" + date + ".html"
    if not isfile(filename):
        return ""

    with open(filename, "r") as f:
        return f.read()

def hash256(data):
    hash_obj = sha256(str(data).encode("utf-8"))
    return int(hash_obj.hexdigest(), 16)

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
        "static_dir", type=str, action="store", help="path to folder with static files)"
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

    parser.add_argument("--season", action="store", default=1, help="season number")
    parser.add_argument("--nplaces", type=int, action="store", default=4, help="number of rooms")
    parser.add_argument("--nchars", type=int, action="store", default=3, help="number of characters")
    parser.add_argument("--location", action="store", default=None, help="use a specific location")
    parser.add_argument("--mode", action="store", default="html", help="output mode")

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
        default=8,
        help="max number of time slots",
    )

    args = parser.parse_args()

    print("Welcome to mystery-o-matic!")
    solidity_file = args.scenario
    static_dir = args.static_dir
    out_dir = args.out_dir
    used_seed = args.seed
    workers = args.workers
    season = args.season
    number_places = args.nplaces
    number_characters = args.nchars
    date = datetime.today().strftime("%d-%m-%Y")
    mode = args.mode
    max_time_slots = args.max_time_slots
    telegram_api_key = args.telegram_api_key

    # Check if the mode is valid
    if mode not in ["html", "text"]:
        print("Invalid mode", mode)
        print("Only html and text is accepted")
        return -1

    if args.today:
        print(f"Generating mystery for {date} (season {season})")
        assert used_seed is None
        used_seed = abs(hash256(str(date)))

    if used_seed is not None:
        seed(used_seed)
    else:
        used_seed = abs(hash256(random()))

    create_outdir(out_dir)
    location_name, location_data = get_location_data(args.location)
    print("Location selected is:", location_name)
    weapons_available = get_available_weapons(number_places, location_name)

    while True:
        solidity_file = args.scenario
        locations = Locations(location_name, number_places, location_data, weapons_available.keys())
        weapon_locations = locations.weapon_locations
        activities = locations.get_activities()

        model = Model("StoryModel", locations, out_dir, solidity_file)
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

    story_clue = read_story(season, date)

    weapon_used = locations.weapon_locations[used_weapon_location]
    mystery = Mystery(
        initial_locations_pairs, weapon_locations, weapon_used, activities, model.source, txs
    )
    mystery.load_events(events)
    mystery.process_clues()

    if mode == "html":
        produce_html_output(
            static_dir, out_dir, mystery, weapons_available, locations, story_clue
        )
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
    locations.render_locations(out_dir)

    print("Characters:")
    for i, char in enumerate(mystery.get_characters()):
        print("  * {} is {}".format("CHAR" + str(i + 1), char.lower()))

    print("Locations:")
    for room, name in locations.names.items():
        print("  * {} is {}".format(room, name))

    print("Solution:")
    print(" Initial locations:")
    for c, p in mystery.initial_locations:
        print("  * {} was in the {}".format(c, p))

    for action in mystery.solution:
        print(action)
    return 0


if __name__ == "__main__":
    exit(main())

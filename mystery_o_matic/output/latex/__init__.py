import re
from random import shuffle

from mystery_o_matic.output import create_template
from mystery_o_matic.output.latex.book import render_book_case
from mystery_o_matic.output.latex.utils import (
    generate_latex_clue_table,
    generate_latex_weapons_table,
    get_bullet_list,
    create_tex_template,
    save_tex,
    get_char_name,
    get_emoji_name,
    replace_emojis,
    replace_opening_quotes,
    save_solution,
)
from mystery_o_matic.traits import COARSE_PHRASES

# The book has no easy way to render the trait/descriptor/hat hints yet, so for
# LaTeX foggy sightings fall back to a plain "somebody".
_FOG_SOMEBODY_WORD = {"en": "somebody", "es": "alguien", "ru": "кого-то"}


def _strip_fog_enrichment(text, language):
    word = _FOG_SOMEBODY_WORD[language]
    # "someone wearing X" / "alguien con X" / "кого-то в X" -> plain somebody
    text = re.sub(r"(someone|alguien|кого-то) \$TELL_CHAR\d+", word, text)
    # any remaining trait/descriptor tokens -> somebody
    text = re.sub(r"\$(TELL|DESC)_CHAR\d+", word, text)
    # coarse property phrases (hat/glasses) are baked-in text (no token) -> somebody
    for phrases in COARSE_PHRASES.values():
        text = text.replace(phrases[language], word)
    return text


def _shuffle_clues(mystery):
    for attribute, objects_attribute in (
        ("additional_clues", "clue_objects"),
        ("additional_clues_with_lies", "clue_objects_with_lies"),
    ):
        clues = getattr(mystery, attribute)
        analysis = getattr(mystery, "clue_analysis", {}).get(attribute)
        boundary = analysis.minimum if analysis is not None else None
        order = list(range(len(clues)))
        if boundary is None:
            shuffle(order)
        else:
            # Never shuffle redundant clues ahead of the sufficient prefix.
            required, redundant = order[:boundary], order[boundary:]
            shuffle(required)
            shuffle(redundant)
            order = required + redundant
        clues[:] = [clues[i] for i in order]
        objects = getattr(mystery, objects_attribute, None)
        if objects is not None:
            objects[:] = [objects[i] for i in order]


def produce_tex_output(
    out_dir,
    languages,
    mystery,
    weapons,
    weapon_labels,
    locations,
    shuffle_clues=True,
    clue_marker="\\cluemark",
    weapon_column_width=None,
    write_lies=True,
    room_labels=None,
):
    intervals = mystery.get_intervals()
    suspects = mystery.get_suspects()
    room_labels = room_labels or {}

    if shuffle_clues:
        _shuffle_clues(mystery)

    names_html = {}
    for i, char in enumerate(mystery.get_characters()):
        names_html["CHAR" + str(i + 1)] = get_char_name(char)

    names_html["SUS0"] = suspects[0].capitalize()
    names_html["SUS1"] = suspects[1].capitalize()

    save_solution(out_dir, mystery.get_answer())
    for language in languages:

        if language == "en":
            names_html["NOBODY"] = "nobody"

            for weapon_type in ["STABBING", "STRANGULATION", "CONTUSION", "PROJECTILE"]:
                names_html[weapon_type] = weapon_type.lower()

        elif language == "es":
            names_html["NOBODY"] = "nadie"

            weapon_type_labels_es = {
                "STABBING": "apuñalamiento",
                "STRANGULATION": "estrangulamiento",
                "CONTUSION": "contusión",
                "PROJECTILE": "proyectil",
            }
            for weapon_type in ["STABBING", "STRANGULATION", "CONTUSION", "PROJECTILE"]:
                names_html[weapon_type] = weapon_type_labels_es[weapon_type]
        else:
            raise ValueError("Unknown language: " + language)

        for room, name in locations.names[language].items():
            if room not in locations.rindices:
                continue  # skip any missing place
            index = locations.rindices[room]
            name = room_labels.get(language, {}).get(index, name)
            names_html[index] = (
                name + " (" + get_emoji_name(locations.representations[index]) + ")"
            )
        for weapon, label in weapon_labels[language].items():
            if weapon not in weapons:
                continue
            if language == "es":
                label = label.capitalize()
            names_html[weapon.replace("$", "")] = (
                label + " (" + get_emoji_name(weapons[weapon]) + ")"
            )

        # Trait/descriptor tokens are NOT registered here: foggy sightings are
        # stripped back to "somebody" for LaTeX (see _strip_fog_enrichment).

        firstClue = mystery.initial_clues[0]
        firstClue = create_template(firstClue[language]).substitute(names_html)

        sub_bullets = []
        for clue in mystery.final_locations_clues:
            clue = create_template(clue[language]).substitute(names_html)
            sub_bullets.append(clue)

        additional_clues = []

        for clue in mystery.additional_clues:
            if language not in clue:
                continue
            text = _strip_fog_enrichment(clue[language], language)
            clue = replace_emojis(create_template(text).substitute(names_html))
            clue = replace_opening_quotes(clue)
            additional_clues.append(clue)

        additional_clues_enumeration = get_bullet_list(
            additional_clues, customItem=clue_marker
        )

        additional_clues_with_lies = []
        for clue in mystery.additional_clues_with_lies:
            if language not in clue:
                continue
            text = _strip_fog_enrichment(clue[language], language)
            clue = replace_emojis(create_template(text).substitute(names_html))
            clue = replace_opening_quotes(clue)
            additional_clues_with_lies.append(clue)

        additional_clues_with_lies_enumeration = get_bullet_list(
            additional_clues_with_lies, customItem=clue_marker
        )

        args = {}
        args["firstClue"] = firstClue
        args["additionalClues"] = additional_clues_enumeration
        args["finalLocationsList"] = get_bullet_list(sub_bullets, "")
        args["finalTime"] = str(mystery.final_time)
        tables = ""

        for i in range(len(locations.weapon_locations.items())):
            tables += (
                generate_latex_clue_table(
                    f"ROOM{i}REP",
                    len(intervals),
                    mystery.get_characters(),
                    mystery.final_locations,
                    mystery.victim,
                    i == 0,
                )
                + "\n"
            )

        args["cluesTables"] = tables
        args["weaponsTable"] = generate_latex_weapons_table(
            len(locations.weapon_locations), column_width=weapon_column_width
        )

        for i in range(len(mystery.get_characters())):
            args[f"CHAR{i+1}"] = names_html[f"CHAR{i+1}"]

        for room in locations.names[language]:
            if room not in locations.rindices:
                continue  # skip any missing place
            index = locations.rindices[room]
            args[index + "REP"] = get_emoji_name(locations.representations[index])

        for l, w in locations.weapon_locations.items():
            args[l + "WEAPONREP"] = (
                get_emoji_name(weapons[w])
                + " "
                + get_emoji_name(locations.representations[l])
            )

        for i, time in enumerate(intervals):
            args[f"TIME{i}"] = time

        # Resolve worksheet cells before inserting them into the shared layout.
        # Neither the layout nor the map reads a per-case template or image.
        for field in ("cluesTables", "weaponsTable"):
            args[field] = create_tex_template(args[field]).substitute(args)

        variants = [("mystery.tex", additional_clues_enumeration)]
        if write_lies:
            variants.append(("mystery.lies.tex", additional_clues_with_lies_enumeration))
        for filename, clues in variants:
            args["additionalClues"] = clues
            tex_source = render_book_case(language, args, locations)
            save_tex(out_dir, language, tex_source, filename)

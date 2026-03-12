from mystery_o_matic.output import create_template
from mystery_o_matic.output.html.utils import (
    read_html_template,
    build_website,
    get_bullet_list,
    get_options_selector,
    get_char_name,
    get_clue_table,
    get_weapon_type_name,
    save_json,
)
from mystery_o_matic.clues import NoOneElseStatement


def produce_html_output(
    static_dir,
    out_dir,
    languages,
    mystery,
    weapons,
    weapon_labels,
    locations,
    story_clue,
):
    intervals = mystery.get_intervals()
    suspects = mystery.get_suspects()
    select_suspects = get_options_selector(zip(suspects, suspects))
    select_intervals = get_options_selector(zip(intervals, intervals))

    names_html = {}
    for i, char in enumerate(mystery.get_characters()):
        names_html["CHAR" + str(i + 1)] = get_char_name(char)

    names_html["SUS0"] = suspects[0].capitalize()
    names_html["SUS1"] = suspects[1].capitalize()

    names_txt = {}
    for i, char in enumerate(mystery.get_characters()):
        names_txt["CHAR" + str(i + 1)] = char.lower()

    for room, name in locations.indices.items():
        names_txt[room] = locations.names["en"][name]

    final_locations_map = {}
    for c, p in mystery.final_locations.items():
        c = create_template(c).substitute(names_txt)
        p = create_template(p).substitute(names_txt)
        final_locations_map[c] = p

    representations_map = {}
    for l, r in locations.representations.items():
        l = create_template("$" + l).substitute(names_txt)
        representations_map[l] = r

    # the weapons map will be computed reversing the location_weapons one
    weapons_map = {}
    for l, w in locations.weapon_locations.items():
        l = create_template("$" + l).substitute(names_txt)
        weapons_map[w] = l

    correct_answer = mystery.get_answer_hash()

    clues_tables = ""
    sorted_locations = locations.sort_locations()
    clues_tables += get_clue_table(sorted_locations[0], 115, 500) + "\n"

    for loc in locations.sort_locations()[1:]:
        clues_tables += get_clue_table(loc, 95, 500) + "\n"

    location_order = []
    for loc in sorted_locations:
        location_order.append((loc, create_template("$" + loc.upper()).substitute(names_txt)))

    json = {}
    json["locationOrder"] = location_order
    json["additionalClues"] = {}
    json["additionalCluesWithLies"] = {}
    json["numIntervals"] = len(intervals)
    json["characterNames"] = mystery.get_characters()
    json["victim"] = create_template(mystery.victim).substitute(names_txt)
    json["locationMap"] = final_locations_map
    json["locationIcons"] = representations_map
    json["weaponMap"] = weapons_map
    json["weaponIcons"] = weapons
    json["timeOffset"] = mystery.initial_time.seconds
    json["correctAnswer"] = correct_answer

    for language in languages:

        if language == "en":
            names_html["NOBODY"] = "nobody"
            names_txt["NOBODY"] = "nobody"

            for weapon_type in ["STABBING", "STRANGULATION", "CONTUSION", "PROJECTILE"]:
                names_html[weapon_type] = get_weapon_type_name(weapon_type)
                names_txt[weapon_type] = weapon_type.lower()

        elif language == "es":
            names_html["NOBODY"] = "nadie"
            names_txt["NOBODY"] = "nadie"

            weapon_type_labels_es = {
                "STABBING": "apuñalamiento",
                "STRANGULATION": "estrangulamiento",
                "CONTUSION": "contusión",
                "PROJECTILE": "proyectil",
            }
            for weapon_type in ["STABBING", "STRANGULATION", "CONTUSION", "PROJECTILE"]:
                label = weapon_type_labels_es[weapon_type]
                names_html[weapon_type] = get_weapon_type_name(weapon_type, label)
                names_txt[weapon_type] = label

        elif language == "ru":
            names_html["NOBODY"] = "никого"
            names_txt["NOBODY"] = "никого"

            weapon_type_labels_ru = {
                "STABBING": "колото-резаного ранения",
                "STRANGULATION": "удушения",
                "CONTUSION": "ушиба",
                "PROJECTILE": "огнестрельного ранения",
            }
            for weapon_type in ["STABBING", "STRANGULATION", "CONTUSION", "PROJECTILE"]:
                label = weapon_type_labels_ru[weapon_type]
                names_html[weapon_type] = get_weapon_type_name(weapon_type, label)
                names_txt[weapon_type] = label
        else:
            raise ValueError("Unknown language: " + language)

        characters = list(map(lambda char: char.capitalize(), mystery.get_characters()))
        if language == "es":
            conjunction = " y "
        elif language == "ru":
            conjunction = " и "
        else:
            conjunction = " and "
        introLocation = ", ".join(characters[:-1]) + conjunction + characters[-1]
        introLocation += locations.intro[language]

        for room, name in locations.names[language].items():
            if room not in locations.rindices:
                continue  # skip any missing place
            index = locations.rindices[room]
            names_html[index] = name + " (" + locations.representations[index] + ")"

        if language == "ru":
            for room, name in locations.names["ru_loc"].items():
                if room not in locations.rindices:
                    continue
                index = locations.rindices[room]
                names_html[index + "_LOC"] = name + " (" + locations.representations[index] + ")"
            for room, name in locations.names["ru_gen"].items():
                if room not in locations.rindices:
                    continue
                index = locations.rindices[room]
                names_html[index + "_GEN"] = name + " (" + locations.representations[index] + ")"

        for weapon, label in weapon_labels[language].items():
            if weapon not in weapons:
                continue
            if language == "es":
                label = label.capitalize()
            names_html[weapon.replace("$", "")] = label + " (" + weapons[weapon] + ")"

        # print(names_html)
        bullets = []
        for i, clue in enumerate(mystery.initial_clues):
            bullets.append(clue[language])

        sub_bullets = []
        for clue in mystery.weapon_locations_clues:
            sub_bullets.append(clue[language])

        weapon_locations_bullets = mystery.weapon_locations_intro[language]
        weapon_locations_bullets += get_bullet_list(sub_bullets, language)
        bullets.append(weapon_locations_bullets)
        bullets.append(mystery.weapon_locations_outro[language])

        sub_bullets = []
        for clue in mystery.final_locations_clues:
            sub_bullets.append(clue[language])

        final_locations_bullets = mystery.final_locations_intro[language]
        final_locations_bullets += get_bullet_list(sub_bullets)
        bullets.append(final_locations_bullets)
        bullets.append(NoOneElseStatement().string()[language])

        initial_clues = get_bullet_list(bullets)

        additional_clues = []

        for i, clue in enumerate(mystery.additional_clues):
            additional_clues.append(
                create_template(clue[language]).substitute(names_html)
            )

        additional_clues_with_lies = []

        for i, clue in enumerate(mystery.additional_clues_with_lies):
            additional_clues_with_lies.append(
                create_template(clue[language]).substitute(names_html)
            )

        # populate the weapon options
        weapons_options = []
        for w in locations.weapon_locations.values():
            # use the labels in the current language but the values in english
            weapons_options.append((weapon_labels[language][w], weapon_labels["en"][w]))

        select_weapons = get_options_selector(weapons_options)

        args = {}
        args["cluesTables"] = clues_tables
        args["introLocation"] = introLocation
        args["initialClues"] = initial_clues
        args["selectIntervals"] = select_intervals
        args["selectSuspects"] = select_suspects
        args["selectWeapon"] = select_weapons
        args["storyClue"] = story_clue

        html_template = read_html_template(
            static_dir + f"/{language}/index.template.html"
        )
        html_source = html_template.substitute(args)
        html_source = create_template(html_source).substitute(names_html)
        build_website(out_dir, static_dir, language, html_source)

        json["additionalClues"][language] = additional_clues
        json["additionalCluesWithLies"][language] = additional_clues_with_lies

    save_json(out_dir, f"data = ", json)

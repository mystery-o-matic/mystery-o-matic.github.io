from random import shuffle

from mystery_o_matic.output import create_template
from mystery_o_matic.output.latex.utils import generate_latex_clue_table, generate_latex_weapons_table, get_bullet_list, get_enumeration_list, read_tex_template, create_tex_template, save_tex, get_char_name, get_emoji_name, replace_emojis, replace_opening_quotes, save_solution
from mystery_o_matic.clues import NoOneElseStatement

def produce_tex_output(static_dir, out_dir, languages, mystery, weapons, weapon_labels, locations, story_clue):
    intervals = mystery.get_intervals()
    suspects = mystery.get_suspects()

    shuffle(mystery.additional_clues)
    shuffle(mystery.additional_clues_with_lies)

    names_html = {}
    for i, char in enumerate(mystery.get_characters()):
        names_html["CHAR" + str(i + 1)] = get_char_name(char)

    names_html["SUS0"] = suspects[0].capitalize()
    names_html["SUS1"] = suspects[1].capitalize()

    names_txt = {}
    for i, char in enumerate(mystery.get_characters()):
        names_txt["CHAR" + str(i + 1)] = char.lower()

    for room, name in locations.indices.items():
        names_txt[room] = locations.names['en'][name]

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

    save_solution(out_dir, mystery.get_answer())
    for language in languages:

        if language == "en":
            names_html["NOBODY"] = "nobody"
            names_txt["NOBODY"] = "nobody"
        elif language == "es":
            names_html["NOBODY"] = "nadie"
            names_txt["NOBODY"] = "nadie"
        else:
            raise ValueError("Unknown language: " + language)

        characters = list(map(lambda char: char.capitalize(), mystery.get_characters()))
        introLocation = ", ".join(characters[:-1]) + " and " + characters[-1]
        introLocation += " !TODO" #locations.intro[language]

        for room, name in locations.names[language].items():
            if room not in locations.rindices:
                continue # skip any missing place
            index = locations.rindices[room]
            names_html[index] = name + " (" + get_emoji_name(locations.representations[index]) + ")"
        for weapon, label in weapon_labels[language].items():
            if weapon not in weapons:
                continue
            if language == "es":
                label = label.capitalize()
            names_html[weapon.replace("$", "")] = label + " (" + get_emoji_name(weapons[weapon]) + ")"

        #print(names_html)
        firstClue = mystery.initial_clues[0]
        firstClue = create_template(firstClue[language]).substitute(names_html)

        #bullets = []
        #for i, clue in enumerate(mystery.initial_clues[:1]):
        #    clue = create_template(clue[language]).substitute(names_html)
        #    bullets.append(clue)

        #sub_bullets = []
        #for clue in mystery.weapon_locations_clues:
        #    clue = create_template(clue[language]).substitute(names_html)
        #    sub_bullets.append(clue)

        #weapon_locations_bullets = mystery.weapon_locations_intro[language]
        #weapon_locations_bullets += get_bullet_list(sub_bullets)
        #bullets.append(weapon_locations_bullets)
        #bullets.append(mystery.weapon_locations_outro[language])

        sub_bullets = []
        for clue in mystery.final_locations_clues:
            clue = create_template(clue[language]).substitute(names_html)
            sub_bullets.append(clue)

        final_locations_bullets = mystery.final_locations_intro[language]
        final_locations_bullets += get_bullet_list(sub_bullets, "")
        #bullets.append(final_locations_bullets)
        #bullets.append(NoOneElseStatement().string()[language])

        #initial_clues = get_bullet_list(bullets)

        additional_clues = []

        for clue in mystery.additional_clues:
            clue = replace_emojis(create_template(clue[language]).substitute(names_html))
            clue = replace_opening_quotes(clue)
            additional_clues.append(clue)

        additional_clues_enumeration = get_bullet_list(additional_clues, customItem="\\ding{43}")

        additional_clues_with_lies = []
        for clue in mystery.additional_clues_with_lies:
            clue = replace_emojis(create_template(clue[language]).substitute(names_html))
            clue = replace_opening_quotes(clue)
            additional_clues_with_lies.append(clue)

        additional_clues_with_lies_enumeration = get_bullet_list(additional_clues_with_lies, customItem="\\ding{43}")

        # populate the weapon options
        weapons_options = []
        for w in locations.weapon_locations.values():
            # use the labels in the current language but the values in english
            weapons_options.append((weapon_labels[language][w], weapon_labels["en"][w]))

        #select_weapons = get_options_selector(weapons_options)

        args = {}
        args["introLocation"] = introLocation
        args["firstClue"] = firstClue
        args["additionalClues"] = additional_clues_enumeration
        args["finalLocations"] = get_bullet_list([final_locations_bullets], "")
        args["locationImages"] = out_dir + f"/{language}"
        tables = ""

        for i in range(len(locations.weapon_locations.items())):
            tables += generate_latex_clue_table(f"ROOM{i}REP", len(intervals), len(mystery.get_characters()), mystery.final_locations, mystery.victim, i == 0) + "\n"

        args["cluesTables"] = tables
        args["weaponsTable"] = generate_latex_weapons_table(len(weapons_options))

        for i in range(len(mystery.get_characters())):
            args[f"CHAR{i+1}"] = names_html[f"CHAR{i+1}"]

        for room in locations.names[language]:
            if room not in locations.rindices:
                continue # skip any missing place
            index = locations.rindices[room]
            args[index + "REP"] = get_emoji_name(locations.representations[index])

        for l, w in locations.weapon_locations.items():
            args[l + "WEAPONREP"] = get_emoji_name(locations.representations[l]) + " " + get_emoji_name(weapons[w])

        for (i, time) in enumerate(intervals):
            args[f"TIME{i}"] = time

        tex_template = read_tex_template(static_dir + f"/{language}/mystery.template.tex")

        tex_source = tex_template.substitute(args)
        tex_source = create_tex_template(tex_source).substitute(args)
        save_tex(out_dir, language, tex_source, "mystery.tex")

        args["additionalClues"] = additional_clues_with_lies_enumeration

        tex_source = tex_template.substitute(args)
        tex_source = create_tex_template(tex_source).substitute(args)
        save_tex(out_dir, language, tex_source, "mystery.lies.tex")


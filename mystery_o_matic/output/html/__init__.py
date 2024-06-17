from mystery_o_matic.output import create_template
from mystery_o_matic.output.html.utils import (
    read_html_template,
    build_website,
    get_bullet_list,
    get_options_selector,
    get_subtitle,
    get_char_name,
    save_json,
)


def produce_html_output(
    static_dir, out_dir, mystery, weapons, locations, story_clue
):
    html_template = read_html_template(static_dir + "/index.template.html")
    intervals = mystery.get_intervals()
    suspects = mystery.get_suspects()
    select_suspects = get_options_selector(suspects, notranslate=True)
    select_intervals = get_options_selector(intervals)
    select_weapons = get_options_selector(
        map(lambda n: locations.weapon_locations[n], locations.graph.nodes())
    )

    characters = list(map(lambda char: char.capitalize(), mystery.get_characters()))
    introLocation = ", ".join(characters[:-1]) + " and " + characters[-1]
    introLocation += locations.intro

    names_html = {}
    for i, char in enumerate(mystery.get_characters()):
        names_html["CHAR" + str(i + 1)] = get_char_name(char)
    names_html["NOBODY"] = "nobody"

    names_html["SUS0"] = suspects[0].capitalize()
    names_html["SUS1"] = suspects[1].capitalize()

    for room, name in locations.names.items():
        names_html[room] = name

    names_txt = {}
    for i, char in enumerate(mystery.get_characters()):
        names_txt["CHAR" + str(i + 1)] = char.lower()
    names_txt["NOBODY"] = "nobody"

    for room, name in locations.names.items():
        names_txt[room] = name

    intro = ""
    bullets = []
    for i, clue in enumerate(mystery.initial_clues):
        bullets.append(str(clue))

    bullets.append(
        "The murderer was alone with their victim, and the body remained unmoved"
    )

    bullets.append(
        "The murderer wasn't caught with the body"
    )

    sub_bullets = []
    for loc, weapon in locations.weapon_locations.items():
        sub_bullets.append("The {} from the ${}".format(weapon + " (" + weapons[weapon] + ")", loc))

    weapon_locations_bullets = (
        "The killer retrieved the murder weapon from one of these rooms:\n"
    )
    weapon_locations_bullets += get_bullet_list(sub_bullets)
    bullets.append(weapon_locations_bullets)

    sub_bullets = []
    for c, p in mystery.final_locations.items():
        sub_bullets.append("{} was in the {}".format(c, p))

    final_locations_map = {}
    for c, p in mystery.final_locations.items():
        c = create_template(c).substitute(names_txt)
        p = create_template(p).substitute(names_txt)
        final_locations_map[c] = p

    representations_map = {}
    for l, r in locations.representations.items():
        l = create_template("$"+l).substitute(names_txt)
        representations_map[l] = r

    # the weapons map will be computed reversing the location_weapons one
    weapons_map = {}
    for l, w in locations.weapon_locations.items():
        l = create_template("$"+l).substitute(names_txt)
        weapons_map[w] = l

    final_locations_bullets = "When you arrived at {}:\n".format(
        mystery.final_time
    )
    final_locations_bullets += get_bullet_list(sub_bullets)
    bullets.append(final_locations_bullets)
    bullets.append("No one else was present in the location.")

    initial_clues = get_bullet_list(bullets)

    additional_clues = []

    for i, clue in enumerate(mystery.additional_clues):
        additional_clues.append(create_template(str(clue)).substitute(names_html))

    additional_clues_with_lies = []

    for i, clue in enumerate(mystery.additional_clues_with_lies):
        additional_clues_with_lies.append(create_template(str(clue)).substitute(names_html))

    correct_answer = mystery.get_answer_hash()

    args = {}
    args["introLocation"] = introLocation
    args["initialClues"] = initial_clues
    args["selectIntervals"] = select_intervals
    args["selectSuspects"] = select_suspects
    args["selectWeapon"] = select_weapons
    args["storyClue"] = story_clue

    json = {}
    json["numIntervals"] = len(intervals)
    json["characterNames"] = mystery.get_characters()
    json["victim"] = create_template(mystery.victim).substitute(names_txt)
    json["locationMap"] = final_locations_map
    json["locationIcons"] = representations_map
    json["weaponMap"] = weapons_map
    json["weaponIcons"] = weapons
    json["timeOffset"] = 9 * 3600
    json["additionalClues"] = additional_clues
    json["additionalCluesWithLies"] = additional_clues_with_lies
    json["correctAnswer"] = correct_answer

    html_source = html_template.substitute(args)
    html_source = create_template(html_source).substitute(names_html)
    build_website(out_dir, static_dir, html_source)
    save_json(out_dir, "data = ", json)

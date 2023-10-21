from mystery_o_matic.output import create_template
from mystery_o_matic.output.html.utils import (
    read_html_template,
    build_website,
    get_bullet_list,
    get_options_selector,
    get_subtitle,
    get_card,
    get_char_name,
    save_json
)


def produce_html_output(
    static_dir, out_dir, mystery, weapon_locations, locations, story_clue
):
    html_template = read_html_template(static_dir + "/index.template.html")
    intervals = mystery.get_intervals()
    select_suspects = get_options_selector(mystery.get_characters())
    select_intervals = get_options_selector(intervals)
    select_weapons = get_options_selector(
        map(lambda n: weapon_locations[n], locations.nodes())
    )

    names_html = {}
    for i, char in enumerate(mystery.get_characters()):
        names_html["CHAR" + str(i + 1)] = get_char_name(char)
    names_html["NOBODY"] = "nobody"

    names_html["BEDROOM"] = "bedroom"
    names_html["LIVING"] = "living room"
    names_html["KITCHEN"] = "kitchen"
    names_html["BATHROOM"] = "bathroom"

    names_txt = {}
    for i, char in enumerate(mystery.get_characters()):
        names_txt["CHAR" + str(i + 1)] = char.lower()
    names_txt["NOBODY"] = "nobody"

    names_txt["BEDROOM"] = "bedroom"
    names_txt["LIVING"] = "living room"
    names_txt["KITCHEN"] = "kitchen"
    names_txt["BATHROOM"] = "bathroom"

    intro = ""
    bullets = []
    for i, clue in enumerate(mystery.initial_clues):
        bullets.append(str(clue))

    bullets.append(
        "The murderer was alone with their victim and the body was not moved"
    )

    sub_bullets = []
    for loc, weapon in weapon_locations.items():
        sub_bullets.append("The {} from the ${}".format(weapon, loc))

    weapon_locations_bullets = (
        "The killer took the murder weapon from one of these rooms:\n"
    )
    weapon_locations_bullets += get_bullet_list(sub_bullets)
    bullets.append(weapon_locations_bullets)

    sub_bullets = []
    for c, p in mystery.final_locations.items():
        sub_bullets.append("{} was in the {}".format(c, p))

    final_locations_map = {}
    for (c, p) in mystery.final_locations.items():
        c = create_template(c).substitute(names_txt)
        p = create_template(p).substitute(names_txt)
        final_locations_map[c] = p

    final_locations_bullets = "When the police arrived at {}:\n".format(
        mystery.final_time
    )
    final_locations_bullets += get_bullet_list(sub_bullets)
    bullets.append(final_locations_bullets)

    initial_clues = get_bullet_list(bullets)

    additional_clues = ""

    for i, clue in enumerate(mystery.additional_clues):
        additional_clues += get_card("Clue #{}".format(i + 1), str(clue), i + 1) + "\n"

    correct_answer = mystery.get_answer_hash()

    args = {}
    args["initialClues"] = initial_clues
    args["mysteryClues"] = additional_clues
    args["selectIntervals"] = select_intervals
    args["selectSuspects"] = select_suspects
    args["selectWeapon"] = select_weapons
    args["storyClue"] = story_clue

    json = {}
    json["numIntervals"] = len(intervals)
    json["suspectNames"] = mystery.get_characters()
    json["finalLocationsMap"] = final_locations_map
    json["timeOffset"] = 9 * 3600
    json["correctAnswer"] = correct_answer

    html_source = html_template.substitute(args)
    html_source = create_template(html_source).substitute(names_html)
    build_website(out_dir, static_dir, html_source)
    save_json(out_dir, "data = ", json)

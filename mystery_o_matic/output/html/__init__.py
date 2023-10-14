from mystery_o_matic.output import create_template
from mystery_o_matic.output.html.utils import (
    read_html_template,
    build_website,
    get_bullet_list,
    get_options_selector,
    get_subtitle,
    get_accordion,
    get_char_name,
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

    final_locations_bullets = "When the police arrived at {}:\n".format(
        mystery.final_time
    )
    final_locations_bullets += get_bullet_list(sub_bullets)
    bullets.append(final_locations_bullets)

    initial_clues = get_bullet_list(bullets)

    additional_clues = ""

    for i, clue in enumerate(mystery.additional_clues):
        additional_clues += (
            get_accordion("Clue #{}".format(i + 1), str(clue), i + 1) + "\n"
        )

    correct_answer = mystery.get_answer_hash()

    args = {}
    args["initialClues"] = initial_clues
    args["mysteryClues"] = additional_clues
    args["selectIntervals"] = select_intervals
    args["selectSuspects"] = select_suspects
    args["selectWeapon"] = select_weapons
    args["numIntervals"] = str(len(intervals))
    args["suspectNames"] = str(mystery.get_characters())
    args["correctAnswer"] = correct_answer
    args["storyClue"] = story_clue

    html_source = html_template.substitute(args)
    args = {}
    for i, char in enumerate(mystery.get_characters()):
        args["CHAR" + str(i + 1)] = get_char_name(char)
    args["NOBODY"] = "nobody"

    args["BEDROOM"] = "bedroom"
    args["LIVING"] = "living room"
    args["KITCHEN"] = "kitchen"
    args["BATHROOM"] = "bathroom"

    html_source = create_template(html_source).substitute(args)
    build_website(out_dir, static_dir, html_source)

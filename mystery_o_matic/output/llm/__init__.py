from mystery_o_matic.output import create_template
from mystery_o_matic.output.llm.utils import (
    read_txt_template,
    get_bullet_list,
    remove_emojis,
    save_txt,
)
from mystery_o_matic.clues import NoOneElseStatement
from mystery_o_matic.traits import CHARACTER_DESCRIPTORS

# Per-character line mapping the vague "a woman" / "someone wearing X" sightings
# to a name. {gender} is the descriptor ("a woman"), {trait} the bio noun phrase.
# The LLM file is only produced in English.
SUSPECT_DESC_FRAME = "{name} is {gender}, recognizable by {trait}."


def produce_llm_output(
    static_dir, out_dir, language, mystery, weapons, weapon_labels, locations
):

    connections_list = []
    for src in locations.graph.nodes:
        connections = []
        for dst in locations.graph[src]:
            connections.append("$" + dst)
        connections_list.append(
            "The $" + src + " is connected with " + ", ".join(connections)
        )

    connections_list = get_bullet_list(connections_list, 0)

    names_txt = {}
    for i, char in enumerate(mystery.get_characters()):
        names_txt["CHAR" + str(i + 1)] = char.capitalize()
        # Foggy-sighting tell/descriptor tokens (no emoji, like the room names).
        trait = mystery.character_traits.get("$CHAR" + str(i + 1))
        if trait is not None:
            names_txt["TELL_CHAR" + str(i + 1)] = trait["clue"][language]
        desc = CHARACTER_DESCRIPTORS.get(char.lower())
        if desc is not None:
            names_txt["DESC_CHAR" + str(i + 1)] = desc[language]

    for room, name in locations.indices.items():
        names_txt[room] = locations.names[language][name]

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

    if language == "en":
        names_txt["NOBODY"] = "nobody"
        for weapon_type in ["STABBING", "STRANGULATION", "CONTUSION", "PROJECTILE"]:
            names_txt[weapon_type] = weapon_type.lower()

    elif language == "es":
        names_txt["NOBODY"] = "nadie"
        weapon_type_labels_es = {
            "STABBING": "apuñalamiento",
            "STRANGULATION": "estrangulamiento",
            "CONTUSION": "contusión",
            "PROJECTILE": "proyectil",
        }
        for weapon_type in ["STABBING", "STRANGULATION", "CONTUSION", "PROJECTILE"]:
            names_txt[weapon_type] = weapon_type_labels_es[weapon_type]
    else:
        raise ValueError("Unknown language: " + language)

    characters = list(map(lambda char: char.capitalize(), mystery.get_characters()))
    conjunction = " y " if language == "es" else " and "
    introLocation = ", ".join(characters[:-1]) + conjunction + characters[-1]
    introLocation += locations.intro[language]
    introLocation = introLocation.replace("<b>", "").replace("</b>", "")

    for room, name in locations.names[language].items():
        if room not in locations.rindices:
            continue  # skip any missing place
        index = locations.rindices[room]
        names_txt[index] = name

    for weapon, label in weapon_labels[language].items():
        if weapon not in weapons:
            continue
        if language == "es":
            label = label.capitalize()
        names_txt[weapon.replace("$", "")] = label

    # print(names_html)
    bullets = []
    for i, clue in enumerate(mystery.initial_clues):
        bullets.append(clue[language])

    sub_bullets = []
    for clue in mystery.weapon_locations_clues:
        sub_bullets.append(clue[language])

    weapon_locations_bullets = mystery.weapon_locations_intro[language]
    weapon_locations_bullets += get_bullet_list(sub_bullets, 1)
    bullets.append(weapon_locations_bullets)
    bullets.append(mystery.weapon_locations_outro[language])

    sub_bullets = []
    for clue in mystery.final_locations_clues:
        sub_bullets.append(clue[language])

    final_locations_bullets = mystery.final_locations_intro[language]
    final_locations_bullets += get_bullet_list(sub_bullets, 1)
    bullets.append(final_locations_bullets)
    bullets.append(NoOneElseStatement().string()[language])

    initial_clues_list = get_bullet_list(bullets, 0)

    additional_clues = []

    for i, clue in enumerate(mystery.additional_clues):
        additional_clues.append(create_template(clue[language]).substitute(names_txt))

    additional_clues_list = get_bullet_list(additional_clues, 0)

    additional_clues_with_lies = []

    for i, clue in enumerate(mystery.additional_clues_with_lies):
        additional_clues_with_lies.append(
            create_template(clue[language]).substitute(names_txt)
        )

    additional_clues_with_lies = get_bullet_list(additional_clues_with_lies, 0)

    suspect_descriptions = []
    for i, char in enumerate(mystery.get_characters()):
        gender = CHARACTER_DESCRIPTORS.get(char.lower(), {}).get(language)
        trait = mystery.character_traits.get("$CHAR" + str(i + 1))
        if gender is None or trait is None:
            continue
        suspect_descriptions.append(
            SUSPECT_DESC_FRAME.format(
                name=char.capitalize(), gender=gender, trait=trait["bio"][language]
            )
        )
    suspect_descriptions_list = get_bullet_list(suspect_descriptions, 0)

    args = {}
    args["introLocation"] = introLocation
    args["initialClues"] = initial_clues_list
    args["locationConnections"] = connections_list
    args["suspectDescriptions"] = suspect_descriptions_list
    args["additionalClues"] = remove_emojis(additional_clues_list)
    args["additionalCluesWithLies"] = remove_emojis(additional_clues_with_lies)
    args["solution"] = mystery.get_answer()

    txt_template = read_txt_template(static_dir + f"/llms.template.txt")
    txt_source = txt_template.substitute(args)
    txt_output = create_template(txt_source).substitute(names_txt)
    save_txt(out_dir, txt_output, "llms.txt")

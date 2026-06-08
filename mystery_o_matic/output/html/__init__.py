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
from mystery_o_matic.lang import get_renderer
from mystery_o_matic.time import Time
from mystery_o_matic.traits import CHARACTER_DESCRIPTORS, CHARACTER_EMOJIS

# Sentence frame for the profile "distinguishing feature" line. {} is filled
# with the trait's nominative noun phrase + emoji, e.g. "a brass pocket watch (⌚)".
# RU avoids "узнать по <dative>" (the noun phrases are nominative) — review by a
# native speaker, like the other Russian strings.
BIO_FRAME = {
    "en": "Easily recognized by {}.",
    "es": "Se reconoce fácilmente por {}.",
    "ru": "Запоминающаяся деталь — {}.",
}


def _tok(x):
    """Normalize ``CHAR1`` or ``$CHAR1`` to a ``$``-prefixed placeholder."""
    if isinstance(x, str) and not x.startswith("$"):
        return "$" + x
    return x


def _stripped(x):
    return x.replace("$", "") if isinstance(x, str) else str(x)


def _build_solution_steps(language, mystery, names_html):
    """Build localized solution steps for the "peek under the curtain" feature.

    Language-specific phrasing is produced by the registered
    ``LanguageRenderer`` (see ``mystery_o_matic/lang/*``). Renderers return
    template strings with ``$CHAR1``/``$ROOM0``/``$PISTOL`` placeholders
    (plus ``_LOC`` / ``_GEN`` suffixes for Russian cases); we substitute
    them against ``names_html`` — which already resolves names with their
    emoji representation and character modal links, just like the clues.

    Event timestamps mirror the Solidity ``StoryModel`` simulation:
      * ``takesWeapon`` — instantaneous, at the current time.
      * ``move(c, p)``  — if ``lastMovement[c] == time`` insert ``stay()``
                           (+15 min), then ``sawEvents`` advances another
                           +15 min; arrival is at the post-increment time.
      * ``kills(k, v)`` — emitted at the current time, then ``stay()``
                           advances by +15 min.
    """
    r = get_renderer(language)

    interval = mystery.interval_size  # 15 minutes, in seconds
    base_seconds = mystery.initial_time.seconds

    def _clock(offset_seconds):
        return str(Time(base_seconds + offset_seconds))

    def _sub(template_str):
        return create_template(template_str).substitute(names_html)

    time = 0
    last_movement = {}
    current_location = {
        _stripped(c): _tok(p) for c, p in mystery.initial_locations
    }

    weapon_tok = mystery.weapon_used  # already ``$``-prefixed

    initial_items = [
        _sub(r.render_solution_initial_item(_tok(c), _tok(p)))
        for c, p in mystery.initial_locations
    ]

    event_items = []
    for action in mystery.solution:
        verb = action[0]
        if verb == "takesWeapon":
            char_tok = _tok(action[1])
            place_tok = current_location[_stripped(char_tok)]
            event_items.append({
                "time": _clock(time),
                "text": _sub(r.render_solution_takes_weapon(
                    char_tok, weapon_tok, place_tok
                )),
            })
        elif verb == "move":
            char_tok = _tok(action[1])
            dest_tok = _tok(action[2])
            from_tok = current_location[_stripped(char_tok)]
            if last_movement.get(_stripped(char_tok), 0) == time:
                time += interval  # stay()
            time += interval      # sawEvents()
            last_movement[_stripped(char_tok)] = time
            current_location[_stripped(char_tok)] = dest_tok
            event_items.append({
                "time": _clock(time),
                "text": _sub(r.render_solution_move(
                    char_tok, from_tok, dest_tok
                )),
            })
        elif verb == "kills":
            killer_tok = _tok(action[1])
            victim_tok = _tok(action[2])
            place_tok = current_location[_stripped(killer_tok)]
            event_items.append({
                "time": _clock(time),
                "text": _sub(r.render_solution_kills(
                    killer_tok, victim_tok, weapon_tok, place_tok
                )),
            })
            time += interval  # stay()

    return {
        "initialHeader": r.render_solution_initial_header(str(mystery.initial_time)),
        "initialItems": initial_items,
        "eventsHeader": r.render_solution_events_header(),
        "eventsItems": event_items,
    }


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
    json["solutionSteps"] = {}
    json["numIntervals"] = len(intervals)
    json["characterNames"] = mystery.get_characters()
    json["characterEmojis"] = {
        name: CHARACTER_EMOJIS[name]
        for name in mystery.get_characters()
        if name in CHARACTER_EMOJIS
    }
    json["victim"] = create_template(mystery.victim).substitute(names_txt)
    json["locationMap"] = final_locations_map
    json["locationIcons"] = representations_map
    json["weaponMap"] = weapons_map
    json["weaponIcons"] = weapons
    json["timeOffset"] = mystery.initial_time.seconds
    json["correctAnswer"] = correct_answer
    json["characterBios"] = {}

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

        # Distinguishing-feature "tells": register the in-clue form for every
        # character so $TELL_CHARn resolves in the clue substitution below, and
        # collect the nominative bio form shown in the suspect profile modal.
        character_bios = {}
        for i, char in enumerate(mystery.get_characters()):
            placeholder = "$CHAR" + str(i + 1)
            desc = CHARACTER_DESCRIPTORS.get(char.lower())
            if desc is not None:
                names_html["DESC_CHAR" + str(i + 1)] = desc[language]
            trait = mystery.character_traits.get(placeholder)
            if trait is None:
                continue
            suffix = " (" + trait["emoji"] + ")"
            names_html["TELL_CHAR" + str(i + 1)] = trait["clue"][language] + suffix
            character_bios[char.lower()] = BIO_FRAME[language].format(
                trait["bio"][language] + suffix
            )
        json["characterBios"][language] = character_bios

        json["solutionSteps"][language] = _build_solution_steps(
            language, mystery, names_html
        )

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

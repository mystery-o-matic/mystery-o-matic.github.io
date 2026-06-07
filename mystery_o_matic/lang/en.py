from random import randint, choice

from mystery_o_matic.lang import LanguageRenderer, register_renderer
from mystery_o_matic.weapons import get_weapon_type
from mystery_o_matic.time import Time


class EnglishRenderer(LanguageRenderer):
    @property
    def lang_code(self):
        return "en"

    # --- Statements ---

    def render_murder_was_alone(self):
        return "The murderer was alone with their victim, and the body remained unmoved"

    def render_murder_was_not_found_with_body(self):
        return "The murderer wasn't caught with the body"

    def render_weapon_location(self, weapon, vplace):
        return f"The {weapon} from the {vplace}"

    def render_character_location(self, subject, place, victim):
        if subject == victim:
            return f"{subject}'s body was in the {place}"
        else:
            return f"{subject} was in the {place}"

    def render_no_one_else(self):
        return "No one else was present in the location."

    def render_weapon_locations_intro(self):
        return "The killer retrieved the murder weapon from one of these places:\n"

    def render_weapon_locations_outro(self):
        return "No one saw the killer retrieving the murder weapon"

    def render_final_locations_intro(self, time):
        return f"We know where everyone was at {time}:\n"

    # --- Clues ---

    def render_saw_when_arriving(self, subject, object, object_is_alive, place, time, foggy):
        r = randint(0, 2)
        s = f'{subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'The {place} was empty when I arrived at {time}"'
                return s
            r = 0

        if r == 0:
            s += "Saw "
        elif r == 1:
            s += "Noticed "
        elif r == 2:
            s += "Spotted "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not object_is_alive:
            return f'{subject}: "I was horrified to discover {object}\'s body when I arrived at the {place} at {time}"'

        if foggy and object_is_alive:
            if object != "$NOBODY":
                object = "somebody"

        s += f'{object} when I arrived at the {place} at {time}"'
        return s

    def render_not_saw(self, subject, object, place, time):
        r = randint(0, 5)
        s = f'{subject}: "'

        if r == 0:
            s += f'I\'m sure {object} was not with me in the {place} at {time}"'
        elif r == 1:
            s += f'I was in the {place} at {time} but {object} wasn\'t around."'
        elif r == 2:
            s += f'{object} definitely was not with me in the {place} at {time}"'
        elif r == 3:
            s += f'{object} was not with me in the {place} at {time}"'
        elif r == 4:
            s += f'While I was in the {place} at {time}, {object} was nowhere to be seen."'
        elif r == 5:
            s += f'I was in the {place} at {time} but {object} was not there with me."'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def render_saw_victim_when_arriving(self, subject, object, object_is_alive, place, time):
        r = randint(0, 2)
        s = f'{subject}: "'

        if r == 0:
            verb = "saw"
        elif r == 1:
            verb = "noticed"
        elif r == 2:
            verb = "spotted"
        else:
            raise ValueError("Invalid random number: " + str(r))

        r = randint(0, 1)
        if r == 0:
            s += f'{verb.capitalize()} {object} arriving while I was in the {place} at {time}"'
        elif r == 1:
            s += f'I was in the {place} when {verb} {object} arriving at {time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def render_saw_victim_when_leaving(self, subject, object, object_is_alive, place, time):
        r = randint(0, 2)
        s = f'{subject}: "'

        if r == 0:
            verb = "saw"
        elif r == 1:
            verb = "noticed"
        elif r == 2:
            verb = "spotted"
        else:
            raise ValueError("Invalid random number: " + str(r))

        r = randint(0, 1)
        if r == 0:
            s += f'{verb.capitalize()} {object} leaving while I was in the {place} at {time}"'
        elif r == 1:
            s += f'I was in the {place} when {verb} {object} leaving at {time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def render_saw_when_leaving(self, subject, object, object_is_alive, place, time, foggy):
        r = randint(0, 2)
        s = f'{subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'The {place} was empty when I left it at {time}"'
                return s
            r = 0

        if r == 0:
            s += "Saw "
        elif r == 1:
            s += "Noticed "
        elif r == 2:
            s += "Spotted "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not object_is_alive:
            s = f'{subject}: "I was shocked to see the body of '

        if foggy and object_is_alive:
            if object != "$NOBODY":
                object = "somebody"

        s += f'{object} when I was leaving the {place} at {time}"'
        return s

    def render_was_murdered_initial(self, subject, place, time_start, time_end):
        return f"{subject} was murdered in the {place} at some time between {time_start} and {time_end}"

    def render_was_murdered_body_two_options(self, time1, time2):
        return f"A close examination of the body reveals that the murder took place either at {time1} or at {time2}"

    def render_was_victim_dead_at(self, time, alternative):
        if alternative:
            r = "Inspecting the crime scene reveals that the victim had been dead by "
        else:
            r = "A close examination of the body reveals that the victim had been dead by "
        r += f"{time}"
        return r

    def render_was_victim_alive_at(self, time, alternative):
        if alternative:
            r = "Inspecting the crime scene reveals that the victim was alive at "
        else:
            r = "A close examination of the body reveals that the victim was alive at "
        r += f"{time}"
        return r

    def render_was_murdered_after(self, time, interval_size, positive, alternative):
        if alternative:
            r = "Inspecting the crime scene reveals that the victim was murdered "
        else:
            r = "A close examination of the body reveals that the victim was murdered "
        if positive:
            t = Time(time.seconds)
            r += f"after {t}"
        else:
            t = Time(time.seconds + interval_size)
            r += f"not before {t}"
        return r

    def render_was_murdered_before(self, time, interval_size, positive, alternative):
        if alternative:
            r = "Inspecting the crime scene reveals that the victim was murdered "
        else:
            r = "A close examination of the body reveals that the victim was murdered "
        if positive:
            t = Time(time.seconds)
            r += f"before {t}"
        else:
            t = Time(time.seconds - interval_size)
            r += f"not after {t}"
        return r

    def render_was_murdered_scream(self, time1, time2):
        return f"A blood-curdling scream from the victim was heard between {time1} and {time2}"

    def render_evidence(self, subject, place):
        r = randint(0, 2)
        if r == 0:
            return f"A recent footprint matching {subject}'s shoe was found in the {place}"
        elif r == 1:
            return f"A fingerprint of {subject} was found in the {place}. It looks very fresh"
        elif r == 2:
            return f"A strand of hair matching {subject} was found in the {place}, indicating that they were recently there"
        else:
            raise ValueError("Invalid random number: " + str(r))

    def render_stayed(self, subject, place, time_start, time_end, activity=None):
        s = f'{subject}: "'
        if activity is not None:
            s += f'I went to the {place} {activity["en"]} at {time_start} and stayed until {time_end}"'
            return s
        r = randint(0, 2)
        if r == 0:
            s += f'I was in the {place} from {time_start} to {time_end}"'
        elif r == 1:
            s += f'I did not move from the {place} between {time_start} and {time_end}"'
        elif r == 2:
            s += f'Stayed in the {place} from {time_start} to {time_end}"'
        else:
            raise ValueError("Invalid random number: " + str(r))
        return s

    def render_interacted(self, subject0, subject1, place):
        r = randint(0, 1)
        if r == 0:
            return f'{subject0}: "I talked with {subject1} in the {place}"'
        elif r == 1:
            return f'{subject0}: "I chatted with {subject1} in the {place}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

    def render_heard(self, subject, activity_text, time):
        return f'{subject}: "I {activity_text} at {time}"'

    def render_weapon_not_used(self, weapon):
        r = randint(0, 2)

        if r == 0:
            s = "Inspecting the body reveals "
        elif r == 1:
            s = "The inspection of the body indicates "
        elif r == 2:
            s = "The body shows "
        else:
            raise ValueError("Invalid random number: " + str(r))

        weapon_type = get_weapon_type(weapon)
        if weapon_type == "projectile":
            return s + "there are no $PROJECTILE holes."
        elif weapon_type == "strangulation":
            return s + "no signs of $STRANGULATION."
        elif weapon_type == "sharp force":
            return s + "no signs of $STABBING."
        elif weapon_type == "poisoning":
            return s + "that the " + weapon + " was not the murder weapon."
        elif weapon_type == "blunt force":
            return s + "no signs of $CONTUSION."
        else:
            raise ValueError("Unknown type of weapon: " + weapon)


    # --- Solution steps ---

    def render_solution_initial_header(self, time):
        return f"Starting positions at {time}:"

    def render_solution_events_header(self):
        return "What happened next:"

    def render_solution_initial_item(self, subject, place):
        return f"{subject} was in the {place}."

    def render_solution_takes_weapon(self, subject, weapon, place):
        return f"{subject} picked up the {weapon} in the {place}."

    def render_solution_move(self, subject, from_place, to_place):
        return f"{subject} went from the {from_place} to the {to_place}."

    def render_solution_kills(self, killer, victim, weapon, place):
        return f"{killer} murdered {victim} with the {weapon} in the {place}."


register_renderer(EnglishRenderer())

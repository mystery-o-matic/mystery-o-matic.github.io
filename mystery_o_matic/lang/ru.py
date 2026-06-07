from random import randint, choice

from mystery_o_matic.lang import LanguageRenderer, register_renderer
from mystery_o_matic.weapons import get_weapon_type
from mystery_o_matic.time import Time


class RussianRenderer(LanguageRenderer):
    @property
    def lang_code(self):
        return "ru"

    # --- Statements ---

    def render_murder_was_alone(self):
        return "Убийца был(а) наедине с жертвой, и тело осталось на месте"

    def render_murder_was_not_found_with_body(self):
        return "Убийцу не застали рядом с телом"

    def render_weapon_location(self, weapon, vplace):
        return f"{weapon} — {vplace}"

    def render_character_location(self, subject, place, victim):
        if subject == victim:
            return f"Тело {subject} находилось в {place}_LOC"
        else:
            return f"{subject} находился(ась) в {place}_LOC"

    def render_no_one_else(self):
        return "В этом месте больше никого не было."

    def render_weapon_locations_intro(self):
        return "Убийца взял(а) орудие убийства из одного из следующих мест:\n"

    def render_weapon_locations_outro(self):
        return "Никто не видел, как убийца брал(а) орудие убийства"

    def render_final_locations_intro(self, time):
        return f"Нам известно, где находился(ась) каждый(ая) в {time}:\n"

    # --- Clues ---

    def render_saw_when_arriving(self, subject, object, object_is_alive, place, time, foggy):
        r = randint(0, 2)
        s = f'{subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'В {place}_LOC никого не было, когда я пришёл(ла) в {time}"'
                return s
            r = 0

        if r == 0:
            s += "Увидел(а) "
        elif r == 1:
            s += "Заметил(а) "
        elif r == 2:
            s += "Разглядел(а) "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not object_is_alive:
            return f'{subject}: "Я был(а) потрясён(а), обнаружив тело {object}, когда я пришёл(ла) в {place}_LOC в {time}"'

        if foggy and object_is_alive:
            if object != "$NOBODY":
                object = "кого-то"

        s += f'{object}, когда я пришёл(ла) в {place}_LOC в {time}"'
        return s

    def render_not_saw(self, subject, object, place, time):
        r = randint(0, 5)
        s = f'{subject}: "'

        if r == 0:
            s += f'Уверен(а), что {object} не было рядом со мной в {place}_LOC в {time}"'
        elif r == 1:
            s += f'Я был(а) в {place}_LOC в {time}, но {object} там не было"'
        elif r == 2:
            s += f'{object} точно не было рядом со мной в {place}_LOC в {time}"'
        elif r == 3:
            s += f'{object} не было со мной в {place}_LOC в {time}"'
        elif r == 4:
            s += f'Пока я был(а) в {place}_LOC в {time}, {object} нигде не было видно"'
        elif r == 5:
            s += f'Я был(а) в {place}_LOC в {time}, но {object} не было рядом"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def render_saw_victim_when_arriving(self, subject, object, object_is_alive, place, time):
        r = randint(0, 2)
        s = f'{subject}: "'

        if r == 0:
            verb = "увидел(а)"
        elif r == 1:
            verb = "заметил(а)"
        elif r == 2:
            verb = "разглядел(а)"
        else:
            raise ValueError("Invalid random number: " + str(r))

        if object_is_alive:
            object_phrase = f"{object} прибывающим(ей)"
        else:
            object_phrase = f"тело {object} прибывшим(ей)"

        r = randint(0, 1)
        if r == 0:
            s += f'{verb.capitalize()} {object_phrase} в {place}_LOC в {time}"'
        elif r == 1:
            s += f'Я был(а) в {place}_LOC, когда {verb} {object_phrase} в {time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def render_saw_victim_when_leaving(self, subject, object, object_is_alive, place, time):
        r = randint(0, 2)
        s = f'{subject}: "'

        if r == 0:
            verb = "увидел(а)"
        elif r == 1:
            verb = "заметил(а)"
        elif r == 2:
            verb = "разглядел(а)"
        else:
            raise ValueError("Invalid random number: " + str(r))

        r = randint(0, 1)
        if r == 0:
            s += f'{verb.capitalize()} уходящего(ую) {object} из {place}_GEN в {time}"'
        elif r == 1:
            s += f'Я был(а) в {place}_LOC, когда {verb} {object} уходящим(ей) в {time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def render_saw_when_leaving(self, subject, object, object_is_alive, place, time, foggy):
        r = randint(0, 2)
        s = f'{subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'В {place}_LOC было пусто, когда я уходил(а) в {time}"'
                return s
            r = 0

        if r == 0:
            s += "Увидел(а) "
        elif r == 1:
            s += "Заметил(а) "
        elif r == 2:
            s += "Разглядел(а) "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not object_is_alive:
            return f'{subject}: "Я был(а) потрясён(а), увидев тело {object} в {place}_LOC в {time}"'

        if foggy and object_is_alive:
            if object != "$NOBODY":
                object = "кого-то"

        s += f'{object}, уходя из {place}_GEN в {time}"'
        return s

    def render_was_murdered_initial(self, subject, place, time_start, time_end):
        return f"{subject} был(а) убит(а) в {place}_LOC в промежуток между {time_start} и {time_end}"

    def render_was_murdered_body_two_options(self, time1, time2):
        return f"Тщательный осмотр тела показывает, что убийство произошло в {time1} или в {time2}"

    def render_was_victim_dead_at(self, time, alternative):
        if alternative:
            r = "Осмотр места преступления показывает, что жертва была мертва к "
        else:
            r = "Тщательный осмотр тела показывает, что жертва была мертва к "
        r += f"{time}"
        return r

    def render_was_victim_alive_at(self, time, alternative):
        if alternative:
            r = "Осмотр места преступления показывает, что жертва была жива в "
        else:
            r = "Тщательный осмотр тела показывает, что жертва была жива в "
        r += f"{time}"
        return r

    def render_was_murdered_after(self, time, interval_size, positive, alternative):
        if alternative:
            r = "Осмотр места преступления показывает, что убийство произошло "
        else:
            r = "Тщательный осмотр тела показывает, что убийство произошло "
        if positive:
            t = Time(time.seconds)
            r += f"после {t}"
        else:
            t = Time(time.seconds + interval_size)
            r += f"не раньше {t}"
        return r

    def render_was_murdered_before(self, time, interval_size, positive, alternative):
        if alternative:
            r = "Осмотр места преступления показывает, что убийство произошло "
        else:
            r = "Тщательный осмотр тела показывает, что убийство произошло "
        if positive:
            t = Time(time.seconds)
            r += f"до {t}"
        else:
            t = Time(time.seconds - interval_size)
            r += f"не позже {t}"
        return r

    def render_was_murdered_scream(self, time1, time2):
        return f"Леденящий кровь крик жертвы был услышан между {time1} и {time2}"

    def render_evidence(self, subject, place):
        r = randint(0, 2)
        if r == 0:
            return f"Свежий след обуви, соответствующий следам {subject}, был найден в {place}_LOC"
        elif r == 1:
            return f"Отпечаток пальца {subject} был обнаружен в {place}_LOC. Он выглядит совсем свежим"
        elif r == 2:
            return f"Прядь волос, принадлежащая {subject}, была найдена в {place}_LOC, что указывает на недавнее присутствие"
        else:
            raise ValueError("Invalid random number: " + str(r))

    def render_stayed(self, subject, place, time_start, time_end, activity=None):
        s = f'{subject}: "'
        if activity is not None:
            s += f'Я был(а) в {place}_LOC, чтобы {activity["ru"]}, с {time_start} до {time_end}"'
            return s
        r = randint(0, 2)
        if r == 0:
            s += f'Я был(а) в {place}_LOC с {time_start} до {time_end}"'
        elif r == 1:
            s += f'Я не двигался(ась) с места в {place}_LOC между {time_start} и {time_end}"'
        elif r == 2:
            s += f'Оставался(ась) в {place}_LOC с {time_start} до {time_end}"'
        else:
            raise ValueError("Invalid random number: " + str(r))
        return s

    def render_interacted(self, subject0, subject1, place):
        r = randint(0, 1)
        if r == 0:
            return f'{subject0}: "Я разговаривал(а) с {subject1} в {place}_LOC"'
        elif r == 1:
            return f'{subject0}: "Я болтал(а) с {subject1} в {place}_LOC"'
        else:
            raise ValueError("Invalid random number: " + str(r))

    def render_heard(self, subject, activity_text, time):
        return f'{subject}: "Я {activity_text} в {time}"'

    def render_weapon_not_used(self, weapon):
        r = randint(0, 2)

        if r == 0:
            s = "Осмотр тела показывает "
        elif r == 1:
            s = "Обследование тела указывает "
        elif r == 2:
            s = "На теле "
        else:
            raise ValueError("Invalid random number: " + str(r))

        weapon_type = get_weapon_type(weapon)
        if weapon_type == "projectile":
            if r == 2:
                return s + "нет огнестрельных ранений ($PROJECTILE)."
            return s + "на отсутствие огнестрельных ранений ($PROJECTILE)."
        elif weapon_type == "strangulation":
            if r == 2:
                return s + "нет признаков $STRANGULATION."
            return s + "на отсутствие признаков $STRANGULATION."
        elif weapon_type == "sharp force":
            if r == 2:
                return s + "нет признаков $STABBING."
            return s + "на отсутствие признаков $STABBING."
        elif weapon_type == "poisoning":
            if r == 2:
                return s + f"нет признаков отравления {weapon}."
            return s + f"на то, что {weapon} не является орудием убийства."
        elif weapon_type == "blunt force":
            if r == 2:
                return s + "нет признаков $CONTUSION."
            return s + "на отсутствие признаков $CONTUSION."
        else:
            raise ValueError("Unknown type of weapon: " + weapon)


    # --- Solution steps ---

    def render_solution_initial_header(self, time):
        return f"Начальные позиции в {time}:"

    def render_solution_events_header(self):
        return "Что произошло дальше:"

    def render_solution_initial_item(self, subject, place):
        return f"{subject} находился(ась) в {place}_LOC."

    def render_solution_takes_weapon(self, subject, weapon, place):
        return f"{subject} взял(а) {weapon} в {place}_LOC."

    def render_solution_move(self, subject, from_place, to_place):
        # Russian "в + accusative" for motion is not available in the
        # location data (only ``_LOC`` and ``_GEN``). Rephrase as
        # "ended up in Y, having left X" which is correct with locative +
        # genitive respectively.
        return (
            f"{subject} оказался(ась) в {to_place}_LOC, "
            f"выйдя из {from_place}_GEN."
        )

    def render_solution_kills(self, killer, victim, weapon, place):
        return (
            f"{killer} убил(а) {victim} с помощью {weapon} в {place}_LOC."
        )


register_renderer(RussianRenderer())

from random import randint, choice

from mystery_o_matic.lang import LanguageRenderer, register_renderer
from mystery_o_matic.weapons import get_weapon_type
from mystery_o_matic.time import Time
from mystery_o_matic.traits import COARSE_PHRASES


class SpanishRenderer(LanguageRenderer):
    @property
    def lang_code(self):
        return "es"

    # --- Statements ---

    def render_murder_was_alone(self):
        return "El asesino estaba a solas con la víctima y el cuerpo no se movió"

    def render_murder_was_not_found_with_body(self):
        return "El asesino no fue encontrado con el cuerpo"

    def render_weapon_location(self, weapon, vplace):
        return f"{weapon} — {vplace}"

    def render_character_location(self, subject, place, victim):
        if subject == victim:
            return f"El cuerpo de {subject} estaba en {place}"
        else:
            return f"{subject} estaba en {place}"

    def render_no_one_else(self):
        return "No había nadie más en el lugar"

    def render_weapon_locations_intro(self):
        return "El asesino consiguió el arma homicida de uno de los siguientes lugares:\n"

    def render_weapon_locations_outro(self):
        return "Nadie vió al asesino tomar el arma homicida"

    def render_final_locations_intro(self, time):
        return f"Sabemos donde estaban todos a las {time}:\n"

    # --- Clues ---

    def render_saw_when_arriving(self, subject, object, object_is_alive, place, time, fog_kind=None):
        r = randint(0, 2)
        s = f'{subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'{place} estaba vacío cuando llegué a las {time}"'
                return s
            r = 0

        if r == 0:
            s += "Vi "
        elif r == 1:
            s += "Noté "
        elif r == 2:
            s += "Distinguí "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not object_is_alive:
            return f'{subject}: "Me horroricé al descubrir el cuerpo de {object} cuando llegué a {place} a las {time}"'

        if object_is_alive and object != "$NOBODY" and fog_kind:
            if fog_kind == "trait":
                object = "alguien $TELL_" + object.replace("$", "")
            elif fog_kind == "descriptor":
                object = "$DESC_" + object.replace("$", "")
            elif fog_kind in COARSE_PHRASES:
                object = COARSE_PHRASES[fog_kind][self.lang_code]
            else:
                object = "alguien"

        s += f'a {object} cuando llegué a {place} a las {time}"'
        return s

    def render_not_saw(self, subject, object, place, time):
        r = randint(0, 5)
        s = f'{subject}: "'

        if r == 0:
            s += f'Estoy seguro de que {object} no estaba conmigo en {place} a las {time}"'
        elif r == 1:
            s += f'Estuve en {place} a las {time} pero {object} no estaba por ahí"'
        elif r == 2:
            s += f'{object} definitivamente no estaba conmigo en {place} a las {time}"'
        elif r == 3:
            s += f'{object} no estaba conmigo en {place} a las {time}"'
        elif r == 4:
            s += f'Mientras estaba en {place} a las {time}, {object} no se veía por ningún lado"'
        elif r == 5:
            s += f'Estuve en {place} a las {time} pero {object} no estaba ahí conmigo"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def render_saw_victim_when_arriving(self, subject, object, object_is_alive, place, time):
        r = randint(0, 2)
        s = f'{subject}: "'

        if r == 0:
            verb = "vi"
        elif r == 1:
            verb = "noté"
        elif r == 2:
            verb = "divisé"
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not object_is_alive:
            s += "el cuerpo de "

        r = randint(0, 1)
        if r == 0:
            s += f'{verb.capitalize()} a {object} llegando mientras estaba en {place} a las {time}"'
        elif r == 1:
            s += f'Estaba en {place} cuando {verb} a {object} llegando a las {time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def render_saw_victim_when_leaving(self, subject, object, object_is_alive, place, time):
        r = randint(0, 2)
        s = f'{subject}: "'

        if r == 0:
            verb = "vi"
        elif r == 1:
            verb = "noté"
        elif r == 2:
            verb = "divisé"
        else:
            raise ValueError("Invalid random number: " + str(r))

        r = randint(0, 1)
        if r == 0:
            s += f'{verb.capitalize()} a {object} yéndose mientras estaba en {place} a las {time}"'
        elif r == 1:
            s += f'Estaba en {place} cuando {verb} a {object} yéndose a las {time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def render_saw_when_leaving(self, subject, object, object_is_alive, place, time, fog_kind=None):
        r = randint(0, 2)
        s = f'{subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'{place} estaba vacío cuando me fui a las {time}"'
                return s
            r = 0

        if r == 0:
            s += "Vi "
        elif r == 1:
            s += "Noté "
        elif r == 2:
            s += "Distinguí "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not object_is_alive:
            return f'{subject}: "Me impactó ver el cuerpo de {object} cuando me iba de {place} a las {time}"'

        if object_is_alive and object != "$NOBODY" and fog_kind:
            if fog_kind == "trait":
                object = "alguien $TELL_" + object.replace("$", "")
            elif fog_kind == "descriptor":
                object = "$DESC_" + object.replace("$", "")
            elif fog_kind in COARSE_PHRASES:
                object = COARSE_PHRASES[fog_kind][self.lang_code]
            else:
                object = "alguien"

        s += f'a {object} cuando me iba de {place} a las {time}"'
        return s

    def render_was_murdered_initial(self, subject, place, time_start, time_end):
        return f"{subject} fue asesinado en {place} en algún momento entre las {time_start} y las {time_end}"

    def render_was_murdered_body_two_options(self, time1, time2):
        return f"Un examen minucioso del cuerpo revela que el asesinato tuvo lugar a las {time1} o las {time2}"

    def render_was_victim_dead_at(self, time, alternative):
        if alternative:
            r = "Inspeccionando la escena del crimen se revela que la víctima ya estaba muerta a las "
        else:
            r = "Un examen minucioso del cuerpo revela que la víctima ya estaba muerta a las "
        r += f"{time}"
        return r

    def render_was_victim_alive_at(self, time, alternative):
        if alternative:
            r = "Inspeccionando la escena del crimen se revela que la víctima estaba viva a las "
        else:
            r = "Un examen minucioso del cuerpo revela que la víctima estaba viva a las "
        r += f"{time}"
        return r

    def render_was_murdered_after(self, time, interval_size, positive, alternative):
        if alternative:
            r = "Inspeccionando la escena del crimen se revela que el asesinato tuvo lugar "
        else:
            r = "Un examen minucioso del cuerpo revela que el asesinato tuvo lugar "
        if positive:
            t = Time(time.seconds)
            r += f"después de las {t}"
        else:
            t = Time(time.seconds + interval_size)
            r += f"no antes de las {t}"
        return r

    def render_was_murdered_before(self, time, interval_size, positive, alternative):
        if alternative:
            r = "Inspeccionando la escena del crimen se revela que el asesinato tuvo lugar "
        else:
            r = "Un examen minucioso del cuerpo revela que el asesinato tuvo lugar "
        if positive:
            t = Time(time.seconds)
            r += f"antes de las {t}"
        else:
            t = Time(time.seconds - interval_size)
            r += f"no después de las {t}"
        return r

    def render_was_murdered_scream(self, time1, time2):
        return f"Un grito espeluznante de la víctima se escuchó entre las {time1} y las {time2}"

    def render_evidence(self, subject, place):
        r = randint(0, 2)
        if r == 0:
            return f"Una pisada reciente, compatible con el calzado de {subject}, fue encontrada en {place}"
        elif r == 1:
            return f"Una huella digital de {subject} fue identificada en {place}. Se ve muy reciente"
        elif r == 2:
            return f"Una hebra de pelo de {subject} fue encontrada en {place}, indicando que estuvo recientemente ahí"
        else:
            raise ValueError("Invalid random number: " + str(r))

    def render_stayed(self, subject, place, time_start, time_end, activity=None):
        s = f'{subject}: "'
        if activity is not None:
            s += f'Fui a {place} {activity["es"]} a las {time_start} y me quedé hasta las {time_end}"'
            return s
        r = randint(0, 2)
        if r == 0:
            s += f'Estuve en {place} desde las {time_start} hasta las {time_end}"'
        elif r == 1:
            s += f'No me moví de {place} entre las {time_start} y las {time_end}"'
        elif r == 2:
            s += f'Me quedé en {place} desde las {time_start} hasta las {time_end}"'
        else:
            raise ValueError("Invalid random number: " + str(r))
        return s

    def render_interacted(self, subject0, subject1, place):
        r = randint(0, 1)
        if r == 0:
            return f'{subject0}: "Hablé con {subject1} en {place}"'
        elif r == 1:
            return f'{subject0}: "Charlé con {subject1} en {place}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

    def render_heard(self, subject, activity_text, time):
        return f'{subject}: "Yo {activity_text} a las {time}"'

    def render_weapon_not_used(self, weapon):
        r = randint(0, 2)

        if r == 0:
            s = "Una inspección del cuerpo revela "
        elif r == 1:
            s = "La inspección del cuerpo indica "
        elif r == 2:
            s = "El cuerpo muestra "
        else:
            raise ValueError("Invalid random number: " + str(r))

        weapon_type = get_weapon_type(weapon)
        if weapon_type == "projectile":
            return s + "que no había orificio de $PROJECTILE."
        elif weapon_type == "strangulation":
            return s + "que no había signos de $STRANGULATION."
        elif weapon_type == "sharp force":
            return s + "que no había signos de $STABBING."
        elif weapon_type == "poisoning":
            return s + "que " + weapon + " no era el arma homicida."
        elif weapon_type == "blunt force":
            return s + "que no había signos de $CONTUSION."
        else:
            raise ValueError("Unknown type of weapon: " + weapon)


    # --- Solution steps ---

    def render_solution_initial_header(self, time):
        return f"Posiciones iniciales a las {time}:"

    def render_solution_events_header(self):
        return "Lo que ocurrió después:"

    def render_solution_initial_item(self, subject, place):
        return f"{subject} estaba en {place}."

    def render_solution_takes_weapon(self, subject, weapon, place):
        return f"{subject} tomó {weapon} en {place}."

    def render_solution_move(self, subject, from_place, to_place):
        return f"{subject} fue desde {from_place} hasta {to_place}."

    def render_solution_kills(self, killer, victim, weapon, place):
        return f"{killer} asesinó a {victim} con {weapon} en {place}."


register_renderer(SpanishRenderer())

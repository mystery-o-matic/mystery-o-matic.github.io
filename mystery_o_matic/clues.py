from abc import ABC, abstractmethod
from random import randint, choice

from mystery_o_matic.weapons import get_weapon_type

class AbstractStatement(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def string_english(self):
        return ""

    @abstractmethod
    def string_spanish(self):
        return ""

    def string(self):
        return {
            'en': self.string_english(),
            'es': self.string_spanish()
        }

class MurderWasAloneStatement(AbstractStatement):
    def string_english(self):
        return "The murderer was alone with their victim, and the body remained unmoved"
    def string_spanish(self):
        return "El asesino estaba a solas con la víctima y el cuerpo no se movió"

class MurderWasNotFoundWithBodyStatement(AbstractStatement):
    def string_english(self):
        return "The murderer wasn't caught with the body"

    def string_spanish(self):
        return "El asesino no fue encontrado con el cuerpo"

class WeaponLocationStatement(AbstractStatement):
    def __init__(self, weapon, vplace):
        self.vplace = vplace
        self.weapon = weapon
    def string_english(self):
        return f"The {self.weapon} from the {self.vplace}"

    def string_spanish(self):
        return f"{self.weapon} en {self.vplace}"

class CharacterLocationStatement(AbstractStatement):
    def __init__(self, subject, place):
        self.subject = subject
        self.place = place

    def string_english(self):
        return f"{self.subject} was in the {self.place}"

    def string_spanish(self):
        return f"{self.subject} estaba en {self.place}"

class NoOneElseStatement(AbstractStatement):
    def string_english(self):
        return "No one else was present in the location."
    def string_spanish(self):
        return "No había nadie más en el lugar"

class WeaponLocationsIntroStatement(AbstractStatement):
    def string_english(self):
        return "The killer retrieved the murder weapon from one of these places:\n"

    def string_spanish(self):
        return "El asesino consiguió el arma homicida de uno de los siguientes lugares:\n"

class WeaponLocationsOutroStatement(AbstractStatement):
    def string_english(self):
        return "No one saw the killer retriving the murder weapon"

    def string_spanish(self):
        return "Nadie vió al asesino tomar el arma homicida"

class FinalLocationsIntroStatement(AbstractStatement):
    def __init__(self, time):
        self.time = time

    def string_english(self):
        return f"When you arrived at {self.time}:\n"

    def string_spanish(self):
        return f"Cuando llegaste, a las {self.time}:\n"

class AbstractClue(ABC):
    subject = None
    object = None
    object_is_alive = None
    place = None
    time = None
    foggy = None

    def __init__(self):
        r = randint(1, 10)
        self.foggy = False
        if r <= 5:
            self.foggy = True

    @abstractmethod
    def string_english(self):
        return ""

    @abstractmethod
    def string_spanish(self):
        return ""

    def string(self):
        return {
            'en': self.string_english(),
            'es': self.string_spanish()
        }

class SawWhenArrivingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()

    def string_english(self):
        object = self.object
        r = randint(0, 2)
        s = f'{self.subject} said "'

        if object == "$NOBODY":
            r = 0

        if r == 0:
            s += "I saw "
        elif r == 1:
            s += "I noticed "
        elif r == 2:
            s += "I spotted "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not self.object_is_alive:
            s += "the body of "

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "somebody"

        s += f'{object} when I arrived to the {self.place} at {self.time}"'
        return s

    def string_spanish(self):
        object = self.object
        r = randint(0, 2)
        s = f'{self.subject} dijo "'

        if r == 0:
            if object == "$NOBODY":
                s += "No vi "
            else:
                s += "Vi "
        elif r == 1:
            if object == "$NOBODY":
                s += "No noté "
            else:
                s += "Noté "
        elif r == 2:
            if object == "$NOBODY":
                s += "No distinguí "
            else:
                s += "Distinguí "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not self.object_is_alive:
            s += "el cuerpo de "
        else:
            s += "a "

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "alguien"

        s += f'{object} cuando llegué a {self.place} a las {self.time}"'
        return s

    def is_incriminating(self, killer, victim, place, time):
        if self.subject == killer and self.object == victim:
            return True
        return False

    def manipulate(self, killer, victim, alibi_place):
        if self.subject == killer and self.object == victim:
            if not self.object_is_alive:
                # If the body was seen, it is too suspicious to change
                return None

            # r = randint(0, 1)
            # if r == 0:
            self.object = "$NOBODY"
            # elif r == 1:
            self.place = alibi_place

            return self
        raise ValueError("Invalid manipulation: " + str(self))


class NotSawWhenArrivingLeavingClue(AbstractClue):
    def __init__(self, subject, object, place, time):
        self.subject = subject
        self.object = object
        self.place = place
        self.time = time
        super().__init__()

    def string_spanish(self):
        return f'{self.subject} dijo: "No recuerdo que {self.object} estuviese conmigo en {self.place} a las {self.time}"'

    def string_english(self):
        r = randint(0, 2)
        s = f'{self.subject} said: "'

        if r == 0:
            s += ""
        elif r == 1:
            s += "I think "
        elif r == 2:
            s += "I'm sure "
        else:
            raise ValueError("Invalid random number: " + str(r))

        s += f'{self.object} was not with me in the {self.place} at {self.time}"'
        return s

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class SawVictimWhenArrivingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()

    def string_english(self):
        s = f'{self.subject} said: "I saw '
        if not self.object_is_alive:
            # This should never happen, since the victim produced this clue
            # when they were alive
            s += "the body of "

        s += f'{self.object} arriving to the {self.place} at {self.time}"'
        return s

    def string_spanish(self):
        s = f'{self.subject} dijo: "Vi '

        if not self.object_is_alive:
            # This should never happen, since the victim produced this clue
            # when they were alive
            s += "el cuerpo de "

        s += f'a {self.object} llegando a {self.place} a las {self.time}"'
        return s

    def is_incriminating(self, killer, victim, place, time):
        if self.subject == killer and self.object == victim:
            return True
        return False

    def manipulate(self, killer, victim, alibi_place):
        if self.subject == killer and self.object == victim:
            return SawVictimWhenLeavingClue(
                self.subject, self.object, self.object_is_alive, alibi_place, self.time
            )
        raise ValueError("Invalid manipulation: " + str(self))


class SawVictimWhenLeavingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()

    def string_english(self):
        s = f'{self.subject} said: "I saw {self.object} leaving the {self.place} at {self.time}"'
        return s

    def string_spanish(self):
        s = f'{self.subject} dijo: "Vi a {self.object} yendose de {self.place} a las {self.time}"'
        return s

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class SawWhenLeavingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()

    def string_english(self):
        object = self.object
        r = randint(0, 2)
        s = f'{self.subject} said "'

        if object == "$NOBODY":
            r = 0

        if r == 0:
            s += "I saw "
        elif r == 1:
            s += "I noticed "
        elif r == 2:
            s += "I spotted "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not self.object_is_alive:
            s += "the body of "

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "somebody"

        s += f'{object} when I was leaving the {self.place} at {self.time}"'
        return s

    def string_spanish(self):
        object = self.object
        r = randint(0, 2)
        s = f'{self.subject} dijo "'

        if r == 0:
            if object == "$NOBODY":
                s += "No vi "
            else:
                s += "Vi "
        elif r == 1:
            if object == "$NOBODY":
                s += "No noté "
            else:
                s += "Noté "
        elif r == 2:
            if object == "$NOBODY":
                s += "No recuerdo haber visto "
            else:
                s += "Recuerdo haber visto "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not self.object_is_alive:
            s += "el cuerpo de "
        else:
            s += "a "

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "alguien"

        s += f'{object} cuando me fui de {self.place} a las {self.time}"'
        return s

    def is_incriminating(self, killer, victim, place, time):
        if self.subject == killer and self.object == victim:
            return True
        return False

    def manipulate(self, killer, victim, alibi_place):
        if self.subject == killer and self.object == victim:
            if not self.object_is_alive:
                # If the body was seen, it is too suspicious to change
                return None

            # r = randint(0, 1)
            # if r == 0:
            self.object = "$NOBODY"
            # elif r == 1:
            self.place = alibi_place

            return self
        raise ValueError("Invalid manipulation: " + str(self))


class NotSawWhenLeavingClue(AbstractClue):
    def __init__(self, subject, object, place, time):
        self.subject = subject
        self.object = object
        self.place = place
        self.time = time
        super().__init__()

    def string_spanish(self):
        r = randint(0, 2)
        s = f'{self.subject} dijo: "'

        if r == 0:
            s += ""
        elif r == 1:
            s += "Recuerdo que "
        elif r == 2:
            s += "Estoy seguro que "
        else:
            raise ValueError("Invalid random number: " + str(r))

        s += f'{self.object} no estaba conmigo en {self.place} a las {self.time}"'
        return s

    def string_english(self):
        r = randint(0, 2)
        s = f'{self.subject} said: "'

        if r == 0:
            s += ""
        elif r == 1:
            s += "I think "
        elif r == 2:
            s += "I'm sure "
        else:
            raise ValueError("Invalid random number: " + str(r))

        s += f'{self.object} was not with me in the {self.place} at {self.time}"'
        return s

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WasMurderedClue(AbstractClue):
    def __init__(self, victim, place, time):
        self.subject = None
        self.object = victim
        self.object_is_alive = False
        self.place = place
        self.time = time
        super().__init__()

    def string_spanish(self):
        raise ValueError("Not implemented")

    def string_english(self):
        raise ValueError("Not implemented")

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WasMurderedInitialClue(AbstractClue):
    time_start = None
    time_end = None

    def __init__(self, victim, place, time_start, time_end):
        self.subject = victim
        self.object = place
        self.object_is_alive = True
        self.place = place
        self.time_start = time_start
        self.time_end = time_end
        super().__init__()

    def string_spanish(self):
        return f"{self.subject} fue asesinado en {self.object} en algún momento entre las {self.time_start} y las {self.time_end}"

    def string_english(self):
        return f"{self.subject} was murdered in the {self.object} at some time between {self.time_start} and {self.time_end}"

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WasMurderedInspectionClue(AbstractClue):
    time1 = None
    time2 = None

    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        super().__init__()

    def string_spanish(self):
        return f"Un examen minucioso del cuerpo revela que el asesinato tuvo lugar a las {self.time1} o las {self.time2}"

    def string_english(self):
        return f"A close examination of the body reveals that the murder took place either at {self.time1} or at {self.time2}"

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))

class WasMurderedAutopsyClue(AbstractClue):
    time1 = None
    time2 = None

    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        super().__init__()

    def string_spanish(self):
        return f"Un grito espeluznante de la víctima se escuchó a las {self.time1} o a las {self.time2}"

    def string_english(self):
        return f"A blood-curdling scream of the victim was heard either at {self.time1} or at {self.time2}"

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))

class PoliceArrivedClue(AbstractClue):
    def __init__(self, time):
        self.time = time
        super().__init__()

    def string_spanish(self):
        raise ValueError("Not implemented")

    def string_english(self):
        raise ValueError("Not implemented")

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class EvidenceClue(AbstractClue):
    def __init__(self, subject, place):
        self.subject = subject
        self.place = place
        super().__init__()

    def string_spanish(self):
        r = randint(0, 2)

        if r == 0:
            return f"Una pisada reciente, compatible con el calzado de {self.subject} fue encontrada en {self.place}"
        elif r == 1:
            return f"Una huella digital de {self.subject} fue identificada {self.place}. Se ve muy reciente"
        elif r == 2:
            return f"Un hebra de pelo de {self.subject} fue encontrada en {self.place} indicando que estuvo reciente ahí"
        else:
            raise ValueError("Invalid random number: " + str(r))

    def string_english(self):
        r = randint(0, 2)

        if r == 0:
            return f"A recent footstep matching {self.subject} shoes was found in the {self.place}"
        elif r == 1:
            return f"A fingerprint of {self.subject} was found in the {self.place}. It looks very fresh"
        elif r == 2:
            return f"A strand of hair matching {self.subject} was found in the {self.place}, indicating that they were recently there"
        else:
            raise ValueError("Invalid random number: " + str(r))

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))

class StayedClue(AbstractClue):
    def __init__(self, subject, place, time_start, time_end):
        self.subject = subject
        self.object = place
        self.place = place
        self.time_start = time_start
        self.time_end = time_end
        super().__init__()

    def string_spanish(self):
        r = randint(0, 3)

        if r == 0:
            return f'{self.subject} dijo: "Estuve en {self.place} desde las {self.time_start} hasta las {self.time_end}"'
        elif r == 1:
            return f'{self.subject} dijo: "Me quedé en {self.place} desde las {self.time_start} hasta las {self.time_end}"'
        elif r == 2:
            return f'"Estuve en {self.place} desde las {self.time_start} hasta las {self.time_end}" afirmó {self.subject}'
        elif r == 3:
            return f'"Estuve en {self.place} desde las {self.time_start} hasta las {self.time_end}" aseguró {self.subject}'
        else:
            raise ValueError("Invalid random number: " + str(r))

    def string_english(self):
        r = randint(0, 2)

        if r == 0:
            return f'{self.subject} said: "I was in the {self.place} from {self.time_start} to {self.time_end}"'
        elif r == 1:
            return f'"I was in the {self.place} from {self.time_start} to {self.time_end}" stated {self.subject}'
        elif r == 2:
            return f'"I stayed in the {self.place} from {self.time_start} to {self.time_end}" claimed {self.subject}'
        else:
            raise ValueError("Invalid random number: " + str(r))

    def is_incriminating(self, killer, victim, place, time):
        if (
            self.subject == killer
            and self.place == place
            and self.time_start.seconds <= time.seconds
            and self.time_end.seconds >= time.seconds
        ):
            return True
        return False

    def manipulate(self, killer, victim, alibi_place):
        self.place = alibi_place
        return self

class InteractedClue(AbstractClue):
    def __init__(self, subject0, subject1, place, time):
        self.subject0 = subject0
        self.subject1 = subject1
        self.place = place
        self.time = time
        super().__init__()

    def string_spanish(self):
        return f'{self.subject0} dijo: "Hablé con {self.subject1} en {self.place}"'

    def string_english(self):
        r = randint(0, 2)
        if r == 0:
            return f'{self.subject0} said: "I talked with {self.subject1} in the {self.place}"'
        elif r == 1:
            return f'"I talked with {self.subject1} in the {self.place}" said {self.subject0}'
        elif r == 2:
            return f'{self.subject0} said: "I chatted with {self.subject1} in the {self.place}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

    def is_incriminating(self, killer, victim, place, time):
        if (
            self.subject0 == killer
            and self.subject1 == victim
            and self.place == place
            and self.time.seconds <= time.seconds
        ):
            return True
        return False

    def manipulate(self, killer, victim, alibi_place):
        return None # This clue is not incriminating to lie, just omitting information

class HeardClue(AbstractClue):
    def __init__(self, subject, activity, time):
        self.subject = subject
        self.activity = activity
        assert "en" in activity and "es" in activity
        self.time = time
        super().__init__()


    def string_spanish(self):
        r = randint(0, 1)

        if r == 0:
            return f'{self.subject} dijo: "Yo {self.activity["es"]} a las {self.time}"'
        elif r == 1:
            return f'"Yo {self.activity["es"]} a las {self.time}" afirmó {self.subject}'
        else:
            raise ValueError("Invalid random number: " + str(r))

    def string_english(self):
        r = randint(0, 1)

        if r == 0:
            return f'{self.subject} said: "I {self.activity["en"]} at {self.time}"'
        elif r == 1:
            return f'"I {self.activity["en"]} at {self.time}" said {self.subject}'
        else:
            raise ValueError("Invalid random number: " + str(r))

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))

class WeaponNotUsedClue(AbstractClue):
    def __init__(self, weapon):
        self.weapon = weapon
        super().__init__()

    def string_spanish(self):
        r = randint(0, 1)
        weapon = self.weapon

        if r == 0:
            s = "Una inspección del cuerpo revela "
        elif r == 1:
            s = "La inspección del cuerpo indica "
        else:
            assert False

        weapon_type = get_weapon_type(weapon)
        if weapon_type == "projectile":
            return s + "que no había orificio de bala."
        elif weapon_type == "strangulation":
            return s + "que no había signos de estrangulamiento."
        elif weapon_type == "sharp force":
            return s + "que no había puñaladas."
        elif weapon_type == "poisoning":
            return s + " que " + weapon + " no era el arma homicida."
        elif weapon_type == "blunt force":
            return s + " que no había signos de una contusión mortal."
        else:
            raise ValueError("Unknown type of weapon: " + weapon)

    def string_english(self):
        r = randint(0, 1)
        weapon = self.weapon

        if r == 0:
            s = "Inspecting the body reveals "
        elif r == 1:
            s = "The inspection of the body indicates "
        else:
            raise ValueError("Invalid random number: " + str(r))

        weapon_type = get_weapon_type(weapon)
        if weapon_type == "projectile":
            return s + "there are no projectile holes."
        elif weapon_type == "strangulation":
            return s + "no signs of strangulation."
        elif weapon_type == "sharp force":
            return s + "no signs of stabbing."
        elif weapon_type == "poisoning":
            return s + " that the " + weapon + " was not the murderer weapon."
        elif weapon_type == "blunt force":
            return s + " no signs of contusion."
        else:
            raise ValueError("Unknown type of weapon: " + weapon)


def create_clue(call):
    if call[0] == "SawWhenArriving":
        assert len(call) == 6
        return SawWhenArrivingClue(call[1], call[2], call[3], call[4], call[5])
    elif call[0] == "NotSawWhenArriving":
        assert len(call) == 5
        return NotSawWhenArrivingLeavingClue(call[1], call[2], call[3], call[4])
    elif call[0] == "SawVictimWhenArriving":
        assert len(call) == 6
        return SawVictimWhenArrivingClue(call[1], call[2], call[3], call[4], call[5])
    elif call[0] == "SawVictimWhenLeaving":
        assert len(call) == 6
        return SawVictimWhenLeavingClue(call[1], call[2], call[3], call[4], call[5])
    elif call[0] == "SawWhenLeaving":
        assert len(call) == 6
        return SawWhenLeavingClue(call[1], call[2], call[3], call[4], call[5])
    elif call[0] == "NotSawWhenLeaving":
        assert len(call) == 5
        return NotSawWhenArrivingLeavingClue(call[1], call[2], call[3], call[4])
    elif call[0] == "WasMurdered":
        assert len(call) == 4
        return WasMurderedClue(call[1], call[2], call[3])
    elif call[0] == "WasMurderedInitial":
        assert len(call) == 5
        return WasMurderedInitialClue(call[1], call[2], call[3], call[4])
    elif call[0] == "WasMurderedInspection":
        assert len(call) == 3
        return WasMurderedInspectionClue(call[1], call[2])
    elif call[0] == "WasMurderedAutopsy":
        assert len(call) == 3
        return WasMurderedAutopsyClue(call[1], call[2])
    elif call[0] == "PoliceArrived":
        assert len(call) == 2
        return PoliceArrivedClue(call[1])
    elif call[0] == "Stayed":
        assert len(call) == 5
        return StayedClue(call[1], call[2], call[3], call[4])
    elif call[0] == "Interacted":
        assert len(call) == 5
        return InteractedClue(call[1], call[2], call[3], call[4])
    elif call[0] == "Evidence":
        assert len(call) == 3
        return EvidenceClue(call[1], call[2])

    # Heard is missing
    else:
        raise ValueError("Invalid clue!: " + str(call))

from abc import ABC, abstractmethod
from random import randint, choice

from mystery_o_matic.weapons import get_weapon_type
from mystery_o_matic.time import Time  # parse_time


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
        return {'en': self.string_english(), 'es': self.string_spanish()}

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
    def __init__(self, weapon, place):
        self.place = place
        self.weapon = weapon
    def string_english(self):
        return "The {} from the ${}".format(self.weapon, self.place)

    def string_spanish(self):
        return "{} en ${}".format(self.weapon, self.place)

class CharacterLocationStatement(AbstractStatement):
    def __init__(self, subject, place):
        self.subject = subject
        self.place = place

    def string_english(self):
        return "{} was in the {}".format(self.subject, self.place)

    def string_spanish(self):
        return "{} estaba en {}".format(self.subject, self.place)

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

class FinalLocationsIntroStatement(AbstractStatement):
    def __init__(self, time):
        self.time = time

    def string_english(self):
        return "When you arrived at {}:\n".format(self.time)

    def string_spanish(self):
        return "Cuando llegaste, a las {}:\n".format(self.time)

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
        return {'en': self.string_english(), 'es': self.string_spanish()}

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
        str = '{} said "'

        if object == "$NOBODY":
            r = 0

        if r == 0:
            str += "I saw "
        elif r == 1:
            str += "I noticed "
        elif r == 2:
            str += "I spotted "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not self.object_is_alive:
            str += "the body of "

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "somebody"

        str += '{} when I arrived to the {} at {}"'
        return str.format(self.subject, object, self.place, self.time)

    def string_spanish(self):
        object = self.object
        r = randint(0, 2)
        str = '{} dijo "'

        if r == 0:
            if object == "$NOBODY":
                str += "No vi "
            else:
                str += "Vi "
        elif r == 1:
            if object == "$NOBODY":
                str += "No noté "
            else:
                str += "Noté "
        elif r == 2:
            if object == "$NOBODY":
                str += "No distinguí "
            else:
                str += "Distinguí "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not self.object_is_alive:
            str += "el cuerpo de "

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "alguien"

        str += 'a {} cuando llegaba a {} a las {}"'
        return str.format(self.subject, object, self.place, self.time)

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
        str = '{} dijo: "No recuerdo que {} estuviese conmigo en {} a las {}"'
        return str.format(self.subject, self.object, self.place, self.time)

    def string_english(self):
        r = randint(0, 2)
        str = '{} said: "'

        if r == 0:
            str += ""
        elif r == 1:
            str += "I think "
        elif r == 2:
            str += "I'm sure "
        else:
            raise ValueError("Invalid random number: " + str(r))

        str += '{} was not with me in the {} at {}"'
        return str.format(self.subject, self.object, self.place, self.time)

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
        str = '{} said: "I saw '
        if not self.object_is_alive:
            # This should never happen, since the victim produced this clue
            # when they were alive
            str += "the body of "

        str += '{} arriving to the {} at {}"'
        return str.format(self.subject, self.object, self.place, self.time)

    def string_spanish(self):
        str = '{} dijo: "Vi '

        if not self.object_is_alive:
            # This should never happen, since the victim produced this clue
            # when they were alive
            str += "el cuerpo de "

        str += 'a {} llegando a {} a las {}"'
        return str.format(self.subject, self.object, self.place, self.time)

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
        str = '{} said: "I saw '
        str += '{} leaving the {} at {}"'
        return str.format(self.subject, self.object, self.place, self.time)

    def string_spanish(self):
        str = '{} dijo: "Vi a {} yendose de {} a las {}"'
        return str.format(self.subject, self.object, self.place, self.time)

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
        str = '{} said "'

        if object == "$NOBODY":
            r = 0

        if r == 0:
            str += "I saw "
        elif r == 1:
            str += "I noticed "
        elif r == 2:
            str += "I spotted "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not self.object_is_alive:
            str += "the body of "

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "somebody"

        str += '{} when I was leaving the {} at {}"'
        return str.format(self.subject, object, self.place, self.time)

    def string_spanish(self):
        object = self.object
        r = randint(0, 2)
        str = '{} dijo "'

        if r == 0:
            if object == "$NOBODY":
                str += "No vi "
            else:
                str += "Vi "
        elif r == 1:
            if object == "$NOBODY":
                str += "No noté "
            else:
                str += "Noté "
        elif r == 2:
            if object == "$NOBODY":
                str += "No recuerdo "
            else:
                str += "Recuerdo "
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not self.object_is_alive:
            str += "el cuerpo de "

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "alguien"

        str += 'a {} cuando me iba de {} a las {}"'
        return str.format(self.subject, object, self.place, self.time)

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
        str = '{} dijo: "'

        if r == 0:
            str += ""
        elif r == 1:
            str += "Recuerdo que "
        elif r == 2:
            str += "Estoy seguro que "
        else:
            raise ValueError("Invalid random number: " + str(r))

        str += '{} no estaba conmigo en {} a las {}"'
        return str.format(self.subject, self.object, self.place, self.time)

    def string_english(self):
        r = randint(0, 2)
        str = '{} said: "'

        if r == 0:
            str += ""
        elif r == 1:
            str += "I think "
        elif r == 2:
            str += "I'm sure "
        else:
            raise ValueError("Invalid random number: " + str(r))

        str += '{} was not with me in the {} at {}"'
        return str.format(self.subject, self.object, self.place, self.time)

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
        return "{} fue asesinado en {} en algún momento entre las {} y las {}".format(
            self.subject, self.object, self.time_start, self.time_end
        )

    def string_english(self):
        return "{} was murdered in the {} at some time between {} and {}".format(
            self.subject, self.object, self.time_start, self.time_end
        )

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
        return "Un examen minusioso del cuerpo revela que el asesinato tuvo lugar a las {} o las {}".format(
            self.time1, self.time2
        )

    def string_english(self):
        return "A close examination of the body reveals that the murder took place either at {} or at {}".format(
            self.time1, self.time2
        )

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
        return "Un grito espeluznante de la víctima se escuchó a las {} o a las {}".format(
            self.time1, self.time2
        )

    def string_english(self):
        return "A blood-curdling scream of the victim was heard either at {} or at {}".format(
            self.time1, self.time2
        )

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
            return "Una pisada reciente, compatible con el calzado de {} fue encontrada en {}".format(
                self.subject, self.place
            )
        elif r == 1:
            return (
                "Una huella digital de {} fue identificada {}. Se ve muy reciente".format(
                    self.subject, self.place
                )
            )
        elif r == 2:
            return "Un hebra de pelo de {} fue encontrada en {} indicando que estuvo reciente ahí".format(
                self.subject, self.place
            )
        else:
            raise ValueError("Invalid random number: " + str(r))

    def string_english(self):
        r = randint(0, 2)

        if r == 0:
            return "A recent footstep matching {} shoes was found in the {}".format(
                self.subject, self.place
            )
        elif r == 1:
            return (
                "A fingerprint of {} was found in the {}. It looks very fresh".format(
                    self.subject, self.place
                )
            )
        elif r == 2:
            return "A strand of hair matching {} was found in the {}, indicating that they were recently in that place".format(
                self.subject, self.place
            )
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
            str = '{} dijo: "Estuve en {} desde las {} hasta las {}"'
            return str.format(self.subject, self.place, self.time_start, self.time_end)
        elif r == 1:
            str = '{} dijo: "Me quedé en {} desde las {} hasta las {}"'
            return str.format(self.subject, self.place, self.time_start, self.time_end)
        elif r == 2:
            str = '"Estuve en {} desde las {} hasta las {}" afirmó {}'
            return str.format(self.place, self.time_start, self.time_end, self.subject)
        elif r == 3:
            str = '"Estuve en {} desde las {} hasta las {}" aseguró {}'
            return str.format(self.place, self.time_start, self.time_end, self.subject)
        else:
            raise ValueError("Invalid random number: " + str(r))

    def string_english(self):
        r = randint(0, 2)

        if r == 0:
            str = '{} said: "I was in the {} from {} to {}"'
            return str.format(self.subject, self.place, self.time_start, self.time_end)
        elif r == 1:
            str = '"I was in the {} from {} to {}" stated {}'
            return str.format(self.place, self.time_start, self.time_end, self.subject)
        elif r == 2:
            str = '"I stayed in the {} from {} to {}" claimed {}'
            return str.format(self.place, self.time_start, self.time_end, self.subject)
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
            str = '{} dijo: "Yo {} a las {}"'
            return str.format(self.subject, self.activity["es"], self.time)
        elif r == 1:
            str = '"Yo {} a las {}" afirmó {}'
            return str.format(self.activity["es"], self.time, self.subject)
        else:
            raise ValueError("Invalid random number: " + str(r))

    def string_english(self):
        r = randint(0, 1)

        if r == 0:
            str = '{} said: "I {} at {}"'
            return str.format(self.subject, self.activity["en"], self.time)
        elif r == 1:
            str = '"I {} at {}" said {}'
            return str.format(self.activity["en"], self.time, self.subject)
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
            str = "Una inspección del cuerpo revela "
        elif r == 1:
            str = "La inspección del cuerpo indica "
        else:
            assert False

        weapon_type = get_weapon_type(weapon)
        if weapon_type == "projectile":
            return str + "que no había orificio de bala."
        elif weapon_type == "strangulation":
            return str + "que no había signos de estrangulamiento."
        elif weapon_type == "sharp force":
            return str + "que no había puñaladas."
        elif weapon_type == "poisoning":
            return str + " que " + weapon + " no era el arma homicida."
        elif weapon_type == "blunt force":
            return str + " que no había signos de una contusión mortal."
        else:
            raise ValueError("Unknown type of weapon: " + weapon)

    def string_english(self):
        r = randint(0, 1)
        weapon = self.weapon

        if r == 0:
            str = "Inspecting the body reveals "
        elif r == 1:
            str = "The inspection of the body indicates "
        else:
            raise ValueError("Invalid random number: " + str(r))

        weapon_type = get_weapon_type(weapon)
        if weapon_type == "projectile":
            return str + "there are no projectile holes."
        elif weapon_type == "strangulation":
            return str + "no signs of strangulation."
        elif weapon_type == "sharp force":
            return str + "no signs of stabbing."
        elif weapon_type == "poisoning":
            return str + " that the " + weapon + " was not the murderer weapon."
        elif weapon_type == "blunt force":
            return str + " no signs of contusion."
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
    elif call[0] == "Evidence":
        assert len(call) == 3
        return EvidenceClue(call[1], call[2])

    # Heard is missing
    else:
        raise ValueError("Invalid clue!: " + str(call))

from abc import ABC, abstractmethod
from random import randint, choice

from mystery_o_matic.weapons import get_weapon_type
from mystery_o_matic.time import Time


class AbstractStatement(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def string_english(self):
        return ""

    @abstractmethod
    def string_spanish(self):
        return ""

    @abstractmethod
    def string_russian(self):
        return ""

    def string(self):
        return {"en": self.string_english(), "es": self.string_spanish(), "ru": self.string_russian()}


class MurderWasAloneStatement(AbstractStatement):
    def string_english(self):
        return "The murderer was alone with their victim, and the body remained unmoved"

    def string_spanish(self):
        return "El asesino estaba a solas con la víctima y el cuerpo no se movió"

    def string_russian(self):
        return "Убийца был(а) наедине с жертвой, и тело осталось на месте"


class MurderWasNotFoundWithBodyStatement(AbstractStatement):
    def string_english(self):
        return "The murderer wasn't caught with the body"

    def string_spanish(self):
        return "El asesino no fue encontrado con el cuerpo"

    def string_russian(self):
        return "Убийцу не застали рядом с телом"


class WeaponLocationStatement(AbstractStatement):
    def __init__(self, weapon, vplace):
        self.vplace = vplace
        self.weapon = weapon

    def string_english(self):
        return f"The {self.weapon} from the {self.vplace}"

    def string_spanish(self):
        return f"{self.weapon} en {self.vplace}"

    def string_russian(self):
        return f"{self.weapon} — {self.vplace}"


class CharacterLocationStatement(AbstractStatement):
    def __init__(self, subject, place, victim):
        self.subject = subject
        self.victim = victim
        self.place = place

    def string_english(self):
        if self.subject == self.victim:
            return f"{self.subject}'s body was in the {self.place}"
        else:
            return f"{self.subject} was in the {self.place}"

    def string_spanish(self):
        if self.subject == self.victim:
            return f"El cuerpo de {self.subject} estaba en {self.place}"
        else:
            return f"{self.subject} estaba en {self.place}"

    def string_russian(self):
        if self.subject == self.victim:
            return f"Тело {self.subject} находилось в {self.place}_LOC"
        else:
            return f"{self.subject} находился(ась) в {self.place}_LOC"


class NoOneElseStatement(AbstractStatement):
    def string_english(self):
        return "No one else was present in the location."

    def string_spanish(self):
        return "No había nadie más en el lugar"

    def string_russian(self):
        return "В этом месте больше никого не было."


class WeaponLocationsIntroStatement(AbstractStatement):
    def string_english(self):
        return "The killer retrieved the murder weapon from one of these places:\n"

    def string_spanish(self):
        return (
            "El asesino consiguió el arma homicida de uno de los siguientes lugares:\n"
        )

    def string_russian(self):
        return "Убийца взял(а) орудие убийства из одного из следующих мест:\n"


class WeaponLocationsOutroStatement(AbstractStatement):
    def string_english(self):
        return "No one saw the killer retrieving the murder weapon"

    def string_spanish(self):
        return "Nadie vió al asesino tomar el arma homicida"

    def string_russian(self):
        return "Никто не видел, как убийца брал(а) орудие убийства"


class FinalLocationsIntroStatement(AbstractStatement):
    def __init__(self, time):
        self.time = time

    def string_english(self):
        return f"We know where everyone was at {self.time}:\n"

    def string_spanish(self):
        return f"Sabemos donde estaban todos a las {self.time}:\n"

    def string_russian(self):
        return f"Нам известно, где находился(ась) каждый(ая) в {self.time}:\n"


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

    @abstractmethod
    def string_russian(self):
        return ""

    def string(self):
        return {"en": self.string_english(), "es": self.string_spanish(), "ru": self.string_russian()}


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
        s = f'{self.subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'The {self.place} was empty when I arrived at {self.time}"'
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

        if not self.object_is_alive:
            return f'{self.subject}: "I was horrified to discover {self.object}\'s body when I arrived at the {self.place} at {self.time}"'

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "somebody"

        s += f'{object} when I arrived at the {self.place} at {self.time}"'
        return s

    def string_spanish(self):
        object = self.object
        r = randint(0, 2)
        s = f'{self.subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'{self.place} estaba vacío cuando llegué a las {self.time}"'
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

        if not self.object_is_alive:
            return f'{self.subject}: "Me horroricé al descubrir el cuerpo de {self.object} cuando llegué a {self.place} a las {self.time}"'

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "alguien"

        s += f'a {object} cuando llegué a {self.place} a las {self.time}"'
        return s

    def string_russian(self):
        object = self.object
        r = randint(0, 2)
        s = f'{self.subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'В {self.place}_LOC никого не было, когда я пришёл(ла) в {self.time}"'
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

        if not self.object_is_alive:
            return f'{self.subject}: "Я был(а) потрясён(а), обнаружив тело {self.object}, когда я пришёл(ла) в {self.place}_LOC в {self.time}"'

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "кого-то"

        s += f'{object}, когда я пришёл(ла) в {self.place}_LOC в {self.time}"'
        return s

    def is_incriminating(self, killer, victim, place, time):
        if self.subject == killer and self.object == victim:
            return True
        if (
            self.subject == killer
            and self.place == place
            and self.time.seconds <= time.seconds
        ):
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
        return None
        raise ValueError("Invalid manipulation: " + str(self))


class NotSawWhenArrivingLeavingClue(AbstractClue):
    def __init__(self, subject, object, place, time, mode):
        self.subject = subject
        self.object = object
        self.place = place
        self.time = time
        self.mode = mode
        super().__init__()

    def string_spanish(self):
        r = randint(0, 5)
        s = f'{self.subject}: "'

        if r == 0:
            s += f'Estoy seguro de que {self.object} no estaba conmigo en {self.place} a las {self.time}"'
        elif r == 1:
            s += f'Estuve en {self.place} a las {self.time} pero {self.object} no estaba por ahí"'
        elif r == 2:
            s += f'{self.object} definitivamente no estaba conmigo en {self.place} a las {self.time}"'
        elif r == 3:
            s += f'{self.object} no estaba conmigo en {self.place} a las {self.time}"'
        elif r == 4:
            s += f'Mientras estaba en {self.place} a las {self.time}, {self.object} no se veía por ningún lado"'
        elif r == 5:
            s += f'Estuve en {self.place} a las {self.time} pero {self.object} no estaba ahí conmigo"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def string_russian(self):
        r = randint(0, 5)
        s = f'{self.subject}: "'

        if r == 0:
            s += f'Уверен(а), что {self.object} не было рядом со мной в {self.place}_LOC в {self.time}"'
        elif r == 1:
            s += f'Я был(а) в {self.place}_LOC в {self.time}, но {self.object} там не было"'
        elif r == 2:
            s += f'{self.object} точно не было рядом со мной в {self.place}_LOC в {self.time}"'
        elif r == 3:
            s += f'{self.object} не было со мной в {self.place}_LOC в {self.time}"'
        elif r == 4:
            s += f'Пока я был(а) в {self.place}_LOC в {self.time}, {self.object} нигде не было видно"'
        elif r == 5:
            s += f'Я был(а) в {self.place}_LOC в {self.time}, но {self.object} не было рядом"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def string_english(self):
        r = randint(0, 5)
        s = f'{self.subject}: "'

        if r == 0:
            s += f'I\'m sure {self.object} was not with me in the {self.place} at {self.time}"'
        elif r == 1:
            s += f'I was in the {self.place} at {self.time} but {self.object} wasn\'t around."'
        elif r == 2:
            s += f'{self.object} definitely was not with me in the {self.place} at {self.time}"'
        elif r == 3:
            s += f'{self.object} was not with me in the {self.place} at {self.time}"'
        elif r == 4:
            s += f'While I was in the {self.place} at {self.time}, {self.object} was nowhere to be seen."'
        elif r == 5:
            s += f'I was in the {self.place} at {self.time} but {self.object} was not there with me."'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def is_incriminating(self, killer, victim, place, time):
        # The subject is revealing that the object was not with them
        # so if the subject is the killer, the place is the crime scene
        if self.subject == killer and self.place == place:
            if self.mode == "arriving":
                # Arriving before the crime is incriminating
                return self.time.seconds <= time.seconds
            elif self.mode == "leaving":
                # Leaving after the crime is incriminating
                return self.time.seconds >= time.seconds
            else:
                raise ValueError("Invalid mode: " + self.mode)

        return False

    def manipulate(self, killer, victim, alibi_place):
        # we could manipulate this clue, but it will produce many false statements from the killer
        # which will be much easier to detect
        return None


class SawVictimWhenArrivingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()

    def string_english(self):
        r = randint(0, 2)
        s = f'{self.subject}: "'
        verb = None

        # Introduce verbs
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
            s += f'{verb.capitalize()} {self.object} arriving while I was in the {self.place} at {self.time}"'
        elif r == 1:
            s += f'I was in the {self.place} when {verb} {self.object} arriving at {self.time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def string_spanish(self):
        r = randint(0, 2)
        s = f'{self.subject}: "'
        verb = None

        if r == 0:
            verb = "vi"
        elif r == 1:
            verb = "noté"
        elif r == 2:
            verb = "divisé"
        else:
            raise ValueError("Invalid random number: " + str(r))

        if not self.object_is_alive:
            s += "el cuerpo de "

        r = randint(0, 1)
        if r == 0:
            s += f'{verb.capitalize()} a {self.object} llegando mientras estaba en {self.place} a las {self.time}"'
        elif r == 1:
            s += f'Estaba en {self.place} cuando {verb} a {self.object} llegando a las {self.time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def string_russian(self):
        r = randint(0, 2)
        s = f'{self.subject}: "'
        verb = None

        if r == 0:
            verb = "увидел(а)"
        elif r == 1:
            verb = "заметил(а)"
        elif r == 2:
            verb = "разглядел(а)"
        else:
            raise ValueError("Invalid random number: " + str(r))

        if self.object_is_alive:
            object_phrase = f"{self.object} прибывающим(ей)"
        else:
            object_phrase = f"тело {self.object} прибывшим(ей)"

        r = randint(0, 1)
        if r == 0:
            s += f'{verb.capitalize()} {object_phrase} в {self.place}_LOC в {self.time}"'
        elif r == 1:
            s += f'Я был(а) в {self.place}_LOC, когда {verb} {object_phrase} в {self.time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def is_incriminating(self, killer, victim, place, time):
        if self.subject == killer and self.object == victim and self.place == place:
            return True
        return False

    def manipulate(self, killer, victim, alibi_place):
        return None  # Too risky to manipulate this clue


class SawVictimWhenLeavingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()

    def string_english(self):
        r = randint(0, 2)
        s = f'{self.subject}: "'
        verb = None

        # Introduce verbs
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
            s += f'{verb.capitalize()} {self.object} leaving while I was in the {self.place} at {self.time}"'
        elif r == 1:
            s += f'I was in the {self.place} when {verb} {self.object} leaving at {self.time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def string_spanish(self):
        r = randint(0, 2)
        s = f'{self.subject}: "'
        verb = None

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
            s += f'{verb.capitalize()} a {self.object} yéndose mientras estaba en {self.place} a las {self.time}"'
        elif r == 1:
            s += f'Estaba en {self.place} cuando {verb} a {self.object} yéndose a las {self.time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def string_russian(self):
        r = randint(0, 2)
        s = f'{self.subject}: "'
        verb = None

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
            s += f'{verb.capitalize()} уходящего(ую) {self.object} из {self.place}_GEN в {self.time}"'
        elif r == 1:
            s += f'Я был(а) в {self.place}_LOC, когда {verb} {self.object} уходящим(ей) в {self.time}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

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
        s = f'{self.subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'The {self.place} was empty when I left it at {self.time}"'
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

        if not self.object_is_alive:
            s = f'{self.subject}: "I was shocked to see the body of '

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "somebody"

        s += f'{object} when I was leaving the {self.place} at {self.time}"'
        return s

    def string_spanish(self):
        object = self.object
        r = randint(0, 2)
        s = f'{self.subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'{self.place} estaba vacío cuando me fui a las {self.time}"'
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

        if not self.object_is_alive:
            return f'{self.subject}: "Me impactó ver el cuerpo de {self.object} cuando me iba de {self.place} a las {self.time}"'

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "alguien"

        s += f'a {object} cuando me iba de {self.place} a las {self.time}"'
        return s

    def string_russian(self):
        object = self.object
        r = randint(0, 2)
        s = f'{self.subject}: "'

        if object == "$NOBODY":
            if r > 0:
                s += f'В {self.place}_LOC было пусто, когда я уходил(а) в {self.time}"'
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

        if not self.object_is_alive:
            return f'{self.subject}: "Я был(а) потрясён(а), увидев тело {self.object} в {self.place}_LOC в {self.time}"'

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "кого-то"

        s += f'{object}, уходя из {self.place}_GEN в {self.time}"'
        return s

    def is_incriminating(self, killer, victim, place, time):
        if self.subject == killer and self.object == victim:
            return True
        return False

    def manipulate(self, killer, victim, alibi_place):
        return None  # Too risky to manipulate this clue


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

    def string_russian(self):
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

    def string_russian(self):
        return f"{self.subject} был(а) убит(а) в {self.object}_LOC в промежуток между {self.time_start} и {self.time_end}"

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WasMurderedBodyTwoOptionsClue(AbstractClue):
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

    def string_russian(self):
        return f"Тщательный осмотр тела показывает, что убийство произошло в {self.time1} или в {self.time2}"

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WasVictimDeadAtClue(AbstractClue):  # UNUSED
    time = Time(0)
    alternative = False

    def __init__(self, time, alternative):
        self.time = time
        self.alternative = alternative
        super().__init__()

    def string_spanish(self):
        if self.alternative:
            r = "Inspeccionando la escena del crimen se revela que la víctima estaba muerta a las "
        else:
            r = "Un examen minucioso del cuerpo revela que la víctima estaba muerta a las "

        r += f"{self.time}"
        return r

    def string_english(self):
        if self.alternative:
            r = "Inspecting the crime scene reveals that the victim had been dead by "
        else:
            r = "A close examination of the body reveals that the victim had been dead by "

        r += f"{self.time}"
        return r

    def string_russian(self):
        if self.alternative:
            r = "Осмотр места преступления показывает, что жертва была мертва к "
        else:
            r = "Тщательный осмотр тела показывает, что жертва была мертва к "

        r += f"{self.time}"
        return r

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WasVictimAliveAtClue(AbstractClue):
    time = Time(0)
    alternative = False

    def __init__(self, time, alternative):
        self.time = time
        self.alternative = alternative
        super().__init__()

    def string_spanish(self):
        if self.alternative:
            r = "Inspeccionando la escena del crimen se revela que la víctima estaba viva a las "
        else:
            r = "Un examen minucioso del cuerpo revela que la víctima estaba viva a las "

        r += f"{self.time}"
        return r

    def string_english(self):
        if self.alternative:
            r = "Inspecting the crime scene reveals that the victim was alive at "
        else:
            r = "A close examination of the body reveals that the victim was alive at "

        r += f"{self.time}"
        return r

    def string_russian(self):
        if self.alternative:
            r = "Осмотр места преступления показывает, что жертва была жива в "
        else:
            r = "Тщательный осмотр тела показывает, что жертва была жива в "

        r += f"{self.time}"
        return r

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WasMurderedAfterClue(AbstractClue):
    time = Time(0)
    positive = False
    alternative = False

    def __init__(self, time, interval_size, positive, alternative):
        self.time = time
        self.interval_size = interval_size
        self.positive = positive
        self.alternative = alternative
        super().__init__()

    def string_spanish(self):
        if self.alternative:
            r = "Inspeccionando la escena del crimen se revela que el asesinato tuvo lugar "
        else:
            r = "Un examen minucioso del cuerpo revela que el asesinato tuvo lugar "
        if self.positive:
            t = Time(self.time.seconds)
            r += f"después de las {t}"
        else:
            t = Time(self.time.seconds + self.interval_size)
            r += f"no antes de las {t}"

        return r

    def string_english(self):
        if self.alternative:
            r = "Inspecting the crime scene reveals that the victim was murdered "
        else:
            r = "A close examination of the body reveals that the victim was murdered "
        if self.positive:
            t = Time(self.time.seconds)
            r += f"after {t}"
        else:
            t = Time(self.time.seconds + self.interval_size)
            r += f"not before {t}"

        return r

    def string_russian(self):
        if self.alternative:
            r = "Осмотр места преступления показывает, что убийство произошло "
        else:
            r = "Тщательный осмотр тела показывает, что убийство произошло "
        if self.positive:
            t = Time(self.time.seconds)
            r += f"после {t}"
        else:
            t = Time(self.time.seconds + self.interval_size)
            r += f"не раньше {t}"

        return r

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WasMurderedBeforeClue(AbstractClue):
    time = Time(0)
    positive = False
    alternative = False

    def __init__(self, time, interval_size, positive, alternative):
        self.time = time
        self.interval_size = interval_size
        self.positive = positive
        self.alternative = alternative
        super().__init__()

    def string_spanish(self):
        if self.alternative:
            r = "Inspeccionando la escena del crimen se revela que el asesinato tuvo lugar "
        else:
            r = "Un examen minucioso del cuerpo revela que el asesinato tuvo lugar "
        if self.positive:
            t = Time(self.time.seconds)
            r += f"antes de las {t}"
        else:
            t = Time(self.time.seconds + self.interval_size)
            r += f"no después de las {t}"

        return r

    def string_english(self):
        if self.alternative:
            r = "Inspecting the crime scene reveals that the victim was murdered "
        else:
            r = "A close examination of the body reveals that the victim was murdered "

        if self.positive:
            t = Time(self.time.seconds)
            r += f"before {t}"
        else:
            t = Time(self.time.seconds - self.interval_size)
            r += f"not after {t}"

        return r

    def string_russian(self):
        if self.alternative:
            r = "Осмотр места преступления показывает, что убийство произошло "
        else:
            r = "Тщательный осмотр тела показывает, что убийство произошло "

        if self.positive:
            t = Time(self.time.seconds)
            r += f"до {t}"
        else:
            t = Time(self.time.seconds - self.interval_size)
            r += f"не позже {t}"

        return r

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WasMurderedScreamClue(AbstractClue):
    time1 = None
    time2 = None

    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        super().__init__()

    def string_spanish(self):
        return f"Un grito espeluznante de la víctima se escuchó entre las {self.time1} y las {self.time2}"

    def string_english(self):
        return f"A blood-curdling scream from the victim was heard between {self.time1} and {self.time2}"

    def string_russian(self):
        return f"Леденящий кровь крик жертвы был услышан между {self.time1} и {self.time2}"

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

    def string_russian(self):
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
            return f"Una pisada reciente, compatible con el calzado de {self.subject}, fue encontrada en {self.place}"
        elif r == 1:
            return f"Una huella digital de {self.subject} fue identificada en {self.place}. Se ve muy reciente"
        elif r == 2:
            return f"Una hebra de pelo de {self.subject} fue encontrada en {self.place}, indicando que estuvo recientemente ahí"
        else:
            raise ValueError("Invalid random number: " + str(r))

    def string_english(self):
        r = randint(0, 2)

        if r == 0:
            return f"A recent footprint matching {self.subject}'s shoe was found in the {self.place}"
        elif r == 1:
            return f"A fingerprint of {self.subject} was found in the {self.place}. It looks very fresh"
        elif r == 2:
            return f"A strand of hair matching {self.subject} was found in the {self.place}, indicating that they were recently there"
        else:
            raise ValueError("Invalid random number: " + str(r))

    def string_russian(self):
        r = randint(0, 2)

        if r == 0:
            return f"Свежий след обуви, соответствующий следам {self.subject}, был найден в {self.place}_LOC"
        elif r == 1:
            return f"Отпечаток пальца {self.subject} был обнаружен в {self.place}_LOC. Он выглядит совсем свежим"
        elif r == 2:
            return f"Прядь волос, принадлежащая {self.subject}, была найдена в {self.place}_LOC, что указывает на недавнее присутствие"
        else:
            raise ValueError("Invalid random number: " + str(r))

    def is_incriminating(self, killer, victim, place, time):
        # this can be incriminating, but the killer cannot manipulate them
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
        r = randint(0, 2)
        s = f'{self.subject}: "'

        if r == 0:
            s += f'Estuve en {self.place} desde las {self.time_start} hasta las {self.time_end}"'
        elif r == 1:
            s += f'No me moví de {self.place} entre las {self.time_start} y las {self.time_end}"'
        elif r == 2:
            s += f'Me quedé en {self.place} desde las {self.time_start} hasta las {self.time_end}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def string_english(self):
        r = randint(0, 2)
        s = f'{self.subject}: "'
        if r == 0:
            s += f'I was in the {self.place} from {self.time_start} to {self.time_end}"'
        elif r == 1:
            s += f'I did not move from the {self.place} between {self.time_start} and {self.time_end}"'
        elif r == 2:
            s += (
                f'Stayed in the {self.place} from {self.time_start} to {self.time_end}"'
            )
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

    def string_russian(self):
        r = randint(0, 2)
        s = f'{self.subject}: "'
        if r == 0:
            s += f'Я был(а) в {self.place}_LOC с {self.time_start} до {self.time_end}"'
        elif r == 1:
            s += f'Я не двигался(ась) с места в {self.place}_LOC между {self.time_start} и {self.time_end}"'
        elif r == 2:
            s += f'Оставался(ась) в {self.place}_LOC с {self.time_start} до {self.time_end}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

        return s

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
        r = randint(0, 1)
        if r == 0:
            return f'{self.subject0}: "Hablé con {self.subject1} en {self.place}"'
        elif r == 1:
            return f'{self.subject0}: "Charlé con {self.subject1} en {self.place}"'
        else:
            raise ValueError("Invalid random number: " + str(r))

    def string_english(self):
        r = randint(0, 1)
        if r == 0:
            return (
                f'{self.subject0}: "I talked with {self.subject1} in the {self.place}"'
            )
        elif r == 1:
            return (
                f'{self.subject0}: "I chatted with {self.subject1} in the {self.place}"'
            )
        else:
            raise ValueError("Invalid random number: " + str(r))

    def string_russian(self):
        r = randint(0, 1)
        if r == 0:
            return f'{self.subject0}: "Я разговаривал(а) с {self.subject1} в {self.place}_LOC"'
        elif r == 1:
            return f'{self.subject0}: "Я болтал(а) с {self.subject1} в {self.place}_LOC"'
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
        return None  # This clue is not incriminating enough to lie, just omitting information


class HeardClue(AbstractClue):
    def __init__(self, subject, activity, time):
        self.subject = subject
        self.activity = activity
        assert "en" in activity and "es" in activity and "ru" in activity
        self.time = time
        super().__init__()

    def string_spanish(self):
        return f'{self.subject}: "Yo {self.activity["es"]} a las {self.time}"'

    def string_english(self):
        return f'{self.subject}: "I {self.activity["en"]} at {self.time}"'

    def string_russian(self):
        return f'{self.subject}: "Я {self.activity["ru"]} в {self.time}"'

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WeaponNotUsedClue(AbstractClue):
    def __init__(self, weapon):
        self.weapon = weapon
        super().__init__()

    def string_spanish(self):
        r = randint(0, 2)
        weapon = self.weapon

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

    def string_english(self):
        r = randint(0, 2)
        weapon = self.weapon

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

    def string_russian(self):
        r = randint(0, 2)
        weapon = self.weapon

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


def create_clue(call):
    if call[0] == "SawWhenArriving":
        assert len(call) == 6
        return SawWhenArrivingClue(call[1], call[2], call[3], call[4], call[5])
    elif call[0] == "NotSawWhenArriving":
        assert len(call) == 5
        return NotSawWhenArrivingLeavingClue(
            call[1], call[2], call[3], call[4], "arriving"
        )
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
        return NotSawWhenArrivingLeavingClue(
            call[1], call[2], call[3], call[4], "leaving"
        )
    elif call[0] == "WasMurdered":
        assert len(call) == 4
        return WasMurderedClue(call[1], call[2], call[3])
    elif call[0] == "WasMurderedInitial":
        assert len(call) == 5
        return WasMurderedInitialClue(call[1], call[2], call[3], call[4])
    elif call[0] == "WasMurderedBodyTwoOptions":
        assert len(call) == 3
        return WasMurderedBodyTwoOptionsClue(call[1], call[2])
    elif call[0] == "WasMurderedScream":
        assert len(call) == 3
        return WasMurderedScreamClue(call[1], call[2])
    elif call[0] == "WasMurderedBefore":
        assert len(call) == 5
        return WasMurderedBeforeClue(call[1], call[2], call[3], call[4])
    elif call[0] == "WasMurderedAfter":
        assert len(call) == 5
        return WasMurderedAfterClue(call[1], call[2], call[3], call[4])
    elif call[0] == "WasVictimAliveAt":
        assert len(call) == 3
        return WasVictimAliveAtClue(call[1], call[2])
    elif call[0] == "WasVictimDeadAt":
        assert len(call) == 3
        return WasVictimDeadAtClue(call[1], call[2])
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


def create_murder_time_clues(murder_time, interval_size, difficulty):
    r = -1
    if difficulty == "easy":
        r = randint(0, 1)  # Only the first two types of clues are used
    else:
        r = randint(2, 6)

    third_clue = None
    if r == 0:
        first_clue = create_clue(
            [
                "WasMurderedScream",
                murder_time,
                Time(murder_time.seconds + interval_size),
            ]
        )
        second_clue = create_clue(
            [
                "WasMurderedBodyTwoOptions",
                Time(murder_time.seconds - interval_size),
                murder_time,
            ]
        )
    elif r == 1:
        first_clue = create_clue(
            [
                "WasMurderedScream",
                Time(murder_time.seconds - interval_size),
                murder_time,
            ]
        )
        second_clue = create_clue(
            [
                "WasMurderedBodyTwoOptions",
                murder_time,
                Time(murder_time.seconds + interval_size),
            ]
        )
    elif r == 2:
        first_clue = create_clue(
            [
                "WasMurderedScream",
                Time(murder_time.seconds - 2 * interval_size),
                murder_time,
            ]
        )
        positive = randint(0, 1)
        second_clue = create_clue(
            [
                "WasMurderedBefore",
                Time(murder_time.seconds + 2 * interval_size),
                interval_size,
                positive,
                False,
            ]
        )
        third_clue = create_clue(
            [
                "WasMurderedAfter",
                Time(murder_time.seconds - interval_size),
                interval_size,
                not positive,
                True,  # Use alternative form
            ]
        )
    elif r == 3:
        first_clue = create_clue(
            [
                "WasMurderedScream",
                murder_time,
                Time(murder_time.seconds + 2 * interval_size),
            ]
        )
        positive = randint(0, 1)
        second_clue = create_clue(
            [
                "WasMurderedBefore",
                Time(murder_time.seconds + interval_size),
                interval_size,
                positive,
                False,
            ]
        )
        third_clue = create_clue(
            [
                "WasMurderedAfter",
                Time(murder_time.seconds - 3 * interval_size),
                interval_size,
                not positive,
                True,  # Use alternative form
            ]
        )
    elif r == 4:
        first_clue = create_clue(
            [
                "WasMurderedScream",
                Time(murder_time.seconds - 2 * interval_size),
                murder_time,
            ]
        )
        second_clue = create_clue(
            ["WasVictimAliveAt", Time(murder_time.seconds - 2 * interval_size), False]
        )
        third_clue = create_clue(
            [
                "WasVictimAliveAt",
                Time(murder_time.seconds - interval_size),
                True,  # Use alternative form
            ]
        )
    elif r == 5:
        first_clue = create_clue(
            [
                "WasMurderedScream",
                murder_time,
                Time(murder_time.seconds + 2 * interval_size),
            ]
        )
        second_clue = create_clue(
            ["WasVictimDeadAt", Time(murder_time.seconds + 2 * interval_size), False]
        )
        third_clue = create_clue(
            [
                "WasVictimDeadAt",
                Time(murder_time.seconds + interval_size),
                True,  # Use alternative form
            ]
        )
    elif r == 6:
        first_clue = create_clue(
            [
                "WasMurderedScream",
                Time(murder_time.seconds - interval_size),
                Time(murder_time.seconds + interval_size),
            ]
        )
        second_clue = create_clue(
            ["WasVictimAliveAt", Time(murder_time.seconds - interval_size), False]
        )
        third_clue = create_clue(
            [
                "WasVictimDeadAt",
                Time(murder_time.seconds + interval_size),
                True,  # Use alternative form
            ]
        )
    else:
        raise ValueError("Invalid random number: " + str(r))

    # print("Murder time:", str(murder_time))
    # print(first_clue.string_english())
    # print(second_clue.string_english())
    # if third_clue is not None:
    #    print(third_clue.string_english())
    # assert False

    return first_clue, second_clue, third_clue

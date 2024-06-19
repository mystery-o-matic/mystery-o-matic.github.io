from random import randint, choice
from mystery_o_matic.weapons import get_weapon_type
from mystery_o_matic.time import parse_time

class AbstractClue:
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

class SawWhenArrivingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()

    def __str__(self):
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
            assert False

        if not self.object_is_alive:
            str += "the body of "

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "somebody"

        str += '{} when I arrived to the {} at {}"'
        return str.format(self.subject, object, self.place, self.time)

    def is_incriminating(self, killer, victim, place, time):
        if (
            self.subject == killer
            and self.object == victim
        ):
            return True
        return False

    def manipulate(self, killer, victim, alibi_place):
        if (
            self.subject == killer
            and self.object == victim
        ):
            if not self.object_is_alive:
                # If the body was seen, it is too suspicious to change
                return None

            #r = randint(0, 1)
            #if r == 0:
            self.object = "$NOBODY"
            #elif r == 1:
            self.place = alibi_place

            return self
        assert False, "Not implemented"

class NotSawWhenArrivingLeavingClue(AbstractClue):
    def __init__(self, subject, object, place, time):
        self.subject = subject
        self.object = object
        self.place = place
        self.time = time
        super().__init__()

    def __str__(self):
        r = randint(0, 2)
        str = '{} said: "'

        if r == 0:
            str += ""
        elif r == 1:
            str += "I think "
        elif r == 2:
            str += "I'm sure "
        else:
            assert False

        str += '{} was not in the {} at {}"'
        return str.format(self.subject, self.object, self.place, self.time)

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        assert False, "Not implemented"

class SawVictimWhenArrivingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()

    def __str__(self):
        str = '{} said: "I saw '
        if not self.object_is_alive:
            # This should never happen, since the victim produced this clue
            # when they were alive
            str += "the body of "

        str += '{} arriving to the {} at {}"'
        return str.format(self.subject, self.object, self.place, self.time)
    def is_incriminating(self, killer, victim, place, time):
        if (
            self.subject == killer
            and self.object == victim
        ):
            return True
        return False
    def manipulate(self, killer, victim, alibi_place):
        if (
            self.subject == killer
            and self.object == victim
        ):
            return SawVictimWhenLeavingClue(self.subject, self.object, self.object_is_alive, alibi_place, self.time)
        assert False, "Not implemented"

class SawVictimWhenLeavingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()

    def __str__(self):
        str = '{} said: "I saw '
        str += '{} leaving the {} at {}"'
        return str.format(self.subject, self.object, self.place, self.time)
    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        assert False, "Not implemented"

class SawWhenLeavingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()
    def __str__(self):
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
            assert False

        if not self.object_is_alive:
            str += "the body of "

        if self.foggy and self.object_is_alive:
            if object != "$NOBODY":
                object = "somebody"

        str += '{} when I was leaving the {} at {}"'
        return str.format(self.subject, object, self.place, self.time)

    def is_incriminating(self, killer, victim, place, time):
        if (
            self.subject == killer
            and self.object == victim
        ):
            return True
        return False

    def manipulate(self, killer, victim, alibi_place):
        if (
            self.subject == killer
            and self.object == victim
        ):
            if not self.object_is_alive:
                # If the body was seen, it is too suspicious to change
                return None

            #r = randint(0, 1)
            #if r == 0:
            self.object = "$NOBODY"
            #elif r == 1:
            self.place = alibi_place

            return self
        assert False, "Not implemented"

class NotSawWhenLeavingClue(AbstractClue):
    def __init__(self, subject, object, place, time):
        self.subject = subject
        self.object = object
        self.place = place
        self.time = time
        super().__init__()

    def __str__(self):
        r = randint(0, 2)
        str = '{} said: "'

        if r == 0:
            str += ""
        elif r == 1:
            str += "I think "
        elif r == 2:
            str += "I'm sure "
        else:
            assert False

        str += '{} was not in the {} at {}"'
        return str.format(self.subject, self.object, self.place, self.time)

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        assert False, "Not implemented"

class WasMurderedClue(AbstractClue):
    def __init__(self, victim, place, time):
        self.subject = None
        self.object = victim
        self.object_is_alive = False
        self.place = place
        self.time = time
        super().__init__()

    def __str__(self):
        assert False, "Not implemented"

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        assert False, "Not implemented"

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

    def __str__(self):
        return "{} was murdered in the {} at some time between {} and {}!".format(
            self.subject, self.object, self.time_start, self.time_end
        )

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        assert False, "Not implemented"

class WasMurderedInspectionClue(AbstractClue):
    time1 = None
    time2 = None
    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        super().__init__()

    def __str__(self):
        return "A close examination of the body reveals that the murder took place either at {} or at {}".format(
            self.time1, self.time2
        )

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        assert False, "Not implemented"

class WasMurderedAutopsyClue(AbstractClue):
    time1 = None
    time2 = None
    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        super().__init__()

    def __str__(self):
        return "A blood-curdling scream of the victim was heard either at {} or at {}".format(
            self.time1, self.time2
        )

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        assert False, "Not implemented"

class PoliceArrivedClue(AbstractClue):
    def __init__(self, time):
        self.time = time
        super().__init__()

    def __str__(self):
        return "Police arrived at {}!".format(self.time)

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        assert False, "Not implemented"

class StayedClue(AbstractClue):
    def __init__(self, subject, place, time_start, time_end):
        self.subject = subject
        self.object = place
        self.place = place
        self.time_start = time_start
        self.time_end = time_end
        super().__init__()

    def __str__(self):
        r = randint(0, 2)

        if r == 0:
            str = '{} said: "I was in the {} from {} to {}"'
            return str.format(
                self.subject, self.place, self.time_start, self.time_end
            )
        elif r == 1:
            str = '"I was in the {} from {} to {}" stated {}'
            return str.format(
                self.place, self.time_start, self.time_end, self.subject
            )
        elif r == 2:
            str = '"I stayed in the {} from {} to {}" claimed {}'
            return str.format(
                self.place, self.time_start, self.time_end, self.subject
            )
        else:
            assert False

    def is_incriminating(self, killer, victim, place, time):
        if (
            self.subject == killer
            and self.place == place
            and parse_time(self.time_start) <= parse_time(time)
            and parse_time(self.time_end) >= parse_time(time)
        ):
            return True
        return False

    def manipulate(self, killer, victim, alibi_place):
        self.place = alibi_place
        return self

class HeardClue(AbstractClue):
    def __init__(self, subject, action, time):
        self.subject = subject
        self.activity = action
        self.time = time
        super().__init__()

    def __str__(self):
        r = randint(0, 1)

        if r == 0:
            str = '{} said: "I {} at {}"'
            return str.format(self.subject, self.activity, self.time)
        elif r == 1:
            str = '"I {} at {}" said {}'
            return str.format(self.activity, self.time, self.subject)
        else:
            assert False

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        assert False, "Not implemented"

class WeaponNotUsedClue(AbstractClue):
    def __init__(self, weapon):
        self.weapon = weapon
        super().__init__()

    def __str__(self):
        r = randint(0, 1)
        weapon = self.weapon

        if r == 0:
            str = "Inspecting the body reveals "
        elif r == 1:
            str = "The inspection of the body indicates "
        else:
            assert False

        weapon_type = get_weapon_type(weapon)
        if weapon_type == "projectile":
            return str + "there are no projectile holes."
        elif weapon_type == "strangulation":
            return str + "no signs of strangulation."
        elif weapon_type == "sharp force":
            return str + "no signs of stabbing."
        elif weapon_type == "poisoning":
            return str + " that the "+ weapon + " was not the murderer weapon."
        elif weapon_type == "blunt force":
            return str + " no signs of contusion."
        else:
            assert False, "Unknown type of weapon: "+ weapon

def create_clue(call):
    print(call)
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
    # Heard is missing
    else:
        assert False, "Invalid clue!: " + str(call)
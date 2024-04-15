from random import randint
from mystery_o_matic.weapons import get_weapon_type

class Clue:
    """
    Represents a clue in a mystery investigation.

    Attributes:
        name (str): The name of the clue.
        fields (list): The fields associated with the clue.
        foggy (bool): Indicates if the clue is foggy or not.
    """

    name = ""
    fields = []

    def __init__(self, name, fields):
        """
        Initialize a Clue object.

        Args:
            name (str): The name of the clue.
            fields (list): A list of fields associated with the clue.
        """
        self.name = name
        self.fields = fields
        r = randint(1, 10)
        self.foggy = False
        if r <= 5:
            self.foggy = True

    def __str__(self):
        if self.name == "SawWhenArriving":
            return self.print_SawWhenArriving_clue()
        elif self.name == "NotSawWhenArriving":
            return self.print_NotSawWhenArrivingLeaving_clue()
        elif self.name == "SawVictimWhenArriving":
            return self.print_SawVictimWhenArriving_clue()
        elif self.name == "SawVictimWhenLeaving":
            return self.print_SawVictimWhenLeaving_clue()
        elif self.name == "SawWhenLeaving":
            return self.print_SawWhenLeaving_clue()
        elif self.name == "NotSawWhenLeaving":
            return self.print_NotSawWhenArrivingLeaving_clue()
        elif self.name == "WasMurderedInitial":
            return "{} was murdered in the {} at some time between {} and {}!".format(
                self.fields[0], self.fields[1], self.fields[2], self.fields[3]
            )
        elif self.name == "WasMurderedInspection":
            return "A close examination of the body reveals that the murder took place either at {} or at {}".format(
                self.fields[0], self.fields[1]
            )

        elif self.name == "WasMurderedAutopsy":
            return "The pathologist says that murder took place either at {} or at {}".format(
                self.fields[0], self.fields[1]
            )

        elif self.name == "PoliceArrived":
            return "Police arrived at {}!".format(self.fields[0])
        elif self.name == "Stayed":
            return self.print_Stayed_clue()
        elif self.name == "Heard":
            return self.print_Heard_clue()
        elif self.name == "WeaponNotUsed":
            return self.print_WeaponNotUsed_clue()
        else:
            print("Invalid clue!", self.name, self.fields)
            assert False

    def is_incriminating(self, killer, victim):
        """
        Check if the clue is incriminating based on the provided killer and victim.

        Args:
            killer (str): The name of the killer.
            victim (str): The name of the victim.

        Returns:
            bool: True if the clue is incriminating, False otherwise.
        """
        if (
            self.name == "SawWhenArriving"
            and self.fields[0] == killer
            and self.fields[1] == victim
        ):
            return True
        elif (
            self.name == "SawWhenLeaving"
            and self.fields[0] == killer
            and self.fields[1] == victim
            and not self.fields[2]
        ):
            return True
        elif (
            self.name == "SawVictimWhenArriving"
            and self.fields[0] == killer
            and self.fields[1] == victim
        ):
            return True
        return False

    def print_SawVictimWhenArriving_clue(self):
        """
        Returns a formatted string representing a clue about the witness who saw the victim arriving at a certain location.
        """
        str = '{} said: "I saw '
        if not self.fields[2]:
            # This should never happen, since the victim produced this clue
            # when they were alive
            str += "the body of "

        str += '{} arriving to the {} at {}"'
        return str.format(
            self.fields[0], self.fields[1], self.fields[3], self.fields[4]
        )

    def print_SawVictimWhenLeaving_clue(self):
        """
        Returns a formatted string representing a clue about the witness who saw the victim leaving a certain location.
        """
        str = '{} said: "I saw '
        str += '{} leaving the {} at {}"'
        return str.format(
            self.fields[0], self.fields[1], self.fields[3], self.fields[4]
        )

    def print_SawWhenLeaving_clue(self):
        r = randint(0, 2)
        str = '{} said "'

        if self.fields[1] == "$NOBODY":
            r = 0

        if r == 0:
            str += "I saw "
        elif r == 1:
            str += "I noticed "
        elif r == 2:
            str += "I spotted "
        else:
            assert False

        if not self.fields[2]:
            str += "the body of "

        if self.foggy and self.fields[2]:
            if self.fields[1] != "$NOBODY":
                self.fields[1] = "somebody"

        str += '{} when I was leaving the {} at {}"'
        return str.format(
            self.fields[0], self.fields[1], self.fields[3], self.fields[4]
        )

    def print_SawWhenArriving_clue(self):
        r = randint(0, 2)
        str = '{} said "'

        if self.fields[1] == "$NOBODY":
            r = 0

        if r == 0:
            str += "I saw "
        elif r == 1:
            str += "I noticed "
        elif r == 2:
            str += "I spotted "
        else:
            assert False

        if not self.fields[2]:
            str += "the body of "

        if self.foggy and self.fields[2]:
            if self.fields[1] != "$NOBODY":
                self.fields[1] = "somebody"

        str += '{} when I arrived to the {} at {}"'
        return str.format(
            self.fields[0], self.fields[1], self.fields[3], self.fields[4]
        )

    def print_NotSawWhenArrivingLeaving_clue(self):
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
        return str.format(
            self.fields[0], self.fields[1], self.fields[2], self.fields[3]
        )

    def print_WeaponNotUsed_clue(self):
        r = randint(0, 1)
        weapon = self.fields[0]

        if r == 0:
            str = "Inspecting the body reveals "
        elif r == 1:
            str = "The inspection of the body indicates "
        else:
            assert False

        weapon_type = get_weapon_type(weapon)
        if weapon_type == "projectile":
            return str + "there are no holes."
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

    def print_Stayed_clue(self):
        r = randint(0, 2)

        if r == 0:
            str = '{} said: "I was in the {} from {} to {}"'
            return str.format(
                self.fields[0], self.fields[1], self.fields[2], self.fields[3]
            )
        elif r == 1:
            str = '"I was in the {} from {} to {}" stated {}'
            return str.format(
                self.fields[1], self.fields[2], self.fields[3], self.fields[0]
            )
        elif r == 2:
            str = '"I stayed in the {} from {} to {}" claimed {}'
            return str.format(
                self.fields[1], self.fields[2], self.fields[3], self.fields[0]
            )
        else:
            assert False

    def print_Heard_clue(self):
        r = randint(0, 1)

        if r == 0:
            str = '{} said: "I {} at {}"'
            return str.format(self.fields[0], self.fields[1], self.fields[2])
        elif r == 1:
            str = '"I {} at {}" said {}'
            return str.format(self.fields[1], self.fields[2], self.fields[0])

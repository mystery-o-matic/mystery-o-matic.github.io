from datetime import timedelta
from random import shuffle, randint
from hashlib import sha256

from mystery_o_matic.clues import Clue
from mystery_o_matic.solidity import get_tx, get_event
from mystery_o_matic.text import get_char_name


def parse_time(t):
    """
    Converts a time string in the format "hh:mm" to seconds.

    Parameters:
    t (str): The time string to be parsed.

    Returns:
    int: The time in seconds.
    """
    h, m = map(int, t.split(":"))
    return h * 3600 + m * 60


def print_time(t):
    """
    Converts a given time in seconds to a formatted string representation.

    Args:
        t (int): The time in seconds.

    Returns:
        str: The formatted time string in the format "hours:minutes".
    """
    clock = timedelta(seconds=t)
    h, m, s = str(clock).split(":")
    return h + ":" + m


def get_intervals_length_from_events(source, contract_name, events):
    """
    Calculates the length of intervals between events.

    Args:
        source (str): The source of the events.
        contract_name (str): The name of the contract.
        events (list): A list of events.

    Returns:
        float: The length of intervals between events in minutes.
    """
    interval_size = 15 * 60  # 15 minutes
    initial_time = parse_time("9:00")
    for event in events:
        event = get_event(source, contract_name, event)
        if event[0] == "PoliceArrived":
            final_time = parse_time(event[1])
            return (final_time - initial_time) / interval_size


class Mystery:
    source = None
    solution = []
    characters = []
    weapon_locations = {}
    killer = None
    victim = None
    initial_clues = []
    additional_clues = []
    initial_time = "9:00"
    murder_time = ""
    interval_size = 15 * 60  # 15 minutes
    final_time = ""

    def __init__(self, initial_locations, weapon_locations, weapon_used, source, txs):
        """
        Initialize the Mystery class.

        Args:
            initial_locations (list): List of initial locations.
            weapon_locations (dict): Dictionary of weapon locations.
            weapon_used (str): The weapon used.
            source (str): The source of the smart contract.
            txs (list): List of transactions.

        Returns:
            None
        """
        self.source = source
        self.initial_locations = initial_locations
        self.final_locations = dict()
        self.weapon_used = weapon_used
        self.weapon_locations = weapon_locations

        for tx in txs:
            self.solution.append(get_tx(self.source, "StoryModel", tx))

        for action in self.solution:
            if action[0] == "kills":
                self.killer = action[1]
                self.victim = action[2]

        self.characters = ["alice", "bob", "carol", "dave", "eddie", "frida"]
        shuffle(self.characters)
        self.characters = self.characters[:3]

    def get_characters(self):
        return self.characters

    def get_suspects(self):
        victimName = None
        for i, char in enumerate(self.characters):
            if "$CHAR" + str(i + 1) == self.victim:
                victimName = char

        suspects = []
        for character in self.characters:
            if character == victimName:
                continue
            suspects.append(character)

        return suspects

    def load_events(self, events):
        event_calls = []
        for event in events:
            event_calls.append(get_event(self.source, "StoryModel", event))

        for call in event_calls:
            if call[0].startswith("NotSaw") and call[1] == self.victim:
                continue
            # victim clues should be modified
            elif call[0].startswith("Saw") and call[1] == self.victim:
                if call[2] == "$NOBODY":  # No witnesses
                    continue
                elif call[0] == "SawWhenLeaving":  # TODO
                    continue
                else:
                    call[0] = "SawVictimWhenArriving"
                    call[1] = call[2]
                    call[2] = self.victim
            elif call[0].startswith("Stayed") and call[1] == self.victim:
                continue
            elif call[0] == "FinalLocation":
                self.final_locations[call[1]] = call[2]
                continue

            if call[0] == "WasMurdered":
                self.initial_clues.append(Clue(call[0], [call[1], call[2]]))
                self.murder_time = call[3]
            elif call[0] == "PoliceArrived":
                self.initial_clues.append(Clue(call[0], call[1:]))
            else:
                self.additional_clues.append(Clue(call[0], call[1:]))

    def process_clues(self):
        # Process initial clues
        for clue in self.initial_clues:
            if clue.name == "PoliceArrived":
                self.final_time = clue.fields[0]

        # Filter initial clues
        clues = []
        for clue in self.initial_clues:
            if clue.name == "PoliceArrived":
                continue
            elif clue.name == "WasMurdered":
                clue.name = "WasMurderedInitial"
                clue.fields += [self.initial_time, self.final_time]
                clues.append(clue)
            else:
                clues.append(clue)

        self.initial_clues = clues

        # Filter additional clues
        clues = []
        for clue in self.additional_clues:
            if clue.is_incriminating(self.killer, self.victim):
                continue
            else:
                clues.append(clue)

        self.additional_clues = clues
        for weapon in self.weapon_locations.values():
            if weapon != self.weapon_used:
                clue = Clue("WeaponNotUsed", [weapon])
                self.additional_clues.append(clue)

        # The player needs more hints to fully determinate when the murdered took place
        murder_time_seconds = parse_time(self.murder_time)
        rand_bool = randint(0, 1)
        if rand_bool:
            first_clue = Clue(
                "WasMurderedInspection",
                [
                    self.murder_time,
                    print_time(murder_time_seconds + self.interval_size),
                ],
            )
            second_clue = Clue(
                "WasMurderedAutopsy",
                [
                    print_time(murder_time_seconds - self.interval_size),
                    self.murder_time,
                ],
            )
        else:
            first_clue = Clue(
                "WasMurderedInspection",
                [
                    print_time(murder_time_seconds - self.interval_size),
                    self.murder_time,
                ],
            )
            second_clue = Clue(
                "WasMurderedAutopsy",
                [
                    self.murder_time,
                    print_time(murder_time_seconds + self.interval_size),
                ],
            )

        shuffle(self.additional_clues)

        first_clue_index = randint(0, len(self.additional_clues) // 2)
        self.additional_clues.insert(first_clue_index, first_clue)
        second_clue_index = randint(
            len(self.additional_clues) // 2, len(self.additional_clues)
        )
        self.additional_clues.insert(second_clue_index, second_clue)

    def get_intervals(self):
        """
        Returns a list of time intervals between the initial_time and final_time,
        with a specified interval size.

        Returns:
            intervals (list): A list of time intervals.
        """
        intervals = []
        initial_seconds = self._time_to_seconds(self.initial_time)
        final_seconds = self._time_to_seconds(self.final_time)

        for t in range(initial_seconds, final_seconds + 1, self.interval_size):
            intervals.append(print_time(t))

        return intervals

    def _time_to_seconds(self, t):
        h, m = map(int, t.split(":"))
        return h * 3600 + m * 60

    def get_answer(self):
        """
        Returns the answer to the mystery based on the killer, weapon used, and murder time.

        The answer is constructed by concatenating the character, weapon, and murder time
        in the format: character-weapon-murder_time.

        Returns:
            str: The answer to the mystery.
        """
        index = int("".join(filter(str.isdigit, self.killer))) - 1
        return self.characters[index] + "-" + self.weapon_used + "-" + self.murder_time

    def get_answer_hash(self):
        """
        Returns the SHA256 hash of the answer.

        This method retrieves the answer using the `get_answer` method,
        calculates the SHA256 hash of the answer, and returns the hash value.

        Returns:
            str: The SHA256 hash of the answer.
        """
        answer = self.get_answer()
        print("Answer is:", answer)
        m = sha256()
        m.update(answer.encode("utf-8"))
        return m.hexdigest()

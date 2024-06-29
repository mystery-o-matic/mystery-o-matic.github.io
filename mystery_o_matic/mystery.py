from random import shuffle, randint, choice
from hashlib import sha256

from mystery_o_matic.clues import *
from mystery_o_matic.solidity import get_tx, get_event
from mystery_o_matic.time import Time  # parse_time, print_time


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
    for event in events:
        event = get_event(source, contract_name, event, Time(0))
        if event[0] == "PoliceArrived":
            final_time = event[1]
            return final_time.seconds / interval_size

    raise ValueError("No police arrived event found")


class Mystery:
    source = None
    solution = []
    characters = []
    weapon_locations = {}
    killer = None
    victim = None
    murder_place = None
    alibi_place = None
    initial_clues = []
    additional_clues = []
    additional_clues_with_lies = []
    initial_time = ""
    murder_time = ""
    interval_size = 15 * 60  # 15 minutes
    final_time = ""
    number_characters = 0

    def __init__(
        self, initial_locations, weapon_locations, weapon_used, activities, source, txs
    ):
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
        self.number_characters = len(initial_locations)

        self.initial_time = Time(str(choice(range(1, 9))) + ":00")

        for tx in txs:
            self.solution.append(get_tx(self.source, "StoryModel", tx))

        for action in self.solution:
            if action[0] == "kills":
                self.killer = action[1]
                self.victim = action[2]

        self.characters = ["alice", "bob", "carol", "dave", "eddie", "frida"]
        shuffle(self.characters)
        self.characters = self.characters[: self.number_characters]
        self.cplaceholders = [
            "$CHAR" + str(i + 1) for i in range(self.number_characters)
        ]
        self.activities = activities

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
        # Load all the events from the model
        for event in events:
            event_calls.append(
                get_event(self.source, "StoryModel", event, self.initial_time)
            )

        for call in event_calls:
            # Skip the clues that are produced by the victim
            if call[0].startswith("NotSaw") and call[1] == self.victim:
                continue
            if call[0].startswith("Interacted") and call[1] == self.victim:
                # Let's swap the subjects
                call[1] = call[2]
                call[2] = self.victim

            elif call[0].startswith("Stayed") and call[1] == self.victim:
                pass  # This is handled later

            # Some victim clues can be reused, but changing the subject
            elif call[0].startswith("Saw") and call[1] == self.victim:
                # If the victim was alone, discard the clue,
                # since there are no other witness to use as subjects
                if call[2] == "$NOBODY":
                    continue
                elif call[0] == "SawWhenLeaving":
                    call[0] = "SawVictimWhenLeaving"
                    call[1] = call[2]
                    call[2] = self.victim
                else:
                    call[0] = "SawVictimWhenArriving"
                    call[1] = call[2]
                    call[2] = self.victim
            elif call[0] == "FinalLocation":
                self.final_locations[call[1]] = call[2]
                continue

            # The "WasMurdered" and "PoliceArrived" clues are considered initial clues
            if call[0] == "WasMurdered":
                self.initial_clues.append(create_clue(call))
                self.murder_time = call[3]
            elif call[0] == "PoliceArrived":
                self.initial_clues.append(create_clue(call))
            elif call[0] == "Heard":
                # Add the Heard clue as expected, except when the victim is the subject
                if call[1] == self.victim:
                    continue

                # Create the clue but with some changes
                # clue = create_clue(call)
                place = call[2].replace("$", "")

                if place in self.activities:
                    activity = choice(self.activities[place])
                    # print(clue)
                    self.additional_clues.append(HeardClue(call[1], activity, call[3]))

            elif call[0] == "Stayed":
                # Add the Stayed clue as expected, except when the victim is the subject
                if call[1] != self.victim:
                    self.additional_clues.append(create_clue(call))
            else:
                self.additional_clues.append(create_clue(call))

    def process_clues(self):
        # Process initial clues
        for clue in self.initial_clues:
            if isinstance(clue, PoliceArrivedClue):
                self.final_time = clue.time

        # Filter initial clues
        clues = []
        for clue in self.initial_clues:
            if isinstance(clue, PoliceArrivedClue):
                continue  # Discard
            elif isinstance(clue, WasMurderedClue):
                clues.append(
                    WasMurderedInitialClue(
                        clue.object, clue.place, self.initial_time, self.final_time
                    )
                )
            else:
                clues.append(clue)

        self.initial_clues = clues

        # The killer selects a place for their alibi
        self.murder_place = self.final_locations[self.victim]
        places = list(self.weapon_locations.keys())
        self.alibi_place = "$" + choice(places)
        while self.alibi_place == self.murder_place:
            self.alibi_place = "$" + choice(places)

        # Filter additional clues
        additional_clues = []
        #print(self.final_locations)
        for clue in self.additional_clues:
            if isinstance(clue, EvidenceClue):
                if self.final_locations[clue.subject] == clue.place:
                    continue

            additional_clues.append(clue)

        self.additional_clues = additional_clues
        clues_with_lies = []
        clues_without_lies = []
        for clue in self.additional_clues:
            if clue.is_incriminating(
                self.killer, self.victim, self.murder_place, self.murder_time
            ):
                clue = clue.manipulate(self.killer, self.victim, self.alibi_place)
                if clue is not None:
                    clues_with_lies.append(clue)
            else:
                clues_without_lies.append(clue)
                clues_with_lies.append(clue)

        self.additional_clues = clues_without_lies
        self.additional_clues_with_lies = clues_with_lies
        for weapon in self.weapon_locations.values():
            if weapon != self.weapon_used:
                clue = WeaponNotUsedClue(weapon)
                self.additional_clues.append(clue)
                self.additional_clues_with_lies.append(clue)

        # The player needs more hints to fully determinate when the murdered took place
        assert self.murder_time != "", "Time of murder is missing"

        rand_bool = randint(0, 1)
        if rand_bool:
            first_clue = create_clue(
                [
                    "WasMurderedInspection",
                    self.murder_time,
                    Time(self.murder_time.seconds + self.interval_size),
                ]
            )
            second_clue = create_clue(
                [
                    "WasMurderedAutopsy",
                    Time(self.murder_time.seconds - self.interval_size),
                    self.murder_time,
                ]
            )
        else:
            first_clue = create_clue(
                [
                    "WasMurderedInspection",
                    Time(self.murder_time.seconds - self.interval_size),
                    self.murder_time,
                ]
            )
            second_clue = create_clue(
                [
                    "WasMurderedAutopsy",
                    self.murder_time,
                    Time(self.murder_time.seconds + self.interval_size),
                ]
            )

        shuffle(self.additional_clues)
        shuffle(self.additional_clues_with_lies)

        first_clue_index = randint(0, len(self.additional_clues) // 2)
        self.additional_clues.insert(first_clue_index, first_clue)
        second_clue_index = randint(
            len(self.additional_clues) // 2, len(self.additional_clues)
        )
        self.additional_clues.insert(second_clue_index, second_clue)

        first_clue_index = randint(0, len(self.additional_clues_with_lies) // 2)
        self.additional_clues_with_lies.insert(first_clue_index, first_clue)
        second_clue_index = randint(
            len(self.additional_clues_with_lies) // 2,
            len(self.additional_clues_with_lies),
        )
        self.additional_clues_with_lies.insert(second_clue_index, second_clue)

        # Load additional initial clues
        self.initial_clues.append(MurderWasAloneStatement())
        self.initial_clues.append(MurderWasNotFoundWithBodyStatement())

        self.weapon_locations_intro = WeaponLocationsIntroStatement()
        self.weapon_locations_clues = []
        # Load weapon locations clues
        for loc, weapon in self.weapon_locations.items():
            self.weapon_locations_clues.append(
                WeaponLocationStatement(weapon, "$"+loc)
            )

        self.final_locations_intro = FinalLocationsIntroStatement(self.final_time)
        self.final_locations_clues = []
        # Load final locations clues
        for c, p in self.final_locations.items():
            self.final_locations_clues.append(CharacterLocationStatement(c, p))

        # Convert all statements/clues to strings
        self.weapon_locations_intro = self.weapon_locations_intro.string()
        for i, clue in enumerate(self.weapon_locations_clues):
            self.weapon_locations_clues[i] = clue.string()

        self.final_locations_intro = self.final_locations_intro.string()
        for i, clue in enumerate(self.final_locations_clues):
            self.final_locations_clues[i] = clue.string()

        for i, clue in enumerate(self.initial_clues):
            self.initial_clues[i] = clue.string()

        for i, clue in enumerate(self.additional_clues):
            self.additional_clues[i] = clue.string()

        for i, clue in enumerate(self.additional_clues_with_lies):
            self.additional_clues_with_lies[i] = clue.string()

    def get_intervals(self):
        """
        Returns a list of time intervals between the initial_time and final_time,
        with a specified interval size.

        Returns:
            intervals (list): A list of time intervals.
        """
        intervals = []
        initial_seconds = self.initial_time.seconds
        final_seconds = self.final_time.seconds

        for t in range(initial_seconds, final_seconds + 1, self.interval_size):
            intervals.append(str(Time(t)))

        return intervals

    def get_answer(self):
        """
        Returns the answer to the mystery based on the killer, weapon used, and murder time.

        The answer is constructed by concatenating the character, weapon, and murder time
        in the format: character-weapon-murder_time.

        Returns:
            str: The answer to the mystery.
        """
        assert isinstance(self.killer, str), "Failed to determine the killer"
        index = int("".join(filter(str.isdigit, self.killer))) - 1
        weapon = self.weapon_used.replace("$", "").lower()
        return (
            self.characters[index]
            + "-"
            + weapon
            + "-"
            + str(self.murder_time)
        )

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

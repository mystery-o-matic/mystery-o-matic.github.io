from random import shuffle, randint, choice, random, Random

STAY_ACTIVITY_PROBABILITY = 0.7
# Max number of foggy sightings upgraded to profile-matchable descriptions.
# Real puzzles rarely have more than 1-2 eligible foggy sightings, so this is a
# safety ceiling rather than a typical count.
TRAIT_CLUE_CAP = 3
from hashlib import sha256

from mystery_o_matic.clues import *
from mystery_o_matic.solidity import get_tx, get_event
from mystery_o_matic.time import Time
from mystery_o_matic.traits import ALL_TRAITS

# Register language renderers (must happen before any clue.string() calls)
import mystery_o_matic.lang.en  # noqa: F401
import mystery_o_matic.lang.es  # noqa: F401
import mystery_o_matic.lang.ru  # noqa: F401


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


def _insert_clue_groups_across_sections(clues, clue_groups):
    clue_groups = [group for group in clue_groups if group]
    if not clue_groups:
        return

    total_insertions = sum(len(group) for group in clue_groups)
    final_length = len(clues) + total_insertions
    insertions = []

    for group in clue_groups:
        shuffle(group)
        section_count = len(group)
        for i, clue in enumerate(group):
            section_start = (i * final_length) // section_count
            section_end = ((i + 1) * final_length) // section_count
            insert_index = randint(section_start, section_end - 1)
            insertions.append((insert_index, random(), len(insertions), clue))

    insertions.sort()
    for insert_index, _, _, clue in insertions:
        clues.insert(min(insert_index, len(clues)), clue)


class Mystery:
    difficulty = ""
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
        self,
        difficulty,
        initial_locations,
        weapon_locations,
        weapon_used,
        activities,
        source,
        txs,
        stay_activities=None,
        used_seed=None,
    ):
        """
        Initialize the Mystery class.

        Args:
            difficulty (string): Difficulty
            initial_locations (list): List of initial locations.
            weapon_locations (dict): Dictionary of weapon locations.
            weapon_used (str): The weapon used.
            source (str): The source of the smart contract.
            txs (list): List of transactions.

        Returns:
            None
        """
        self.difficulty = difficulty
        self.source = source
        self.initial_locations = initial_locations
        self.final_locations = dict()
        self.weapon_used = weapon_used
        self.weapon_locations = weapon_locations
        self.number_characters = len(initial_locations)

        self.initial_time = Time(str(choice(range(1, 7))) + ":00")

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
        self.stay_activities = stay_activities or {}

        # Assign each character a unique distinguishing "tell" for the profile
        # mechanic. Drawn from a DERIVED RNG (string seed — a tuple seed is a
        # TypeError on 3.14) so the global stream is untouched and existing
        # puzzles regenerate byte-identically. Keyed by $CHARn placeholder.
        self.used_seed = used_seed
        self._trait_rng = Random("%s-traits" % (used_seed,))
        trait_pool = list(ALL_TRAITS)
        self._trait_rng.shuffle(trait_pool)
        self.character_traits = {
            self.cplaceholders[i]: trait_pool[i]
            for i in range(self.number_characters)
        }

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
                    place_generic = call[2].replace("$", "")
                    stay_activity = None
                    if (place_generic in self.stay_activities
                            and self.stay_activities[place_generic]
                            and random() < STAY_ACTIVITY_PROBABILITY):
                        stay_activity = choice(self.stay_activities[place_generic])
                    self.additional_clues.append(
                        StayedClue(call[1], call[2], call[3], call[4], activity=stay_activity)
                    )
            else:
                self.additional_clues.append(create_clue(call))

    def _collect_describable_sightings(self):
        """Sightings of a living character that can be rendered as a foggy,
        profile-matchable clue, deduped across both clue lists."""
        sightings = []
        seen_ids = set()
        for c in self.additional_clues + self.additional_clues_with_lies:
            if id(c) in seen_ids:
                continue
            seen_ids.add(id(c))
            if (isinstance(c, (SawWhenArrivingClue, SawWhenLeavingClue))
                    and c.object_is_alive
                    and c.object in self.character_traits):
                sightings.append(c)
        return sightings

    def _pick_fog_kind(self, clue, usable_props):
        kinds = [FOG_TRAIT, FOG_DESCRIPTOR] + list(usable_props.keys())
        pick = self._trait_rng.choice(kinds)
        if pick in usable_props:
            wearers, yes_kind, no_kind = usable_props[pick]
            return yes_kind if clue.object in wearers else no_kind
        return pick

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
        final_location_killer = self.final_locations[self.killer]
        places = list(self.weapon_locations.keys())
        self.alibi_place = "$" + choice(places)
        # avoid using the alibi location as the place of the murder
        # also avoid using the final location of the killer to minimize the chance of incoherent statements
        while (
            self.alibi_place == self.murder_place
            or self.alibi_place == final_location_killer
        ):
            self.alibi_place = "$" + choice(places)

        print("Alibi location is:", self.alibi_place)
        # Filter additional clues
        additional_clues = []
        # print(self.final_locations)
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

        # Step 1: collect sightings of a living character. Any living seen-person
        # is fine, including the victim; only $NOBODY (empty room) has no one to
        # describe, and incriminating killer/victim sightings are already
        # manipulated to $NOBODY upstream.
        # The same clue object lives in both lists when not manipulated, so we
        # dedup by identity and assign each fog_kind once for both modes.
        describable_sightings = self._collect_describable_sightings()

        # Step 2: upgrade a few from "somebody" to ONE of: a specific tell, a
        # coarse gender descriptor ("a woman"), or a coarse property hint
        # ("with/without a hat", "with/without glasses"). A property hint is only
        # offered when the cast is MIXED on it (some traits carry the flag, some
        # don't) so it still narrows. Exclusive per clue.
        property_categories = [
            ("hat", FOG_HAT_YES, FOG_HAT_NO),
            ("glasses", FOG_GLASSES_YES, FOG_GLASSES_NO),
        ]
        n_chars = len(self.character_traits)
        usable_props = {}
        for prop, yes_kind, no_kind in property_categories:
            wearers = {ph for ph, tr in self.character_traits.items() if tr.get(prop)}
            if 0 < len(wearers) < n_chars:
                usable_props[prop] = (wearers, yes_kind, no_kind)

        foggy_sightings = [
            c for c in describable_sightings if c.fog_kind == FOG_SOMEBODY
        ]
        self._trait_rng.shuffle(foggy_sightings)

        if not foggy_sightings and describable_sightings:
            self._trait_rng.shuffle(describable_sightings)
            foggy_sightings = [describable_sightings[0]]
            foggy_sightings[0].foggy = True

        for c in foggy_sightings[:TRAIT_CLUE_CAP]:
            c.fog_kind = self._pick_fog_kind(c, usable_props)

        weapon_not_used_clues = []
        for weapon in self.weapon_locations.values():
            if weapon != self.weapon_used:
                weapon_not_used_clues.append(WeaponNotUsedClue(weapon))

        # The player needs more hints to fully determinate when the murdered took place
        assert self.murder_time != "", "Time of murder is missing"

        first_clue, second_clue, third_clue = create_murder_time_clues(
            self.murder_time, self.interval_size, self.difficulty
        )
        murder_time_clues = [first_clue, second_clue]
        if third_clue is not None:
            murder_time_clues.append(third_clue)

        shuffle(self.additional_clues)
        shuffle(self.additional_clues_with_lies)

        _insert_clue_groups_across_sections(
            self.additional_clues,
            [murder_time_clues[:], weapon_not_used_clues[:]],
        )
        _insert_clue_groups_across_sections(
            self.additional_clues_with_lies,
            [murder_time_clues[:], weapon_not_used_clues[:]],
        )

        # Load additional initial clues
        self.initial_clues.append(MurderWasAloneStatement())
        self.initial_clues.append(MurderWasNotFoundWithBodyStatement())

        self.weapon_locations_intro = WeaponLocationsIntroStatement()
        self.weapon_locations_outro = WeaponLocationsOutroStatement()
        self.weapon_locations_clues = []
        # Load weapon locations clues
        for loc, weapon in self.weapon_locations.items():
            self.weapon_locations_clues.append(
                WeaponLocationStatement(weapon, "$" + loc)
            )

        self.final_locations_intro = FinalLocationsIntroStatement(self.final_time)
        self.final_locations_clues = []
        # Load final locations clues
        for c, p in self.final_locations.items():
            self.final_locations_clues.append(
                CharacterLocationStatement(c, p, self.victim)
            )

        # Convert all statements/clues to strings
        self.weapon_locations_intro = self.weapon_locations_intro.string()
        self.weapon_locations_outro = self.weapon_locations_outro.string()
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
        weapon = weapon.replace("_", " ")
        return self.characters[index] + "-" + weapon + "-" + str(self.murder_time)

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

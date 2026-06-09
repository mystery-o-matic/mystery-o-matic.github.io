from abc import ABC, abstractmethod
from random import randint, choice

from mystery_o_matic.weapons import get_weapon_type
from mystery_o_matic.time import Time
from mystery_o_matic.lang import get_all_renderers

# How a foggy sighting obscures the seen person. `fog_kind` is None when the
# sighting is not foggy (the person is named). When foggy it starts as
# FOG_SOMEBODY and process_clues may upgrade a few to FOG_TRAIT / FOG_DESCRIPTOR.
# NOTE: the language renderers compare fog_kind against these exact string values.
FOG_SOMEBODY = "somebody"      # plain "somebody"
FOG_TRAIT = "trait"            # "someone wearing <tell> (emoji)"
FOG_DESCRIPTOR = "descriptor"  # coarse "a woman" / "a man"
FOG_HAT_YES = "hat_yes"        # coarse "someone with some kind of hat"
FOG_HAT_NO = "hat_no"          # coarse "someone without any kind of hat"
FOG_GLASSES_YES = "glasses_yes"  # coarse "someone wearing glasses"
FOG_GLASSES_NO = "glasses_no"    # coarse "someone without glasses"


class AbstractStatement(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def render(self, renderer):
        pass

    def string(self):
        return {lang: self.render(r) for lang, r in get_all_renderers().items()}


class MurderWasAloneStatement(AbstractStatement):
    def render(self, renderer):
        return renderer.render_murder_was_alone()


class MurderWasNotFoundWithBodyStatement(AbstractStatement):
    def render(self, renderer):
        return renderer.render_murder_was_not_found_with_body()


class WeaponLocationStatement(AbstractStatement):
    def __init__(self, weapon, vplace):
        self.vplace = vplace
        self.weapon = weapon

    def render(self, renderer):
        return renderer.render_weapon_location(self.weapon, self.vplace)


class CharacterLocationStatement(AbstractStatement):
    def __init__(self, subject, place, victim):
        self.subject = subject
        self.victim = victim
        self.place = place

    def render(self, renderer):
        return renderer.render_character_location(self.subject, self.place, self.victim)


class NoOneElseStatement(AbstractStatement):
    def render(self, renderer):
        return renderer.render_no_one_else()


class WeaponLocationsIntroStatement(AbstractStatement):
    def render(self, renderer):
        return renderer.render_weapon_locations_intro()


class WeaponLocationsOutroStatement(AbstractStatement):
    def render(self, renderer):
        return renderer.render_weapon_locations_outro()


class FinalLocationsIntroStatement(AbstractStatement):
    def __init__(self, time):
        self.time = time

    def render(self, renderer):
        return renderer.render_final_locations_intro(self.time)


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
    def render(self, renderer):
        pass

    def string(self):
        return {lang: self.render(r) for lang, r in get_all_renderers().items()}


class SawWhenArrivingClue(AbstractClue):
    def __init__(self, subject, object, object_is_alive, place, time):
        self.subject = subject
        self.object = object
        self.object_is_alive = object_is_alive
        self.place = place
        self.time = time
        super().__init__()
        # None when named (not foggy); FOG_SOMEBODY/TRAIT/DESCRIPTOR when foggy.
        self.fog_kind = FOG_SOMEBODY if self.foggy else None

    def render(self, renderer):
        return renderer.render_saw_when_arriving(
            self.subject, self.object, self.object_is_alive,
            self.place, self.time, self.fog_kind
        )

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

            self.object = "$NOBODY"
            self.place = alibi_place

            return self
        return None


class NotSawWhenArrivingLeavingClue(AbstractClue):
    def __init__(self, subject, object, place, time, mode):
        self.subject = subject
        self.object = object
        self.place = place
        self.time = time
        self.mode = mode
        super().__init__()

    def render(self, renderer):
        return renderer.render_not_saw(
            self.subject, self.object, self.place, self.time
        )

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

    def render(self, renderer):
        return renderer.render_saw_victim_when_arriving(
            self.subject, self.object, self.object_is_alive,
            self.place, self.time
        )

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

    def render(self, renderer):
        return renderer.render_saw_victim_when_leaving(
            self.subject, self.object, self.object_is_alive,
            self.place, self.time
        )

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
        # See SawWhenArrivingClue.fog_kind.
        self.fog_kind = FOG_SOMEBODY if self.foggy else None

    def render(self, renderer):
        return renderer.render_saw_when_leaving(
            self.subject, self.object, self.object_is_alive,
            self.place, self.time, self.fog_kind
        )

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

    def render(self, renderer):
        raise ValueError("WasMurderedClue should not be rendered directly")

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

    def render(self, renderer):
        return renderer.render_was_murdered_initial(
            self.subject, self.object, self.time_start, self.time_end
        )

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

    def render(self, renderer):
        return renderer.render_was_murdered_body_two_options(self.time1, self.time2)

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

    def render(self, renderer):
        return renderer.render_was_victim_dead_at(self.time, self.alternative)

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

    def render(self, renderer):
        return renderer.render_was_victim_alive_at(self.time, self.alternative)

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

    def render(self, renderer):
        return renderer.render_was_murdered_after(
            self.time, self.interval_size, self.positive, self.alternative
        )

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

    def render(self, renderer):
        return renderer.render_was_murdered_before(
            self.time, self.interval_size, self.positive, self.alternative
        )

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

    def render(self, renderer):
        return renderer.render_was_murdered_scream(self.time1, self.time2)

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class PoliceArrivedClue(AbstractClue):
    def __init__(self, time):
        self.time = time
        super().__init__()

    def render(self, renderer):
        raise ValueError("PoliceArrivedClue should not be rendered directly")

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class EvidenceClue(AbstractClue):
    def __init__(self, subject, place):
        self.subject = subject
        self.place = place
        super().__init__()

    def render(self, renderer):
        return renderer.render_evidence(self.subject, self.place)

    def is_incriminating(self, killer, victim, place, time):
        # this can be incriminating, but the killer cannot manipulate them
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class StayedClue(AbstractClue):
    def __init__(self, subject, place, time_start, time_end, activity=None):
        self.subject = subject
        self.object = place
        self.place = place
        self.time_start = time_start
        self.time_end = time_end
        self.activity = activity
        super().__init__()

    def render(self, renderer):
        return renderer.render_stayed(
            self.subject, self.place, self.time_start, self.time_end, self.activity
        )

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
        # The activity was chosen for the original room; once the killer
        # swaps the place for an alibi, the activity no longer fits.
        self.activity = None
        return self


class InteractedClue(AbstractClue):
    def __init__(self, subject0, subject1, place, time):
        self.subject0 = subject0
        self.subject1 = subject1
        self.place = place
        self.time = time
        super().__init__()

    def render(self, renderer):
        return renderer.render_interacted(self.subject0, self.subject1, self.place)

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

    def render(self, renderer):
        activity_text = self.activity[renderer.lang_code]
        return renderer.render_heard(self.subject, activity_text, self.time)

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


class WeaponNotUsedClue(AbstractClue):
    def __init__(self, weapon):
        self.weapon = weapon
        super().__init__()

    def render(self, renderer):
        return renderer.render_weapon_not_used(self.weapon)

    def is_incriminating(self, killer, victim, place, time):
        return False

    def manipulate(self, killer, victim, alibi_place):
        raise ValueError("Invalid manipulation: " + str(self))


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

    return first_clue, second_clue, third_clue

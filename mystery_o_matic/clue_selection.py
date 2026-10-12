"""Declarative clue selection for saved cases, independent of book layout."""

from copy import deepcopy

from mystery_o_matic.clues import (
    FOG_SOMEBODY,
    NoVisitorsClue,
    SawWhenArrivingClue,
    SawWhenLeavingClue,
    StayedClue,
    WasMurderedAfterClue,
    WasMurderedBeforeClue,
    WasMurderedBodyTwoOptionsClue,
    WasMurderedScreamClue,
    WeaponNotUsedClue,
)
from mystery_o_matic.time import Time


def select_clues(mystery, specifications):
    """Select truthful clues before process_clues mutates its lying variants.

    Movement clues must match facts derived from events. Editorial exclusions
    and time bounds must agree with the saved simulation. No executable Python
    or arbitrary class construction is accepted from the JSON.
    """
    selected = []
    murder_room = mystery.final_locations[mystery.victim]
    for specification in specifications:
        fields = dict(specification)
        kind = fields.pop("type")
        if "match" in fields:
            match = fields.pop("match")
            matches = [clue for clue in mystery.additional_clues
                       if type(clue).__name__ == kind
                       and all(str(getattr(clue, key, None)) == str(value)
                               for key, value in match.items())]
            if len(matches) != 1:
                raise ValueError(f"expected one {kind} matching {match}, found {len(matches)}")
            clue = deepcopy(matches[0])
            if "anonymous" in fields:
                anonymous = fields.pop("anonymous")
                if (not isinstance(clue, (SawWhenArrivingClue, SawWhenLeavingClue))
                        or type(anonymous) is not bool):
                    raise ValueError("anonymous requires a boolean on an arrival/departure sighting")
                clue.foggy = anonymous
                clue.fog_kind = FOG_SOMEBODY if anonymous else None
            if "activity" in fields and isinstance(clue, StayedClue):
                activity = fields.pop("activity")
                choices = mystery.stay_activities.get(clue.place.lstrip("$"), [])
                found = [item for item in choices if item.get("en") == activity]
                if len(found) != 1:
                    raise ValueError(f"unknown stay activity for {clue.place}: {activity}")
                clue.activity = found[0]
        elif kind == "WeaponNotUsedClue":
            weapon = fields.pop("weapon")
            if weapon not in mystery.weapon_locations.values() or weapon == mystery.weapon_used:
                raise ValueError(f"cannot exclude weapon {weapon}")
            clue = WeaponNotUsedClue(weapon)
        elif kind == "NoVisitorsClue":
            place = "$" + fields.pop("place").lstrip("$")
            if place.lstrip("$") not in mystery.weapon_locations or place in mystery.visited_rooms:
                raise ValueError(f"cannot declare {place} unvisited")
            clue = NoVisitorsClue(place)
        elif kind == "WasMurderedAfterClue":
            when = Time(fields.pop("time"))
            if when.seconds >= mystery.murder_time.seconds:
                raise ValueError("murder-after bound contradicts the saved murder time")
            clue = WasMurderedAfterClue(when, mystery.interval_size, True,
                                       fields.pop("alternative", True))
        elif kind == "WasMurderedBeforeClue":
            when = Time(fields.pop("time"))
            if when.seconds <= mystery.murder_time.seconds:
                raise ValueError("murder-before bound contradicts the saved murder time")
            clue = WasMurderedBeforeClue(when, mystery.interval_size, True,
                                        fields.pop("alternative", True))
        elif kind == "WasMurderedBodyTwoOptionsClue":
            first, second = Time(fields.pop("time1")), Time(fields.pop("time2"))
            if (first.seconds == second.seconds
                    or mystery.murder_time.seconds not in (first.seconds, second.seconds)):
                raise ValueError("two-option clue must include the murder time and one alternative")
            clue = WasMurderedBodyTwoOptionsClue(first, second)
        elif kind == "WasMurderedScreamClue":
            start, end = Time(fields.pop("time1")), Time(fields.pop("time2"))
            if not start.seconds <= mystery.murder_time.seconds <= end.seconds:
                raise ValueError("scream interval excludes the saved murder time")
            clue = WasMurderedScreamClue(start, end)
        else:
            raise ValueError(f"{kind} requires an event match or a supported editorial clue")
        if fields:
            raise ValueError(f"unknown {kind} fields: {', '.join(fields)}")
        if clue.is_incriminating(mystery.killer, mystery.victim, murder_room, mystery.murder_time):
            raise ValueError(f"{kind} is an incriminating statement omitted from truthful output")
        selected.append(clue)
    if not selected:
        raise ValueError("clue selection must not be empty")
    return selected

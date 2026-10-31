"""Lying permissions derived from the public statement and crime scene.

A statement can conceal the crime by describing the scene or by placing its
speaker elsewhere at the murder time. Absence from an unrelated room is not an
alibi. Bounds are inclusive seconds; None denotes an unbounded end. Hidden event
timestamps must never narrow the scope of an untimed statement.
"""

from mystery_o_matic import clues as c


def lying_scope(clue, interval_size, murder_place):
    """Return (speaker, earliest murder, latest murder), or no permission.

    The whole statement may be false when it covers the candidate crime, but
    statements outside this scope stay true, including the killer's statements.
    This uses no intended killer/time, private movement history or chosen alibi.
    """
    at_scene = getattr(clue, "place", None) == murder_place
    if isinstance(clue, c.InteractedClue):
        return (clue.subject0, None, None) if at_scene else None
    if isinstance(clue, c.NotSawWhileInClue):
        return (clue.subject, None, None) if at_scene else None
    if isinstance(clue, c.StayedClue):
        # Being elsewhere during this interval is a direct alibi.
        return clue.subject, clue.time_start.seconds, clue.time_end.seconds
    if isinstance(clue, c.FirstArrivalClue):
        # Earlier absences conceal the crime only when this is the crime scene.
        # At another room, only the claimed presence at T supplies an alibi.
        return clue.subject, None if at_scene else clue.time.seconds, clue.time.seconds
    if isinstance(clue, (c.SawWhenArrivingClue, c.SawVictimWhenArrivingClue)):
        return clue.subject, clue.time.seconds - (interval_size if at_scene else 0), clue.time.seconds
    if isinstance(clue, (c.SawWhenLeavingClue, c.SawVictimWhenLeavingClue)):
        return clue.subject, clue.time.seconds, clue.time.seconds + (interval_size if at_scene else 0)
    if isinstance(clue, c.HeardClue):
        # "I heard someone there from outside" denies presence at the crime
        # scene only when "there" is that scene, not some unrelated room.
        return (clue.subject, clue.time.seconds, clue.time.seconds) if at_scene else None
    if isinstance(clue, c.NotSawWhenArrivingLeavingClue):
        # The wording places the speaker in this room at T; no movement is stated.
        return clue.subject, clue.time.seconds, clue.time.seconds
    # Forensics and narrator statements remain reliable, even when they name
    # the candidate killer. Unknown clue types are rejected by the solver.
    return None


def may_lie_at(clue, killer, time, interval_size, murder_place):
    scope = lying_scope(clue, interval_size, murder_place)
    if scope is None:
        return False
    speaker, start, end = scope
    return (speaker == killer and (start is None or start <= time.seconds)
            and (end is None or time.seconds <= end))

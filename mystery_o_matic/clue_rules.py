"""Lying permissions derived from what a statement actually tells the reader.

Bounds are inclusive seconds; None denotes an unbounded end. Event timestamps
that are absent from the wording must never narrow the scope of a statement.
"""

from mystery_o_matic import clues as c


def statement_scope(clue, interval_size):
    if isinstance(clue, c.InteractedClue):
        return clue.subject0, None, None
    if isinstance(clue, c.NotSawWhileInClue):
        return clue.subject, None, None
    if isinstance(clue, c.StayedClue):
        return clue.subject, clue.time_start.seconds, clue.time_end.seconds
    if isinstance(clue, c.FirstArrivalClue):
        # "Not until T" asserts absence at EVERY earlier mark too.
        return clue.subject, None, clue.time.seconds
    if isinstance(clue, c.SawWhenArrivingClue) and clue.object == "$NOBODY":
        # Existing empty-arrival alibis may conceal an earlier encounter.
        return clue.subject, None, None
    if isinstance(clue, (c.SawWhenArrivingClue, c.SawVictimWhenArrivingClue)):
        return clue.subject, clue.time.seconds - interval_size, clue.time.seconds
    if isinstance(clue, (c.SawWhenLeavingClue, c.SawVictimWhenLeavingClue)):
        return clue.subject, clue.time.seconds, clue.time.seconds + interval_size
    if isinstance(clue, (c.HeardClue, c.NotSawWhenArrivingLeavingClue)):
        return clue.subject, clue.time.seconds, clue.time.seconds
    # Forensics and narrator statements remain reliable, even when they name
    # the candidate killer. Unknown clue types are rejected by the solver.
    return None


def may_lie_at(clue, killer, time, interval_size):
    scope = statement_scope(clue, interval_size)
    if scope is None:
        return False
    speaker, start, end = scope
    return (speaker == killer and (start is None or start <= time.seconds)
            and (end is None or time.seconds <= end))

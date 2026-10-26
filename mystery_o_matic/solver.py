"""Reader-facing uniqueness and randomized selection of necessary clues.

Adapted from the book's scripts/solve_case.py. Locations are unknown: the
simulation's initial positions, moves and chosen alibi are never constraints.
Only the map, final snapshot, public rules and displayed clues are used.
Uniqueness means one (killer, weapon, time), not one complete movement history.
"""

from dataclasses import dataclass
from random import Random

from z3 import And, Bool, BoolVal, FreshBool, If, Implies, Int, Not, Optimize, Or, Solver, Sum
from z3 import is_true, sat, unsat

from mystery_o_matic import clues as c
from mystery_o_matic.time import Time
from mystery_o_matic.traits import CHARACTER_DESCRIPTORS
from mystery_o_matic.weapons import get_weapon_type


def _check(solver, *assumptions):
    result = solver.check(*assumptions)
    if result not in (sat, unsat):
        raise RuntimeError("Clue solver could not decide: " + solver.reason_unknown())
    return result


def minimum_unsat_subset(solver, constraints):
    """Return a smallest set making solver unsatisfiable, or None.

    An implicit hitting-set search proves minimum cardinality (a greedy
    deletion pass alone only proves irreducibility). Each satisfiable selection
    is extended to a maximal satisfiable subset. Every solution must include a
    clue outside that subset. Optimize finds the smallest set hitting all such
    counterexamples; once it is unsatisfiable, no smaller set can suffice.
    The caller must already have excluded the intended answer.
    """
    solver.push()
    try:
        enabled = [Bool(f"clue_enabled_{i}") for i in range(len(constraints))]
        solver.add(*[Implies(flag, fact) for flag, fact in zip(enabled, constraints)])
        if _check(solver, *enabled) == sat:
            return None
        # A small initial upper bound also handles puzzles needing zero clues.
        core = set(solver.unsat_core())
        upper = [i for i, flag in enumerate(enabled) if flag in core]
        for i in upper[:]:
            trial = [j for j in upper if j != i]
            if _check(solver, *[enabled[j] for j in trial]) == unsat:
                upper = trial
        if not upper:
            return ()

        choose = [Bool(f"clue_chosen_{i}") for i in range(len(constraints))]
        search = Optimize()
        size = Sum([If(flag, 1, 0) for flag in choose])
        search.add(size <= len(upper))
        search.minimize(size)
        # Prefer earlier clues when several minimum sets exist.
        search.minimize(Sum([If(flag, i + 1, 0) for i, flag in enumerate(choose)]))
        while True:
            if _check(search) != sat:
                raise RuntimeError("Minimum clue search lost its sufficient upper bound")
            model = search.model()
            selected = [i for i, flag in enumerate(choose) if is_true(model.eval(flag))]
            if _check(solver, *[enabled[i] for i in selected]) == unsat:
                return tuple(selected)

            model = solver.model()
            accepted = {i for i, fact in enumerate(constraints)
                        if is_true(model.eval(fact, model_completion=True))}
            for i in range(len(constraints)):
                if i in accepted:
                    continue
                if _check(solver, *[enabled[j] for j in sorted(accepted | {i})]) == sat:
                    model = solver.model()
                    accepted.update(j for j, fact in enumerate(constraints)
                                    if is_true(model.eval(fact, model_completion=True)))
            search.add(Or(*[flag for i, flag in enumerate(choose) if i not in accepted]))
    finally:
        solver.pop()


@dataclass(frozen=True)
class ClueAnalysis:
    status: str
    total: int
    required: tuple = ()
    alternative: tuple = None

    @property
    def minimum(self):
        return len(self.required) if self.status == "unique" else None

    @property
    def order(self):
        if self.minimum is None:
            return tuple(range(self.total))
        required = set(self.required)
        return self.required + tuple(i for i in range(self.total) if i not in required)


@dataclass(frozen=True)
class ClueSelection:
    """Indices refer to the original pool; minimum/total describe the output.

    Every required clue is indispensable even with the retained redundant clues
    present. Thus the size of the core is the exact minimum for this selection,
    though it need not be the smallest sufficient subset of the original pool.
    """

    status: str
    pool_size: int
    required: tuple = ()
    redundant: tuple = ()
    trial_sizes: tuple = ()
    alternative: tuple = None

    @property
    def minimum(self):
        return len(self.required) if self.status == "unique" else None

    @property
    def order(self):
        return self.required + self.redundant if self.status == "unique" else tuple(range(self.pool_size))

    @property
    def total(self):
        return len(self.order)

    @property
    def omitted(self):
        retained = set(self.order)
        return tuple(i for i in range(self.pool_size) if i not in retained)

    @property
    def necessary_ratio(self):
        return self.minimum / self.total if self.status == "unique" and self.total else None


def select_necessary_subset(solver, constraints, attempts=100, seed=None, min_ratio=1 / 3,
                            max_clues=None):
    """Sample irreducible cores, then add redundancy without restoring shortcuts.

    The caller must already exclude the intended answer. Deletion in different
    orders finds different irreducible cores. Keep the largest of the sampled
    cores that fits max_clues, in its trial order, to favor combining more clues
    over short proofs. A limit never truncates a necessary core.
    This is a heuristic for puzzle difficulty, not a maximum-cardinality proof.

    Adding a redundant clue can make core clues optional. Check each addition
    against EVERY core clue, and bound the final list to meet min_ratio.
    """
    if type(attempts) is not int or attempts < 1:
        raise ValueError("clue shuffles must be a positive integer")
    if not 0 < min_ratio <= 1:
        raise ValueError("minimum necessary ratio must be greater than 0 and at most 1")
    if max_clues is not None and (type(max_clues) is not int or max_clues < 1):
        raise ValueError("maximum clues must be a positive integer")
    rng = Random(seed)
    count = len(constraints)
    solver.push()
    try:
        enabled = [FreshBool("selected_clue") for _ in constraints]
        solver.add(*[Implies(flag, fact) for flag, fact in zip(enabled, constraints)])
        cache = {}

        def has_alternative(indices):
            key = frozenset(indices)
            if key not in cache:
                cache[key] = _check(solver, *[enabled[i] for i in sorted(key)]) == sat
            return cache[key]

        if has_alternative(range(count)):
            return ClueSelection("ambiguous", count)
        if not has_alternative(()):
            return ClueSelection("trivial", count)

        best, best_order, sizes = (), (), []
        for trial in range(attempts):
            order = list(range(count))
            if trial:
                rng.shuffle(order)
            active = set(order)
            # Prefer earlier clues in this trial's order when they substitute
            # for later ones. Do not use an unsat core, which would bias trials
            # towards Z3's preferred short proofs before we even shuffle.
            for i in reversed(order):
                active.remove(i)
                if has_alternative(active):
                    active.add(i)
            core = tuple(i for i in order if i in active)
            sizes.append(len(core))
            if len(core) > len(best) and (max_clues is None or len(core) <= max_clues):
                best, best_order = core, order

        if not best:
            raise ValueError(
                f"No sufficient clue set within --max-clues {max_clues} found in "
                f"{attempts} deletion orders (smallest sampled core: {min(sizes)}). "
                "Increase --max-clues or --clue-shuffles."
            )
        required = set(best)
        redundant = []
        for i in best_order:
            if max_clues is not None and len(best) + len(redundant) >= max_clues:
                break
            if i in required:
                continue
            if len(best) / (len(best) + len(redundant) + 1) < min_ratio:
                break
            enlarged = required | set(redundant) | {i}
            if all(has_alternative(enlarged - {essential}) for essential in best):
                redundant.append(i)
        return ClueSelection("unique", count, best, tuple(redundant), tuple(sizes))
    finally:
        solver.pop()


class ClueSolver:
    """Symbolic version of the book's one-period, map-constrained model.

    The victim remains at the scene; the killer is alone with them at the
    murder mark and privately retrieves a weapon in an earlier period. No
    one-mover-per-tick or extra stay after the crime is assumed. The optional
    killer_leaves rule is printed in the website's opening facts, but omitted
    from book exports, so it is off by default.

    In lying mode, only candidate-killer statements covering the murder may be
    ignored. Empty-arrival alibis and first-arrival claims before the murder can
    also be fabricated by the generator. Evidence is always trustworthy.
    """

    def __init__(self, mystery, graph, clues, with_lies=False, killer_leaves=False):
        self.mystery = mystery
        self.clues = list(clues)
        self.chars = list(mystery.cplaceholders)
        self.ci = {char: i for i, char in enumerate(self.chars)}
        self.rooms = ["$" + room.lstrip("$") for room in graph.nodes]
        self.ri = {room: i for i, room in enumerate(self.rooms)}
        self.weapons = list(mystery.weapon_locations.values())
        self.wi = {weapon: i for i, weapon in enumerate(self.weapons)}
        self.times = list(range(mystery.initial_time.seconds,
                                mystery.final_time.seconds + 1, mystery.interval_size))
        self.ti = {time: i for i, time in enumerate(self.times)}
        if (not self.times or self.times[-1] != mystery.final_time.seconds
                or len(self.wi) != len(self.weapons)):
            raise ValueError("Invalid timeline or duplicate weapon locations")
        self.solver = Solver()
        self.killer, self.weapon, self.murder = Int("killer"), Int("weapon"), Int("murder")
        self.clock = self.times[0] + self.murder * mystery.interval_size
        self.loc = {char: [Int(f"loc_{i}_{t}") for t in range(len(self.times))]
                    for i, char in enumerate(self.chars)}
        self.victim = mystery.victim
        scene = self.ri[mystery.final_locations[self.victim]]
        s = self.solver
        s.add(self.killer >= 0, self.killer < len(self.chars),
              self.killer != self.ci[self.victim], self.weapon >= 0,
              self.weapon < len(self.weapons), self.murder >= 0,
              self.murder < len(self.times))
        edges = set()
        for a, b in graph.edges:
            a, b = self.ri["$" + a.lstrip("$")], self.ri["$" + b.lstrip("$")]
            edges.update(((a, b), (b, a)))
        for char, path in self.loc.items():
            for pos in path:
                s.add(pos >= 0, pos < len(self.rooms))
            for before, after in zip(path, path[1:]):
                s.add(Or(before == after, *[And(before == a, after == b)
                                            for a, b in sorted(edges)]))
            s.add(path[-1] == self.ri[mystery.final_locations[char]])
            if char == self.victim:
                for t, pos in enumerate(path):
                    s.add(Implies(self.murder <= t, pos == scene))
                continue
            for t, pos in enumerate(path):
                s.add(Implies(self.murder == t, (pos == scene) == (self.killer == self.ci[char])))
            if killer_leaves:
                s.add(Implies(self.killer == self.ci[char], path[-1] != scene))
            for room, weapon in mystery.weapon_locations.items():
                r = self.ri["$" + room.lstrip("$")]
                pickups = [And(t < self.murder, path[t] == r,
                               *[self.loc[other][t] != r for other in self.chars if other != char])
                           for t in range(len(self.times) - 1)]
                s.add(Implies(And(self.killer == self.ci[char], self.weapon == self.wi[weapon]),
                              Or(*pickups)))

        self.constraints = []
        for clue in self.clues:
            fact = self._clue(clue)
            if with_lies:
                fact = Or(self._unreliable(clue), fact)
            self.constraints.append(fact)

    def _time(self, time):
        try:
            return self.ti[time.seconds]
        except KeyError:
            raise ValueError(f"Clue time {time} is outside the puzzle timeline") from None

    def _living(self, char, t):
        # The murder mark includes the victim's last living encounter.
        return self.murder >= t if char == self.victim else BoolVal(True)

    def _seen_candidates(self, clue):
        kind = clue.fog_kind
        if not kind:
            return [clue.object]
        if kind == c.FOG_TRAIT:
            trait = self.mystery.character_traits[clue.object]["id"]
            return [char for char in self.chars if self.mystery.character_traits[char]["id"] == trait]
        if kind == c.FOG_DESCRIPTOR:
            names = dict(zip(self.chars, self.mystery.characters))
            descriptor = CHARACTER_DESCRIPTORS[names[clue.object]]
            return [char for char in self.chars if CHARACTER_DESCRIPTORS[names[char]] == descriptor]
        if kind in (c.FOG_HAT_YES, c.FOG_HAT_NO, c.FOG_GLASSES_YES, c.FOG_GLASSES_NO):
            prop, value = kind.split("_")
            return [char for char in self.chars
                    if bool(self.mystery.character_traits[char].get(prop)) == (value == "yes")]
        if kind == c.FOG_SOMEBODY:
            return self.chars
        raise ValueError("Unknown sighting description: " + str(kind))

    def _unreliable(self, clue):
        if isinstance(clue, (c.EvidenceClue, c.NoVisitorsClue)):
            return BoolVal(False)
        subject = clue.subject
        if subject not in self.ci:
            return BoolVal(False)
        if isinstance(clue, c.StayedClue):
            covering = And(self.clock >= clue.time_start.seconds, self.clock <= clue.time_end.seconds)
        elif isinstance(clue, c.SawWhenArrivingClue) and clue.object == "$NOBODY":
            covering = BoolVal(True)
        elif isinstance(clue, c.FirstArrivalClue):
            covering = self.clock >= clue.time.seconds
        elif clue.time is not None:
            covering = self.clock == clue.time.seconds
        else:
            return BoolVal(False)
        return And(self.killer == self.ci[subject], covering)

    def _clue(self, clue):
        if isinstance(clue, c.WeaponNotUsedClue):
            kind = get_weapon_type(clue.weapon)
            excluded = [clue.weapon] if kind == "poisoning" else [
                weapon for weapon in self.weapons if get_weapon_type(weapon) == kind]
            return And(*[self.weapon != self.wi[weapon] for weapon in excluded])
        if isinstance(clue, c.WasMurderedBodyTwoOptionsClue):
            return Or(self.clock == clue.time1.seconds, self.clock == clue.time2.seconds)
        if isinstance(clue, c.WasMurderedScreamClue):
            return And(self.clock >= clue.time1.seconds, self.clock <= clue.time2.seconds)
        if isinstance(clue, (c.WasMurderedAfterClue, c.WasVictimAliveAtClue)):
            if isinstance(clue, c.WasMurderedAfterClue) and not clue.positive:
                return self.clock >= clue.time.seconds + clue.interval_size
            return self.clock > clue.time.seconds
        if isinstance(clue, (c.WasMurderedBeforeClue, c.WasVictimDeadAtClue)):
            if isinstance(clue, c.WasMurderedBeforeClue) and not clue.positive:
                return self.clock <= clue.time.seconds - clue.interval_size
            return self.clock < clue.time.seconds

        if isinstance(clue, c.HeardClue) and clue.place is None:
            raise ValueError("HeardClue must retain its room for solving")
        if clue.place not in self.ri:
            raise ValueError(f"Unknown room on {type(clue).__name__}: {clue.place}")
        r = self.ri[clue.place]
        if isinstance(clue, c.NoVisitorsClue):
            return And(*[pos != r for path in self.loc.values() for pos in path])
        if isinstance(clue, c.InteractedClue):
            # The time in the event is NOT displayed to the reader.
            return Or(*[And(self.loc[clue.subject0][t] == r, self.loc[clue.subject1][t] == r,
                            self._living(clue.subject0, t), self._living(clue.subject1, t))
                        for t in range(len(self.times))])

        path = self.loc[clue.subject]
        if isinstance(clue, c.StayedClue):
            return And(*[path[t] == r for t in range(self._time(clue.time_start), self._time(clue.time_end) + 1)])
        if isinstance(clue, c.EvidenceClue):
            return Or(*[And(pos == r, self._living(clue.subject, t)) for t, pos in enumerate(path)])
        if isinstance(clue, c.NotSawWhileInClue):
            return And(Or(*[pos == r for pos in path]),
                       *[Or(pos != r, self.loc[clue.object][t] != r) for t, pos in enumerate(path)])

        timed_types = (c.FirstArrivalClue, c.NotSawWhenArrivingLeavingClue, c.HeardClue,
                       c.SawVictimWhenArrivingClue, c.SawVictimWhenLeavingClue,
                       c.SawWhenArrivingClue, c.SawWhenLeavingClue)
        if not isinstance(clue, timed_types):
            raise ValueError("Unsupported clue type: " + type(clue).__name__)
        t = self._time(clue.time)
        if isinstance(clue, c.FirstArrivalClue):
            return And(path[t] == r, *[pos != r for pos in path[:t]])
        if isinstance(clue, c.NotSawWhenArrivingLeavingClue):
            # The rendered absence says nothing about arriving or leaving.
            return And(path[t] == r, self.loc[clue.object][t] != r)
        if isinstance(clue, c.HeardClue):
            return And(path[t] != r, Or(*[And(self.loc[other][t] == r, self._living(other, t))
                                         for other in self.chars if other != clue.subject]))
        if isinstance(clue, (c.SawVictimWhenArrivingClue, c.SawVictimWhenLeavingClue)):
            # The victim moves, while the surviving witness is in the room.
            step = t - 1 if isinstance(clue, c.SawVictimWhenArrivingClue) else t + 1
            facts = [path[t] == r, self.loc[clue.object][t] == r]
            if 0 <= step < len(self.times):
                facts.append(self.loc[clue.object][step] != r)
            return And(*facts)
        if isinstance(clue, (c.SawWhenArrivingClue, c.SawWhenLeavingClue)):
            step = t - 1 if isinstance(clue, c.SawWhenArrivingClue) else t + 1
            facts = [path[t] == r]
            if 0 <= step < len(self.times):
                facts.append(path[step] != r)
            if clue.object == "$NOBODY":
                facts.extend(self.loc[other][t] != r for other in self.chars if other != clue.subject)
            elif not clue.object_is_alive:
                facts.extend((self.loc[clue.object][t] == r, self.murder <= t))
            else:
                facts.append(Or(*[And(self.loc[other][t] == r, self._living(other, t))
                                  for other in self._seen_candidates(clue) if other != clue.subject]))
            return And(*facts)
        raise ValueError("Unsupported clue type: " + type(clue).__name__)

    def answer(self, model):
        return (self.chars[model.eval(self.killer).as_long()],
                self.weapons[model.eval(self.weapon).as_long()],
                str(Time(self.times[model.eval(self.murder).as_long()])))

    def _expected(self):
        return And(self.killer == self.ci[self.mystery.killer],
                   self.weapon == self.wi[self.mystery.weapon_used],
                   self.clock == self.mystery.murder_time.seconds)

    def _diagnose(self):
        s = self.solver
        s.push()
        try:
            s.add(*self.constraints)
            if _check(s, self._expected()) == unsat:
                return ClueAnalysis("inconsistent", len(self.clues))
            if _check(s, Not(self._expected())) == sat:
                return ClueAnalysis("ambiguous", len(self.clues), alternative=self.answer(s.model()))
        finally:
            s.pop()

    def analyze(self):
        """Find the exact global minimum in the full input pool, for audits."""
        problem = self._diagnose()
        if problem is not None:
            return problem
        s = self.solver
        s.push()
        try:
            s.add(Not(self._expected()))
            required = minimum_unsat_subset(s, self.constraints)
        finally:
            s.pop()
        return ClueAnalysis("unique", len(self.clues), required)

    def select(self, attempts=100, seed=None, min_ratio=1 / 3, max_clues=None):
        """Choose a sufficient list with the requested fraction indispensable."""
        problem = self._diagnose()
        if problem is not None:
            return ClueSelection(problem.status, len(self.clues), alternative=problem.alternative)
        self.solver.push()
        try:
            self.solver.add(Not(self._expected()))
            return select_necessary_subset(self.solver, self.constraints, attempts, seed,
                                           min_ratio, max_clues)
        finally:
            self.solver.pop()


def order_clues(mystery, graph, include_lies=True, killer_leaves=False,
                attempts=100, min_ratio=1 / 3, max_clues=None):
    """Select necessary clues first, followed by bounded, verified redundancy.

    Operate on the same objects whose translations are exported. Separate RNGs
    derived from the puzzle seed keep both variants reproducible without
    consuming the generator's global random stream. Fail before export if the
    case cannot meet the necessity requirement.
    """
    variants = [("truthful", "additional_clues", "clue_objects", False)]
    if include_lies:
        variants.append(("with lies", "additional_clues_with_lies", "clue_objects_with_lies", True))
    mystery.clue_analysis = {}
    for label, texts_attr, objects_attr, with_lies in variants:
        objects = getattr(mystery, objects_attr)
        texts = getattr(mystery, texts_attr)
        result = ClueSolver(mystery, graph, objects, with_lies, killer_leaves).select(
            attempts=attempts,
            seed=f"{getattr(mystery, 'used_seed', None)}-necessary-clues-{label}",
            min_ratio=min_ratio,
            max_clues=max_clues,
        )
        mystery.clue_analysis[texts_attr] = result
        if result.minimum is not None:
            setattr(mystery, objects_attr, [objects[i] for i in result.order])
            setattr(mystery, texts_attr, [texts[i] for i in result.order])
            print(f"Necessary clues ({label}): {result.minimum} of {result.total} "
                  f"({result.necessary_ratio:.1%}); {len(result.redundant)} redundant, "
                  f"{len(result.omitted)} omitted from {result.pool_size}", flush=True)
            print(f"  {len(result.trial_sizes)} deletion orders: sufficient cores ranged from "
                  f"{min(result.trial_sizes)} to {max(result.trial_sizes)} clues; "
                  "every chosen core clue remains necessary in the final list", flush=True)
        else:
            reasons = {
                "ambiguous": f"the full clue pool allows another answer: {result.alternative}",
                "inconsistent": "the clue pool contradicts the generated answer",
                "trivial": "the fixed public facts already solve the case without any clues",
            }
            raise ValueError(f"Cannot select necessary clues ({label}): {reasons[result.status]}")

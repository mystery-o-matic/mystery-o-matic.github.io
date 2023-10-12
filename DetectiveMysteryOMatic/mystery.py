from datetime import timedelta
from random import shuffle
from hashlib import sha256

from DetectiveMysteryOMatic.clues import Clue
from DetectiveMysteryOMatic.solidity import get_tx, get_event
from DetectiveMysteryOMatic.text import get_char_name

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
	interval_size = 15 * 60 # 15 minutes
	final_time = ""

	def __init__(self, initial_locations, weapon_locations, weapon_used, source, txs):
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

	def load_events(self, events):
		event_calls = []
		for event in events:
			event_calls.append(get_event(self.source, "StoryModel", event))

		for call in event_calls:
			if call[0].startswith("NotSaw") and call[1] == self.victim:
				continue
			# victim clues should be modified
			elif call[0].startswith("Saw") and call[1] == self.victim:
				if call[2] == "$NOBODY": # No witnesses
					continue
				elif call[0] == "SawWhenLeaving": # TODO
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

			if (call[0] == "WasMurdered"):
				self.initial_clues.append(Clue(call[0], [call[1], call[2]]))
				self.murder_time = call[3]
			elif (call[0] == "PoliceArrived"):
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

		shuffle(self.additional_clues)

	def get_intervals(self):
		intervals = []
		initial_seconds = self._time_to_seconds(self.initial_time)
		final_seconds = self._time_to_seconds(self.final_time)

		for t in range(initial_seconds, final_seconds + 1, self.interval_size):
			delta = timedelta(seconds = t)
			h, m, _ = str(delta).split(":")
			intervals.append(h + ":" + m)

		return intervals

	def _time_to_seconds(self, t):
		h, m = map(int, t.split(':'))
		return h * 3600 + m * 60

	def get_answer(self):
		index = int("".join(filter(str.isdigit, self.killer))) - 1
		return self.characters[index] + "-" + self.weapon_used + "-" + self.murder_time

	def get_answer_hash(self):
		answer = self.get_answer()
		print("Answer is:", answer)
		m = sha256()
		m.update(answer.encode('utf-8'))
		return(m.hexdigest())

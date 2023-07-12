from random import randint

class Clue:
	name = ""
	fields = []
	def __init__(self, name, fields):
		self.name = name
		self.fields = fields
		r = randint(1, 10)
		self.foggy = False
		if (r <= 5):
			self.foggy = True

	def __str__(self):
		if (self.name == "SawWhenArriving"):
			return self.print_SawWhenArriving_clue()
		elif (self.name == "NotSawWhenArriving"):
			return self.print_NotSawWhenArrivingLeaving_clue()
		elif (self.name == "SawVictimWhenArriving"):
			return self.print_SawVictimWhenArriving_clue()
	#	elif (name == "SawVictimWhenLeaving"):
	#		return "{} said: \"I saw {} leaving to {} at {}\"".format(clue[1], clue[2], clue[3], clue[4])
		elif (self.name == "SawWhenLeaving"):
			return self.print_SawWhenLeaving_clue()
		elif (self.name == "NotSawWhenLeaving"):
			return self.print_NotSawWhenArrivingLeaving_clue()
		elif (self.name == "WasMurdered"):
			return "{} was murdered in the {} between {} and {}!".format(self.fields[0], self.fields[1], self.fields[2], self.fields[3])
		elif (self.name == "PoliceArrived"):
			return "Police arrived at {}!".format(self.fields[0])
		elif (self.name == "Stayed"):
			return self.print_Stayed_clue()
		elif (self.name == "WeaponNotUsed"):
			return self.print_WeaponNotUsed_clue()
		else:
			print("Invalid clue!", self.name, self.fields)
			assert(False)

	def is_incriminating(self, killer, victim):
		if (self.name == "SawWhenArriving" and self.fields[0] == killer and self.fields[1] == victim):
			return True
		elif (self.name == "SawWhenLeaving" and self.fields[0] == killer and self.fields[1] == victim and not self.fields[2]):
			return True
		elif (self.name == "SawVictimWhenArriving" and self.fields[0] == killer and self.fields[1] == victim):
			return True
		return False

	def print_SawVictimWhenArriving_clue(self):
		str = "{} said: \"I saw "
		if not self.fields[2]:
			str += "the body of "

		str += "{} arriving to the {} at {}\""
		return str.format(self.fields[0], self.fields[1], self.fields[3], self.fields[4])

	def print_SawWhenLeaving_clue(self):
		r = randint(0, 3)
		str = "{} said \""

		if (self.fields[1] == "$NOBODY"):
			r = 0

		if (r == 0):
			str += "I saw "
		elif (r == 1):
			str += "I think I saw "
		elif (r == 2):
			str += "I'm sure I saw "
		elif (r == 3):
			str += "I remember "
		else:
			assert(False)

		if not self.fields[2]:
			str += "the body of "

		if (self.foggy and self.fields[2]):
			if (self.fields[1] is not "$NOBODY"):
				self.fields[1] = "somebody"

		str += "{} when I was leaving the {} at {}\""
		return str.format(self.fields[0], self.fields[1], self.fields[3], self.fields[4])

	def print_SawWhenArriving_clue(self):
		r = randint(0, 3)
		str = "{} said \""

		if (self.fields[1] == "$NOBODY"):
			r = 0

		if (r == 0):
			str += "I saw "
		elif (r == 1):
			str += "I think I saw "
		elif (r == 2):
			str += "I'm sure I saw "
		elif (r == 3):
			str += "I remember "
		else:
			assert(False)

		if not self.fields[2]:
			str += "the body of "

		if (self.foggy and self.fields[2]):
			if (self.fields[1] is not "$NOBODY"):
				self.fields[1] = "somebody"

		str += "{} when I arrived to the {} at {}\""
		return str.format(self.fields[0], self.fields[1], self.fields[3], self.fields[4])

	def print_NotSawWhenArrivingLeaving_clue(self):
		r = randint(0, 2)
		str = "{} said: \""

		if (r == 0):
			str += " "
		elif (r == 1):
			str += "I don't think "
		elif (r == 2):
			str += "I'm sure "
		else:
			assert(False)

		str += "{} was not in the {} at {}\""
		return str.format(self.fields[0], self.fields[1], self.fields[2], self.fields[3])

	def print_WeaponNotUsed_clue(self):
		r = randint(0, 2)

		if (r == 0):
			str = "Inspecting the body reveals that the {} was not the murderer weapon"
			return str.format(self.fields[0])
		elif (r == 1):
			str = "The inspection of the body indicates that the {} was not the weapon employed by the killer."
			return str.format(self.fields[0])
		elif (r == 2):
			str = "When inspecting the body, it becomes clear that the {} was not the weapon used by the murderer."
			return str.format(self.fields[0])
		else:
			assert(False)

	def print_Stayed_clue(self):
		r = randint(0, 2)

		if (r == 0):
			str = "{} said: \"I was in the {} from {} to {}\""
			return str.format(self.fields[0], self.fields[1], self.fields[2], self.fields[3])
		elif (r == 1):
			str = "\"I was in the {} from {} to {}\" stated {}"
			return str.format(self.fields[1], self.fields[2], self.fields[3], self.fields[0])
		elif (r == 2):
			str = "\"I stayed in the {} from {} to {}\" claimed {}"
			return str.format(self.fields[1], self.fields[2], self.fields[3], self.fields[0])
		else:
			assert(False)


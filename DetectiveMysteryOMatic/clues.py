class Clue:
	name = ""
	fields = []
	def __init__(self, name, fields):
		self.name = name
		self.fields = fields

	def __str__(self):
		if (self.name == "SawWhenArriving"):
			str = "{} said: \"I saw "
			if not self.fields[2]:
				str += "the body of "

			str += "{} when I was arriving to the {} at {}\""
			return str.format(self.fields[0], self.fields[1], self.fields[3], self.fields[4])

		elif (self.name == "SawVictimWhenArriving"):
			str = "{} said: \"I saw "
			if not self.fields[2]:
				str += "the body of "

			str += "{} arriving to the {} at {}\""
			return str.format(self.fields[0], self.fields[1], self.fields[3], self.fields[4])
	#	elif (name == "SawVictimWhenLeaving"):
	#		return "{} said: \"I saw {} leaving to {} at {}\"".format(clue[1], clue[2], clue[3], clue[4])
		elif (self.name == "SawWhenLeaving"):
			str = "{} said: \"I saw "
			if not self.fields[2]:
				str += "the body of "

			str += "{} when I was leaving the {} at {}\""
			return str.format(self.fields[0], self.fields[1], self.fields[3], self.fields[4])
		elif (self.name == "WasMurdered"):
			return "{} was murdered in the {} between {} and {}!".format(self.fields[0], self.fields[1], self.fields[2], self.fields[3])
		elif (self.name == "PoliceArrived"):
			return "Police arrived at {}!".format(self.fields[0])
		elif (self.name == "Stayed"):
			str = "{} said: \"I was in the {} at {}\""
			return str.format(self.fields[0], self.fields[1], self.fields[2])
		elif (self.name == "WeaponNotUsed"):
			str = "Inspecting the body reveals that the {} was not the murderer weapon"
			return str.format(self.fields[0])
		else:
			print("Invalid clue!", self.name, self.fields)
			assert(false)

	def is_incriminating(self, killer, victim):
		if (self.name == "SawWhenArriving" and self.fields[0] == killer and self.fields[1] == victim):
			return True
		elif (self.name == "SawWhenLeaving" and self.fields[0] == killer and self.fields[1] == victim and not self.fields[2]):
			return True
		elif (self.name == "SawVictimWhenArriving" and self.fields[0] == killer and self.fields[1] == victim):
			return True
		return False



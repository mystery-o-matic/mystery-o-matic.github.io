import cmd

from DetectiveMysteryOMatic.output import create_template

class DetectiveShell(cmd.Cmd):
	prompt = '? '
	current_clue = 0

	def __init__(self, intro, clues, locations, answer, args, completekey='tab', stdin=None, stdout=None):
		super().__init__(completekey, stdin, stdout)
		self.intro = intro
		self.clues = clues
		self.args = args
		self.locations = locations
		self.answer = answer

	def do_clue(self, arg):
		'Provide next clue'
		if self.current_clue < len(self.clues):
			clue = create_template(str(self.clues[self.current_clue])).substitute(self.args)
			self.current_clue += 1
		else:
			clue = "No more clues!"
		print(clue)

	def do_locations(self, arg):
		for src in self.locations.nodes:
			connections = []
			for dst in self.locations[src]:
				connections.append(dst.lower())
			print("*", src.lower(), "is connected with", ", ".join(connections))

	def do_solve(self, arg):
		print(repr(arg), repr(self.answer))
		if (self.answer == arg):
			print("Correct answer!")
			return True
		else:
			print("Wrong answer or invalid format (name-weapon-time).")

	def do_exit(self, arg):
		return True

def produce_text_output(static_dir, out_dir, mystery, weapon_locations, locations, story_clue):
	txt_source = []
	txt_source.append("Initial clues are:")
	for i, clue in enumerate(mystery.initial_clues):
		txt_source.append("* " + str(clue))

	txt_source.append("* The murderer was alone with their victim and the body was not moved")
	txt_source.append("* The killer took the murder weapon from one of these rooms:")
	for loc, weapon in weapon_locations.items():
		txt_source.append("  - The {} from the ${}".format(weapon, loc))

	txt_source.append("* When the police arrived at {}:".format(mystery.final_time))

	for (c, p) in mystery.final_locations.items():
		txt_source.append("  - {} was in the {}".format(c, p))

	args = dict()
	for i, char in enumerate(mystery.get_characters()):
		args["CHAR" + str(i + 1)] = char.capitalize()

	args["NOBODY"] = "nobody"
	args["BEDROOM"] = "bedroom"
	args["LIVING"] = "living room"
	args["KITCHEN"] = "kitchen"
	args["BATHROOM"] = "bathroom"
	print(mystery.get_answer())

	txt_output = create_template("\n".join(txt_source)).substitute(args)
	DetectiveShell(txt_output, mystery.additional_clues, locations, mystery.get_answer(), args).cmdloop()
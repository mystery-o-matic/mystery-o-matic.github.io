#!/usr/bin/python3

from sys import argv, exit

from DetectiveMysteryOMatic.html import read_html_template, create_template, build_website, get_bullet_list, get_options_selector, get_subtitle, get_accordion, get_char_name
from DetectiveMysteryOMatic.echidna import create_outdir
from DetectiveMysteryOMatic.location import create_locations_graph, render_locations, mansion_locations, weapon_locations
from DetectiveMysteryOMatic.mystery import Mystery
from DetectiveMysteryOMatic.model import Model

def main() -> int:
	if (len(argv) != 4):
		return 1

	print("Welcome to mystery-o-matic!")
	solidity_file = argv[1]
	static_dir = argv[2]
	out_dir = argv[3]

	create_outdir(out_dir)
	locations = create_locations_graph(out_dir, mansion_locations)

	html_template = read_html_template(static_dir + "/index.template.html")

	model = Model("StoryModel", locations, out_dir, solidity_file)
	(initial_locations_pairs, final_locations_pairs, weapon_location) = model.generate_conditions()
	solidity_file = model.generate_solidity()

	print("Running the simulation..")
	result = model.solve()

	if result is None:
		return 1

	txs = (result["tests"][0]["transactions"])

	events = []
	if "events" in result["tests"][0]:
		events = result["tests"][0]["events"]

	weapon_used = weapon_locations[weapon_location]
	mystery = Mystery(initial_locations_pairs, final_locations_pairs, weapon_used, model.source, txs)
	mystery.load_events(events)
	mystery.process_clues()
	intervals = mystery.get_intervals()
	select_suspects = get_options_selector(mystery.get_characters())
	select_intervals = get_options_selector(intervals)
	select_weapons = get_options_selector(map(lambda n: weapon_locations[n], locations.nodes()))

	intro = ""
	bullets = ["The murderer was alone with their victim and the body was not moved"]
	for i, clue in enumerate(mystery.initial_clues):
		bullets.append(str(clue))

	sub_bullets = []
	for loc, weapon in weapon_locations.items():
		sub_bullets.append("The {} was in the ${}".format(weapon, loc))

	weapon_locations_bullets = "At {}, some potential weapons were around:\n".format(mystery.initial_time)
	weapon_locations_bullets += get_bullet_list(sub_bullets)
	bullets.append(weapon_locations_bullets)

	sub_bullets = []
	for (c, p) in mystery.final_locations:
		sub_bullets.append("{} was in the {}".format(c, p))

	final_locations_bullets = "When the police arrived at {}:\n".format(mystery.final_time)
	final_locations_bullets += get_bullet_list(sub_bullets)
	bullets.append(final_locations_bullets)

	initial_clues = get_bullet_list(bullets)

	additional_clues = ""

	for i, clue in enumerate(mystery.additional_clues):
		additional_clues += get_accordion("Clue #{}".format(i+1), str(clue), i+1) + "\n"

	correct_answer = mystery.get_answer_hash()

	html_source = html_template.substitute(initialClues = initial_clues, clues = additional_clues, selectIntervals = select_intervals, selectSuspects = select_suspects, selectWeapon = select_weapons, numIntervals = str(len(intervals)), suspectNames = str(mystery.get_characters()), correctAnswer = correct_answer)

	args = {}
	for i, char in enumerate(mystery.get_characters()):
		args["CHAR" + str(i + 1)] = get_char_name(char)
	args["NOBODY"] = "nobody"

	args["BEDROOM"] = "bedroom"
	args["LIVING"] = "living"
	args["KITCHEN"] = "kitchen"
	args["BATHROOM"] = "bathroom"

	html_source = create_template(html_source).substitute(args)
	build_website(out_dir, static_dir, html_source)
	render_locations(out_dir, locations)

	print("Solution:")

	print(" Initial locations:")
	for (c, p) in mystery.initial_locations:
		print("  * {} was in the {}".format(c, p))

	for action in mystery.solution:
		print(action)
	return 0

if __name__ == '__main__':
	sys.exit(main())

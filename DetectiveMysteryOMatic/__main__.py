#!/usr/bin/python3

from sys import argv, exit
from argparse import ArgumentParser
from random import seed
from datetime import datetime

from DetectiveMysteryOMatic.html import read_story, read_html_template, create_template, build_website, get_bullet_list, get_options_selector, get_subtitle, get_accordion, get_char_name
from DetectiveMysteryOMatic.echidna import create_outdir
from DetectiveMysteryOMatic.location import create_locations_graph, create_locations_weapons, render_locations, mansion_locations
from DetectiveMysteryOMatic.mystery import Mystery
from DetectiveMysteryOMatic.model import Model

def main() -> int:

	parser = ArgumentParser(description='mystery-o-matic')
	parser.add_argument('scenario', type=str, action='store',
						help='path to mystery scenario')
	parser.add_argument('static_dir', type=str, action='store',
						help='path to folder with static files)')
	parser.add_argument('out_dir', type=str, action='store',
						help='path to output folder')

	parser.add_argument('--seed', type=int, action='store',
						help='seed for randomness')

	parser.add_argument('--today', action='store_const',
						const=True, help='generate the mystery for the day')

	parser.add_argument('--season', action='store',
						default=1, help='season number')

	parser.add_argument('--workers', type=int, action='store',
						default=6, help='number of workers')

	args = parser.parse_args()

	print("Welcome to mystery-o-matic!")
	solidity_file = args.scenario
	static_dir = args.static_dir
	out_dir = args.out_dir
	used_seed = args.seed
	workers = args.workers
	season = args.season
	date = datetime.today().strftime('%d-%m-%Y')

	print(date, season)
	if args.today:
		assert(used_seed is None)
		used_seed = abs(hash(date))

	if (used_seed is not None):
		seed(used_seed)

	create_outdir(out_dir)
	locations = create_locations_graph(out_dir, mansion_locations)
	weapon_locations = create_locations_weapons()
	story_clue = read_story(season, date)

	html_template = read_html_template(static_dir + "/index.template.html")

	model = Model("StoryModel", locations, out_dir, solidity_file)
	(initial_locations_pairs, weapon_location) = model.generate_conditions()
	solidity_file = model.generate_solidity()

	print("Running the simulation..")
	result = model.solve(used_seed, workers)

	if result is None:
		return 1

	txs = (result["tests"][0]["transactions"])

	events = []
	if "events" in result["tests"][0]:
		events = result["tests"][0]["events"]

	weapon_used = weapon_locations[weapon_location]
	mystery = Mystery(initial_locations_pairs, weapon_locations, weapon_used, model.source, txs)
	mystery.load_events(events)
	mystery.process_clues()
	intervals = mystery.get_intervals()
	select_suspects = get_options_selector(mystery.get_characters())
	select_intervals = get_options_selector(intervals)
	select_weapons = get_options_selector(map(lambda n: weapon_locations[n], locations.nodes()))

	intro = ""
	bullets = []
	for i, clue in enumerate(mystery.initial_clues):
		bullets.append(str(clue))

	bullets.append("The murderer was alone with their victim and the body was not moved")

	sub_bullets = []
	for loc, weapon in weapon_locations.items():
		sub_bullets.append("The {} from the ${}".format(weapon, loc))

	weapon_locations_bullets = "The killer took the murder weapon from one of these rooms:\n"
	weapon_locations_bullets += get_bullet_list(sub_bullets)
	bullets.append(weapon_locations_bullets)

	sub_bullets = []
	for (c, p) in mystery.final_locations.items():
		sub_bullets.append("{} was in the {}".format(c, p))

	final_locations_bullets = "When the police arrived at {}:\n".format(mystery.final_time)
	final_locations_bullets += get_bullet_list(sub_bullets)
	bullets.append(final_locations_bullets)

	initial_clues = get_bullet_list(bullets)

	additional_clues = ""

	for i, clue in enumerate(mystery.additional_clues):
		additional_clues += get_accordion("Clue #{}".format(i+1), str(clue), i+1) + "\n"

	correct_answer = mystery.get_answer_hash()

	args = {}
	args["initialClues"] = initial_clues
	args["mysteryClues"] = additional_clues
	args["selectIntervals"] = select_intervals
	args["selectSuspects"] =  select_suspects
	args["selectWeapon"] = select_weapons
	args["numIntervals"] = str(len(intervals))
	args["suspectNames"] = str(mystery.get_characters())
	args["correctAnswer"] = correct_answer
	args["storyClue"] = story_clue

	html_source = html_template.substitute(args)
	args = {}
	for i, char in enumerate(mystery.get_characters()):
		args["CHAR" + str(i + 1)] = get_char_name(char)
	args["NOBODY"] = "nobody"

	args["BEDROOM"] = "bedroom"
	args["LIVING"] = "living room"
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

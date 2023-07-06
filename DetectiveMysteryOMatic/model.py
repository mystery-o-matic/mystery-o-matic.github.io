from json import loads
from random import choice

from DetectiveMysteryOMatic.solidity import read_sol_template, read_solidity, save_solidity, get_enum
from DetectiveMysteryOMatic.echidna import create_echidna_process, create_outdir

class Model:
	contract_name = ""
	outdir = ""
	source = ""
	solidity_filename = ""
	weapon_location_condition = ""
	connection_conditions = ""
	initial_locations_conditions = ""

	def __init__(self, contract_name, locations, outdir, solidity_file):
		self.contract_name = contract_name
		self.locations = locations
		self.outdir = outdir
		self.source = read_solidity(solidity_file)
		self.template = read_sol_template(solidity_file)

	def generate_conditions(self):
		self.connection_conditions = self.generate_location_connections()
		self.weapon_location_condition = self.generate_weapon_condition()

		initial_locations_pairs = self.get_location_conditions()
		self.initial_locations_conditions = self.generate_location_conditions(initial_locations_pairs, "currentLocation")

		return (initial_locations_pairs, self.weapon_location)

	def generate_solidity(self):
		solidity_source = self.template.substitute(connectionLocations = self.connection_conditions, currentLocations = self.initial_locations_conditions, locationWeapon = self.weapon_location_condition)
		return save_solidity(self.outdir, solidity_source)

	def generate_location_connections(self):
		r = ""
		for (p0, p1) in self.locations.edges:
			r = r + "connection[Place.{}][Place.{}] = true;\n\t".format(p0, p1);
		return r.strip()

	def generate_weapon_condition(self):
		self.weapon_location = choice(list(self.locations.nodes()))
		return "locationWeapon = Place.{};".format(self.weapon_location)

	def get_location_conditions(self):
		chars = get_enum(self.source, self.contract_name, "Char")
		places = get_enum(self.source, self.contract_name, "Place")
		r = []
		for c in chars[1:]:
			r.append((c, choice(places)))

		return r

	def generate_location_conditions(self, conditions, var_name):
		r = ""
		for (c, p) in conditions:
			c = c.replace("$", "")
			p = p.replace("$", "")
			r = r + "{}[Char.{}] = Place.{};\n\t".format(var_name, c, p)

		return r.strip()

	def solve(self, seed, workers):
		(proc, outjson, outerr) = create_echidna_process(self.outdir, self.outdir + "/model.sol", seed, workers)
		proc.wait()
		outjson.close()
		outerr.close()

		with open(outerr.name, 'r') as f:
			err = f.read().strip()
			if len(err) > 0:
				print("error output:", err)

		if proc.returncode != 0:
			print("Solution found! 🔍")

			json = None
			with open(outjson.name, 'r') as f:
				json = "{" + f.read().split("\n{")[1]

			return loads(json)
		else:
			print("No solution found! 💩")
			return None
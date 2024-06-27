from json import loads
from random import choice, shuffle

from mystery_o_matic.solidity import (
    read_sol_template,
    read_solidity,
    save_solidity,
    get_enum,
)
from mystery_o_matic.echidna import create_echidna_process, create_outdir


class Model:
    """
    Represents a model for generating and solving a mystery game.

    Attributes:
        contract_name (str): The name of the contract.
        outdir (str): The output directory.
        source (str): The solidity source code.
        solidity_filename (str): The filename of the solidity file.
        weapon_location_condition (str): The condition for the weapon location.
        connection_conditions (str): The conditions for the location connections.
        initial_locations_conditions (str): The conditions for the initial locations.
    """

    contract_name = ""
    outdir = ""
    source = ""
    solidity_filename = ""
    weapon_location_condition = ""
    connection_conditions = ""
    initial_locations_conditions = ""
    number_characters = 0
    char_enum = ""

    def __init__(self, contract_name, locations, outdir, solidity_file):
        self.contract_name = contract_name
        self.locations = locations
        self.outdir = outdir
        # self.source = read_solidity(solidity_file)
        self.template = read_sol_template(solidity_file)

    def generate_chars_enum(self, number_characters):
        r = []
        for i in range(number_characters):
            r.append("CHAR" + str(i + 1))
        return r

    def generate_places_enum(self, number_locations):
        r = []
        for i in range(number_locations):
            r.append("ROOM" + str(i))
        return r

    def generate_enums(self, number_characters):
        self.number_characters = number_characters
        enum = self.generate_chars_enum(number_characters)
        self.char_enum = "," + ", ".join(enum)

        enum = self.generate_places_enum(len(self.locations.graph.nodes()))
        self.place_enum = "," + ", ".join(enum[1:])

    def generate_conditions(self):
        self.connection_conditions = self.generate_location_connections()
        self.weapon_location_condition = self.generate_weapon_condition()

        initial_locations_pairs = self.get_location_conditions()
        self.initial_locations_conditions = self.generate_location_conditions(
            initial_locations_pairs, "currentLocation"
        )

        return (initial_locations_pairs, self.used_weapon_location)

    def generate_solidity(self):
        solidity_source = self.template.substitute(
            connectionLocations=self.connection_conditions,
            currentLocations=self.initial_locations_conditions,
            locationWeapon=self.weapon_location_condition,
            charEnum=self.char_enum,
            placeEnum=self.place_enum,
        )
        solidity_filename = save_solidity(self.outdir, solidity_source)
        self.source = read_solidity(solidity_filename)
        return solidity_filename

    def generate_location_connections(self):
        r = ""
        for p0, p1 in self.locations.graph.edges:
            r = r + "connection[Place.{}][Place.{}] = true;\n\t".format(p0, p1)
        return r.strip()

    def generate_weapon_condition(self):
        self.used_weapon_location = choice(list(self.locations.graph.nodes()))
        return "locationWeapon = Place.{};".format(self.used_weapon_location)

    def get_location_conditions(self):
        chars = self.generate_chars_enum(self.number_characters)
        places = self.generate_places_enum(len(self.locations.graph.nodes()))
        shuffle(places)
        r = list(zip(chars, places))
        return r

    def generate_location_conditions(self, conditions, var_name):
        r = ""
        for c, p in conditions:
            c = c.replace("$", "")
            p = p.replace("$", "")
            r = r + "{}[Char.{}] = Place.{};\n\t".format(var_name, c, p)

        return r.strip()

    def solve(self, seed, workers):
        (proc, outjson, outerr) = create_echidna_process(
            self.outdir, self.outdir + "/model.sol", seed, workers
        )
        proc.wait()
        outjson.close()
        outerr.close()

        with open(outerr.name, "r") as f:
            err = f.read().strip()
            if len(err) > 0:
                print("error output:", err)

        if proc.returncode != 0:
            print("Solution found! 🔍")

            json = None
            with open(outjson.name, "r") as f:
                json = "{" + f.read().split("\n{")[1]

            return loads(json)
        else:
            print("No solution found! 💩")
            return None

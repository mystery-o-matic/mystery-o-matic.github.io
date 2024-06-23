from random import shuffle, choice

from networkx import gnr_graph, relabel_nodes, Graph
from networkx.drawing.nx_agraph import to_agraph

locations = ["egypt", "castle", "train", "ship", "space station"]

mansion_names = {
    "KITCHEN": "kitchen",
    "DINING": "dining room",
    "BEDROOM": "bedroom",
    "BATHROOM": "bathroom",
    "GARDEN": "garden",
}

mansion_representations = {
    "KITCHEN": "🍲",
    "DINING": "🪑",
    "BEDROOM": "🛏️",
    "BATHROOM": "🚽",
    "GARDEN": "🌳",
}

mansion_activities = {
    "KITCHEN": ["noticed someone cooking", "heard someone washing the dishes"],
    "BATHROOM": [
        "heard someone brushing their teeth",
        "heard someone flushing the toilet",
    ],
    "GARDEN": [
        "heard someone whistling in the garden (🌳)",
        "looked outside and saw someone pruning the bushes",
    ],
    "DINING": ["heard someone playing the piano in the dining room (🪑)"],
}

ship_names = {
    "GALLEY": "galley",
    "NAVIGATION ROOM": "navigation room",
    "CAPTAIN CABIN": "captain cabin",
    "MAIN DECK": "main deck",
    "CARGO HOLD": "cargo hold",
}

ship_representations = {
    "GALLEY": "🍲",
    "NAVIGATION ROOM": "🧭",
    "CAPTAIN CABIN": "🛏️",
    "MAIN DECK": "⚓",
    "CARGO HOLD": "📦",
}

ship_activities = {
    "GALLEY": ["noticed someone cooking", "heard someone washing the dishes"],
    "NAVIGATION ROOM": ["saw someone looking at a map"],
    "MAIN DECK": [
        "heard someone loading a cannon",
        "heard someone adjusting the sails",
    ],
    "CARGO HOLD": ["heard someone rummaging in the cargo hold (📦)"],
}

egypt_names = {
    "THRONE ROOM": "throne room",
    "BURIAL PLACE": "burial chamber",
    "TEMPLE": "temple",
    "DESERT": "desert",
    "GARDEN": "garden",
}

egypt_representations = {
    "THRONE ROOM": "👑",
    "BURIAL PLACE": "⚰️",
    "TEMPLE": "📿",
    "DESERT": "🏜️",
    "GARDEN": "🌳",
}

egypt_activities = {
    "THRONE ROOM": [
        "saw someone from a distance sitting on the throne",
        "saw someone from afar polishing the throne",
    ],
    "BURIAL PLACE": ["saw someone at a distane praying in the burial chamber (⚰️)"],
    "TEMPLE": [
        "saw someone at a distance praying in the temple (📿)",
        "saw someone from afar lighting candles in the temple (📿)",
    ],
    "DESERT": ["looked outside and saw someone riding a camel in the desert (🏜️)"],
    "GARDEN": [
        "heard someone whistling in the garden (🌳)",
        "looked outside and saw someone pruning the bushes",
    ],
}

medieval_castle_names = {
    "GREAT HALL": "great hall",
    "BED CHAMBER": "bed chamber",
    "DUNGEON": "dungeon",
    "ARMORY": "armory",
    "GARDEN": "garden",
}

medieval_castle_representations = {
    "GREAT HALL": "🍷",
    "BED CHAMBER": "🛏️",
    "DUNGEON": "🔒",
    "ARMORY": "🛡️",
    "GARDEN": "🌳",
}

medieval_castle_activities = {
    "GREAT HALL": [
        "heard someone playing the harp in the great hall (🍷)",
        "saw someone from a distance dancing in the great hall (🍷)",
    ],
    "ARMORY": [
        "saw someone from afar sharpening a sword in the armory (🛡️)",
        "saw someone at a distance polishing a shield in the armory (🛡️)",
    ],
    "GARDEN": [
        "heard someone whistling in the garden (🌳)",
        "looked outside and saw someone pruning the bushes",
    ],
}

train_names = {
    "LOCOMOTIVE": "locomotive",
    "LUGGAGE": "luggage carriage",
    "DINING": "dining carriage",
    "SLEEPING": "sleeping carriage",
    "LOUNGE": "lounge carriage",
}

train_representations = {
    "LOCOMOTIVE": "🚂",
    "LUGGAGE": "🧳",
    "DINING": "🍽️",
    "SLEEPING": "🛌",
    "LOUNGE": "🪑",
}

train_activities = {
    "LOCOMOTIVE": [
        "glanced out my window and saw someone fueling the locomotive (🚂)",
        "heard the whistle of the locomotive",
    ],
    "LUGGAGE": ["heard someone rummaging in the luggage carriage (🧳)"],
    "DINING": [
        "glanced out my window and saw someone eating in the dining carriage (🍽️)",
        "heard someone playing the piano in the dining carriage (🍽️)",
    ],
    "LOUNGE": ["glanced out my window and saw someone reading in the lounge carriage (🪑)"],
}

space_station_names = {
    "COMMAND": "command module",
    "LAB": "lab module",
    "AIRLOCK": "airlock module",
    "SLEEPING": "sleeping module",
    "GARDEN": "garden module",
}

space_station_representations = {
    "COMMAND": "🕹️",
    "LAB": "🔬",
    "AIRLOCK": "🔒",
    "SLEEPING": "🛌",
    "GARDEN": "🥔",
}

space_station_activities = {}


def get_location_data(selected_location):
    if selected_location is None:
        location_name = choice(locations)
    else:
        location_name = selected_location
    location_data = None

    if location_name == "mansion":
        location_data = (
            " are back into <b>the mansion where everything started</b>!",
            mansion_names,
            mansion_representations,
            mansion_activities,
        )
    elif location_name == "ship":
        location_data = (
            " are transported back in time to a <b>a pirate ship sailing in the Caribbean</b>!",
            ship_names,
            ship_representations,
            ship_activities,
        )
    elif location_name == "egypt":
        location_data = (
            " are transported back in time to a <b>pyramid in the Ancient Egypt</b>!",
            egypt_names,
            egypt_representations,
            egypt_activities,
        )
    elif location_name == "castle":
        location_data = (
            " are transported back in time to a <b>castle in the Middle Ages</b>!",
            medieval_castle_names,
            medieval_castle_representations,
            medieval_castle_activities,
        )
    elif location_name == "train":
        location_data = (
            " are transported back in time into <b>the famous Orient Express</b> during its last voyage!",
            train_names,
            train_representations,
            train_activities,
        )
    elif location_name == "space station":
        location_data = (
            " are transported into the future to <b>a high-tech space station</b> orbiting an unknown planet!",
            space_station_names,
            space_station_representations,
            space_station_activities,
        )
    else:
        assert False, "Unknown location name: " + location_name

    return (location_name, location_data)


class Locations:
    """
    A class representing locations in a mystery game.

    Attributes:
    - graph: The graph representing the connections between locations.
    - map: A dictionary mapping generic node names to concrete location names.
    - indices: A dictionary mapping generic node names to concrete location indices.
    - names: A dictionary mapping generic node names to concrete location names.
    - representations: A dictionary mapping generic node names to concrete location representations.
    - weapons: A list of weapons available in the game.
    - weapon_locations: A dictionary mapping location names to weapons.
    """

    def __init__(self, location_name, number_places, location_data, weapons):
        """
        Initializes a Locations object.

        Parameters:
        - number_places: The number of locations in the game.
        - location_data: A tuple containing:
            + intro: A short sentence to introduce the location.
            + names: A dictionary mapping concrete location names to generic node names.
            + representations: A dictionary mapping concrete location names to their representations.
        - weapons: A list of weapons available in the game.
        """

        self.name = location_name
        intro, names, representations, activities = location_data
        self.intro = intro
        self.activities = activities
        self.number_places = number_places
        nodes = {}
        for n in range(number_places):
            nodes[n] = "ROOM" + str(n)

        self.map = nodes
        self.number_places = len(nodes)

        nodes_list = list(nodes.values())
        shuffle(nodes_list)
        names_list = list(names.keys())

        self.indices = {}
        self.names = {}
        self.representations = {}

        if location_name == "train":
            self.indices["ROOM0"] = "LOCOMOTIVE"
            self.names["ROOM0"] = names["LOCOMOTIVE"]
            self.representations["ROOM0"] = representations["LOCOMOTIVE"]

            names_list = [x for x in names_list if x != "LOCOMOTIVE"]
            nodes_list = [x for x in nodes_list if x != "ROOM0"]

        for generic, concrete in zip(nodes_list, names_list):
            self.indices[generic] = concrete
            self.names[generic] = names[concrete]
            self.representations[generic] = representations[concrete]

        self.weapons = weapons
        self.graph = self.create_locations_graph(nodes)
        self.weapon_locations = self.create_locations_weapons(weapons)

    def create_locations_graph(self, nodes):
        """
        Creates a graph representing the connections between locations.

        Parameters:
        - nodes: A dictionary mapping node indices to location names.

        Returns:
        - graph: The created graph.
        """
        if self.name == "train":
            graph = Graph()
            for n in range(self.number_places - 1):
                graph.add_edge("ROOM" + str(n), "ROOM" + str(n + 1))
        else:
            graph = gnr_graph(self.number_places, 0.5).to_undirected()
        graph = relabel_nodes(graph, nodes)
        return graph

    def create_locations_weapons(self, weapons):
        """
        Creates a dictionary mapping location names to weapons.

        Parameters:
        - weapons: A list of weapons available in the game.

        Returns:
        - weapon_locations: The created dictionary.
        """
        weapon_locations = {}
        shuffled_weapons = list(weapons)
        shuffle(shuffled_weapons)

        for loc, weapon in zip(self.map.values(), shuffled_weapons):
            weapon_locations[loc] = weapon

        return weapon_locations

    def render_locations(self, outdir):
        """
        Renders the locations graph and saves it as images.

        Parameters:
        - outdir: The directory where the images will be saved.
        """
        labels = {}
        for place, name in self.names.items():
            labels[place] = name + " " + self.representations[place]

        relabeled_graph = relabel_nodes(self.graph, labels)
        g = to_agraph(relabeled_graph)
        g.graph_attr.update(bgcolor="transparent")
        g.node_attr.update(
            fontname="Raleway", color="lightblue2", style="filled", shape="Mrecord"
        )
        g.edge_attr.update(color="gray")
        g.draw(outdir + "/images/locations_big.svg", prog="dot")
        g.graph_attr.update(dpi="200")
        g.draw(outdir + "/images/locations_big.png", prog="dot")

        labels = {}
        for place, name in self.names.items():
            labels[place] = self.representations[place]

        relabeled_graph = relabel_nodes(self.graph, labels)
        g = to_agraph(relabeled_graph)
        g.graph_attr.update(
            bgcolor="transparent", nodesep="0.1", ranksep="0.1", margin="0"
        )
        g.edge_attr.update(color="gray", labeldistance="0.1")

        g.node_attr.update(
            fontname="Raleway", shape="plaintext", width="0.2", fixedsize="true"
        )
        g.draw(outdir + "/images/locations_small.svg", prog="dot")
        g.graph_attr.update(dpi="200")
        g.draw(outdir + "/images/locations_small.png", prog="dot")

    def get_activities(self):
        """
        Returns the activities associated with each location.

        Returns:
        - activities: A dictionary mapping location names to activities.
        """
        activities = {}
        for generic, concrete in self.indices.items():
            if concrete in self.activities:
                activities[generic] = self.activities[concrete]

        return activities

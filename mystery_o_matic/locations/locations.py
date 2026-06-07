from random import shuffle, choice

from networkx import (
    gnp_random_graph,
    relabel_nodes,
    Graph,
    is_planar,
    is_connected,
    planar_layout,
)
from networkx.drawing.nx_agraph import to_agraph

from mystery_o_matic.locations import (
    mansion,
    ship,
    egypt,
    island,
    castle,
    museum,
    train,
    space_station,
    zoo,
    hospital,
    sport_club,
    school,
    arctic_base,
)

LOCATION_REGISTRY = {
    "mansion": mansion.get_data,
    "ship": ship.get_data,
    "egypt": egypt.get_data,
    "island": island.get_data,
    "castle": castle.get_data,
    "museum": museum.get_data,
    "train": train.get_data,
    "space station": space_station.get_data,
    "zoo": zoo.get_data,
    "hospital": hospital.get_data,
    "sport club": sport_club.get_data,
    "abandoned school": school.get_data,
    "arctic base": arctic_base.get_data,
}

locations = list(LOCATION_REGISTRY.keys())


def get_location_data(selected_location, mode):
    if selected_location is None:
        locs = list(locations)
        if mode == "latex":
            locs.remove("train")
        location_name = choice(locs)
    else:
        location_name = selected_location

    if location_name not in LOCATION_REGISTRY:
        raise ValueError("Unknown location name: " + location_name)

    location_data = LOCATION_REGISTRY[location_name]()
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

    def __init__(self, mode, location_name, number_places, location_data, weapons):
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
        self.mode = mode
        self.name = location_name
        # Some location modules return (intro, names, representations, activities);
        # newer ones include a fifth element with stay-activities for StayedClue flavor.
        if len(location_data) == 5:
            intro, names, representations, activities, stay_activities = location_data
        else:
            intro, names, representations, activities = location_data
            stay_activities = {}
        self.intro = intro
        self.activities = activities
        self.stay_activities = stay_activities
        self.number_places = number_places
        nodes = {}
        for n in range(number_places):
            nodes[n] = "ROOM" + str(n)

        self.map = nodes
        self.number_places = len(nodes)

        nodes_list = list(nodes.values())
        shuffle(nodes_list)
        names_list = list(names["en"].keys())

        self.names = names
        self.indices = {}
        self.representations = {}

        if location_name == "train":
            self.indices["ROOM0"] = "LOCOMOTIVE"
            self.representations["ROOM0"] = representations["LOCOMOTIVE"]

            names_list = [x for x in names_list if x != "LOCOMOTIVE"]
            nodes_list = [x for x in nodes_list if x != "ROOM0"]

        for generic, concrete in zip(nodes_list, names_list):
            self.indices[generic] = concrete
            self.representations[generic] = representations[concrete]

        self.rindices = {v: k for k, v in self.indices.items()}
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
        keepGenerating = True

        while keepGenerating:
            if self.name == "train":
                graph = Graph()
                for n in range(self.number_places - 1):
                    graph.add_edge("ROOM" + str(n), "ROOM" + str(n + 1))
            else:
                graph = gnp_random_graph(self.number_places, 0.5)

            keepGenerating = not (is_planar(graph) and is_connected(graph))

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
        for language in ["en", "es", "ru"]:
            if language in self.names:
                self.render_locations_language(language, outdir)

    def render_locations_language(self, language, outdir):
        """
        Renders the locations graph and saves it as images.

        Parameters:
        - outdir: The directory where the images will be saved.
        """
        names = {}
        for index, place in self.indices.items():
            names[index] = self.names[language][place]

        labels = {}
        for place, name in names.items():
            labels[place] = name + " " + self.representations[place]

        relabeled_graph = relabel_nodes(self.graph, labels)
        g = to_agraph(relabeled_graph)

        if g.number_of_nodes() > 3:
            pos = planar_layout(g)

            # Apply the planar layout to the PyGraphviz graph
            for node, (x, y) in pos.items():
                n = g.get_node(node)
                n.attr["pos"] = f"{x},{y}"

        g.graph_attr.update(bgcolor="transparent")
        g.node_attr.update(
            fontname="Raleway", color="lightblue2", style="filled", shape="Mrecord"
        )
        g.layout(prog="dot")
        g.edge_attr.update(color="gray")
        g.draw(outdir + f"/{language}/locations_big.svg")

        if self.mode == "latex":
            g.draw(outdir + f"/{language}/locations_big.pdf")

        g.graph_attr.update(dpi="200")
        if self.mode != "latex":
            g.draw(outdir + f"/{language}/locations_big.png")

        labels = {}
        for place, name in names.items():
            labels[place] = self.representations[place]

        relabeled_graph = relabel_nodes(self.graph, labels)
        g = to_agraph(relabeled_graph)

        if g.number_of_nodes() > 3:
            pos = planar_layout(g)

            # Apply the planar layout to the PyGraphviz graph
            for node, (x, y) in pos.items():
                n = g.get_node(node)
                n.attr["pos"] = f"{x},{y}"

        g.graph_attr.update(
            bgcolor="transparent", nodesep="0.1", ranksep="0.1", margin="0"
        )
        g.edge_attr.update(color="dimgrey", labeldistance="0.05")

        g.node_attr.update(
            fontname="Raleway", shape="plaintext", width="0.2", fixedsize="true"
        )

        if (self.mode == "latex"):
            if g.number_of_nodes() == 3:
                g.node_attr.update(fontsize="12")
            elif g.number_of_nodes() == 4:
                g.node_attr.update(fontsize="14")
            elif g.number_of_nodes() >= 5:
                g.node_attr.update(fontsize="16")

        g.layout(prog="dot")
        g.draw(outdir + f"/{language}/locations_small.svg")

        if self.mode == "latex":
            g.draw(outdir + f"/{language}/locations_small.pdf")

        g.graph_attr.update(dpi="200")

        if self.mode != "latex":
            g.draw(outdir + f"/{language}/locations_small.png")

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

    def get_stay_activities(self):
        """
        Returns the stay-activities (first-person verb phrases for StayedClue
        flavor text), re-keyed from concrete room names (e.g. KITCHEN) to the
        generic placeholders (ROOM0, ROOM1, ...) used in clue templates.
        """
        out = {}
        for generic, concrete in self.indices.items():
            if concrete in self.stay_activities:
                out[generic] = self.stay_activities[concrete]
        return out

    def sort_locations(self):
        """
        Returns a list of generic labels sorted according to where they show in the graph.
        Sorting is by highest x (descending), then lowest y (ascending).
        """
        g = to_agraph(self.graph)
        g.layout(prog="dot")
        pos = {}
        for node in self.graph.nodes():
            gv_node = g.get_node(node)
            pos_str = gv_node.attr.get("pos")
            if pos_str:
                x, y = map(float, pos_str.split(","))
                pos[node] = (x, y)
        if not pos:
            return list(self.graph.nodes())
        sorted_locations = sorted(pos.items(), key=lambda item: (-item[1][1], item[1][0]))
        sorted_labels = [loc[0].lower() for loc in sorted_locations]
        return sorted_labels

class TutorialLocations(Locations):
    def __init__(self, location_data):
        self.name = "tutorial"
        # Tolerate both legacy 4-tuple and new 5-tuple (with stay_activities).
        names = location_data[1]
        representations = location_data[2]
        self.number_places = 4
        nodes = {}
        for n in range(self.number_places):
            nodes[n] = "ROOM" + str(n)

        self.map = nodes
        self.number_places = len(nodes)

        nodes_list = list(nodes.values())
        shuffle(nodes_list)

        self.names = names
        self.indices = {}
        self.representations = {}

        self.indices["ROOM0"] = "KITCHEN"
        self.representations["ROOM0"] = representations["KITCHEN"]

        self.indices["ROOM1"] = "DINING"
        self.representations["ROOM1"] = representations["DINING"]

        self.indices["ROOM2"] = "BEDROOM"
        self.representations["ROOM2"] = representations["BEDROOM"]

        self.indices["ROOM3"] = "BATHROOM"
        self.representations["ROOM3"] = representations["BATHROOM"]

        self.rindices = {v: k for k, v in self.indices.items()}
        self.graph = self.create_locations_graph(nodes)

    def create_locations_graph(self, nodes):
        """
        Creates a graph representing the connections between locations.

        Parameters:
        - nodes: A dictionary mapping node indices to location names.

        Returns:
        - graph: The created graph.
        """
        graph = Graph()
        graph.add_edge("ROOM0", "ROOM1")
        graph.add_edge("ROOM0", "ROOM2")
        graph.add_edge("ROOM2", "ROOM3")
        graph = relabel_nodes(graph, nodes)
        return graph

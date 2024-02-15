from random import shuffle

from networkx import gnr_graph, relabel_nodes
from networkx.drawing.nx_agraph import to_agraph

mansion_names = {
    "KITCHEN": "kitchen",
    "DINING": "dining room",
    "BEDROOM": "bedroom",
    "BATHROOM": "bathroom",
}

mansion_representations = {
    "KITCHEN": "🍲",
    "DINING": "🪑",
    "BEDROOM": "🛏️",
    "BATHROOM": "🚽",
}

class Locations:
    graph = None

    def __init__(self, names, representations, weapons):
        nodes = {0: "ROOM0", 1: "ROOM1", 2: "ROOM2", 3: "ROOM3"}
        self.map = nodes

        nodes_list = list(nodes.values())
        shuffle(nodes_list)
        names_list = list(names.keys())

        self.indices = {}
        self.names = {}
        self.representations = {}

        for generic, concrete in zip(nodes_list, names_list):
            self.indices[generic] = concrete
            self.names[generic] = names[concrete]
            self.representations[generic] = representations[concrete]

        self.weapons = weapons
        self.graph = self.create_locations_graph(nodes)
        self.weapon_locations = self.create_locations_weapons(weapons)

    def create_locations_graph(self, nodes):
        graph = gnr_graph(4, 0.5).to_undirected()
        graph = relabel_nodes(graph, nodes)
        return graph

    def create_locations_weapons(self, weapons):
        weapon_locations = {}
        shuffled_weapons = list(weapons)
        shuffle(shuffled_weapons)

        for loc, weapon in zip(self.map.values(), shuffled_weapons):
            weapon_locations[loc] = weapon

        return weapon_locations

    def render_locations(self, outdir):
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
        g.graph_attr.update(bgcolor="transparent", nodesep="0.1", ranksep="0.1")
        g.edge_attr.update(color="gray", labeldistance="0.1")

        g.node_attr.update(
            fontname="Raleway", shape="plaintext", width="0.2", fixedsize="true"
        )
        g.draw(outdir + "/images/locations_small.svg", prog="dot")
        g.graph_attr.update(dpi="200")
        g.draw(outdir + "/images/locations_small.png", prog="dot")

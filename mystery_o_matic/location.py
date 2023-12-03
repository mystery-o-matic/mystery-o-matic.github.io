from random import shuffle

from networkx import gnr_graph, relabel_nodes
from networkx.drawing.nx_agraph import to_agraph

mansion_locations = {0: "KITCHEN", 1: "DINING", 2: "BEDROOM", 3: "BATHROOM"}
weapons = {"pistol", "knife", "poison", "rope"}
mansion_names = {
    "KITCHEN": "kitchen",
    "DINING": "dining room",
    "BEDROOM": "bedroom",
    "BATHROOM": "bathroom",
}

mansion_representations = {
    "KITCHEN": "🍲",
    "DINING": "🍽️",
    "BEDROOM": "🛏️",
    "BATHROOM": "🚽",
}

def create_locations_graph(outdir, nodes):
    graph = gnr_graph(4, 0.5).to_undirected()
    graph = relabel_nodes(graph, nodes)
    return graph


def create_locations_weapons():
    weapon_locations = {}
    shuffled_weapons = list(weapons)
    shuffle(shuffled_weapons)

    for loc, weapon in zip(mansion_locations.values(), shuffled_weapons):
        weapon_locations[loc] = weapon

    return weapon_locations


def render_locations(outdir, graph):
    labels = {}
    for place, name in mansion_names.items():
        labels[place] = name + " " + mansion_representations[place]

    relabeled_graph = relabel_nodes(graph, labels)
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
    for place, name in mansion_names.items():
        labels[place] = mansion_representations[place]

    relabeled_graph = relabel_nodes(graph, labels)
    g = to_agraph(relabeled_graph)
    g.graph_attr.update(bgcolor="transparent", nodesep="0.1", ranksep="0.1")
    g.edge_attr.update(color="gray", labeldistance="0.1")

    g.node_attr.update(
        fontname="Raleway", shape="plaintext", width="0.2", fixedsize="true"
    )
    g.draw(outdir + "/images/locations_small.svg", prog="dot")
    g.graph_attr.update(dpi="200")
    g.draw(outdir + "/images/locations_small.png", prog="dot")
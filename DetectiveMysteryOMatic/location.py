from networkx import gnr_graph, relabel_nodes
from networkx.drawing.nx_agraph import to_agraph


mansion_locations = {0: "KITCHEN", 1: "LIVING", 2: "BEDROOM", 3: "BATHROOM"}
weapon_locations = {"KITCHEN": "gun", "LIVING": "knife", "BEDROOM": "poison", "BATHROOM": "rope"}
mansion_representations = {"KITCHEN": "kitchen 🍲", "LIVING": "living room 🛋️", "BEDROOM": "bedroom 🛏️", "BATHROOM": "bathroom 🚽"}

def create_locations_graph(outdir, nodes):
	graph = gnr_graph(4, 0.5).to_undirected()
	graph = relabel_nodes(graph, nodes)
	return graph

def render_locations(outdir, graph):
	graph = relabel_nodes(graph, mansion_representations)
	g = to_agraph(graph)
	g.node_attr.update(color = "lightblue2", style = "filled", shape = "Mrecord")
	g.draw(outdir + "/images/locations.svg", prog='dot')
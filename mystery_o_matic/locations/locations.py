from random import choice, shuffle

from networkx import (
    Graph,
    gnp_random_graph,
    is_connected,
    is_planar,
    relabel_nodes,
)

from mystery_o_matic.locations import (
    arctic_base,
    castle,
    egypt,
    hospital,
    island,
    mansion,
    museum,
    school,
    ship,
    space_station,
    sport_club,
    train,
    zoo,
)
from mystery_o_matic.roommap import (
    BIG_FILL,
    BIG_LINK,
    BIG_LINK_W,
    BIG_RADIUS,
    RADIUS,
    STROKE,
)
from mystery_o_matic.roommap import positions as roommap_positions
from mystery_o_matic.roommap import render as roommap_svg
from mystery_o_matic.roommap import render_png as roommap_png

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

    def render_locations(self, outdir, languages=None):
        if languages is None:
            languages = ["en", "es", "ru"]
        for language in languages:
            if language in self.names:
                self.render_locations_language(language, outdir)

    def _graph_as_indices(self):
        """Return node order and edges expressed as node-index pairs."""
        nodes = list(self.graph.nodes())
        indices = {node: index for index, node in enumerate(nodes)}
        edges = [(indices[start], indices[end]) for start, end in self.graph.edges()]
        return nodes, edges

    def render_locations_language(self, language, outdir):
        """
        Draw the locations graph and save it as images.

        The old maps could be tall and narrow, and their corridors could appear
        to cross unrelated rooms. These maps place rooms on an ellipse, expand
        it when the rendered labels need more clearance, draw corridors behind
        the room tiles, and choose the cyclic room order with the fewest
        corridor crossings.
        """
        names = {
            node: self.names[language][place] for node, place in self.indices.items()
        }
        nodes, edges = self._graph_as_indices()
        glyphs = [self.representations[node] for node in nodes]
        room_names = [names[node] for node in nodes]
        vertical = self.name == "train"

        for (
            stem,
            captions,
            inline,
            fill,
            rx,
            ry,
            tile,
            font_size,
            label_width,
            radius,
            stroke,
            link,
            link_width,
        ) in (
            (
                "locations_big",
                room_names,
                True,
                BIG_FILL,
                150.0,
                110.0,
                52.0,
                20.0,
                180.0,
                BIG_RADIUS,
                BIG_FILL,
                BIG_LINK,
                BIG_LINK_W,
            ),
            (
                "locations_small",
                None,
                False,
                "#ffffff",
                34.0,
                85.0,
                34.0,
                20.0,
                None,
                RADIUS,
                STROKE,
                BIG_LINK,
                BIG_LINK_W,
            ),
        ):
            render_ry = (100.0 if stem == "locations_big" else 52.0) if vertical else ry
            svg = roommap_svg(
                glyphs,
                edges,
                rx=rx,
                ry=render_ry,
                tile=tile,
                font_size=font_size,
                captions=captions,
                inline=inline,
                fill=fill,
                vertical=vertical,
                draw_tiles=True,
                radius=radius,
                stroke=stroke,
                link=link,
                link_width=link_width,
                max_inline_width=label_width,
            )
            with open(
                f"{outdir}/{language}/{stem}.svg", "w", encoding="utf8"
            ) as image_file:
                image_file.write(svg)

            roommap_png(
                glyphs,
                edges,
                f"{outdir}/{language}/{stem}.png",
                rx=rx,
                ry=render_ry,
                tile=tile,
                font_size=font_size,
                captions=captions,
                inline=inline,
                fill=fill,
                vertical=vertical,
                draw_tiles=True,
                radius=radius,
                stroke=stroke,
                link=link,
                link_width=link_width,
                max_inline_width=label_width,
            )

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
        Return generic labels in their visual map order, top to bottom and
        left to right.

        The active room-map layout already knows every position, so sorting
        no longer needs a separate Graphviz layout.
        """
        nodes, edges = self._graph_as_indices()
        points = roommap_positions(nodes, edges, vertical=self.name == "train")
        positions = {node: points[index] for index, node in enumerate(nodes)}

        if not positions:
            return list(self.graph.nodes())
        sorted_locations = sorted(
            positions.items(),
            # Symmetric ellipse points can differ by tiny floating-point
            # amounts. Bucket y before sorting so a visual row is genuinely
            # ordered from left to right.
            key=lambda item: (round(item[1][1], 8), item[1][0]),
        )
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

"""Regenerate every static tutorial room map with the production renderer."""

import sys
from argparse import ArgumentParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mystery_o_matic.locations import TutorialLocations, mansion
from mystery_o_matic.roommap import (
    BIG_FILL,
    BIG_LINK,
    BIG_LINK_W,
    BIG_RADIUS,
    RADIUS,
    STROKE,
    render,
)

LANGUAGES = ("en", "es", "ru")


def _large_map(labels, edges, captions, edge_styles=None):
    return render(
        labels,
        edges,
        rx=150.0,
        ry=110.0,
        tile=52.0,
        font_size=20.0,
        captions=captions,
        inline=True,
        fill=BIG_FILL,
        radius=BIG_RADIUS,
        stroke=BIG_FILL,
        link=BIG_LINK,
        link_width=BIG_LINK_W,
        max_inline_width=180.0,
        edge_styles=edge_styles,
    )


def render_tutorial_maps(output_dir):
    """Write the tutorial's base, small, and highlighted maps."""
    tutorial = TutorialLocations(mansion.get_data())
    nodes, edges = tutorial._graph_as_indices()
    labels = [tutorial.representations[node] for node in nodes]
    room = {tutorial.indices[node]: index for index, node in enumerate(nodes)}

    route_styles = {
        (room["KITCHEN"], room["DINING"]): {
            "stroke": "#49b776",
            "stroke_width": 3.0,
        },
        (room["KITCHEN"], room["BEDROOM"]): {
            "stroke": "#49b776",
            "stroke_width": 3.0,
        },
        (room["BEDROOM"], room["BATHROOM"]): {
            "stroke": "#ff0101",
            "stroke_width": 3.0,
        },
    }
    highlights = {
        "bedroom": room["BEDROOM"],
        "dining_room": room["DINING"],
        "bathroom": room["BATHROOM"],
    }

    output_dir = Path(output_dir)
    for language in LANGUAGES:
        destination = output_dir / language
        destination.mkdir(parents=True, exist_ok=True)
        captions = [tutorial.names[language][tutorial.indices[node]] for node in nodes]

        maps = {
            "locations_tutorial.svg": _large_map(labels, edges, captions),
            "locations_tutorial_highlighted.svg": _large_map(
                labels, edges, captions, route_styles
            ),
            "locations_tutorial_small.svg": render(
                labels,
                edges,
                rx=34.0,
                ry=85.0,
                tile=34.0,
                font_size=20.0,
                fill="#ffffff",
                radius=RADIUS,
                stroke=STROKE,
                link=BIG_LINK,
                link_width=BIG_LINK_W,
            ),
        }
        for name, target in highlights.items():
            edge_styles = {
                edge: {"stroke_dasharray": "4 4"}
                for edge in edges
                if target not in edge
            }
            maps[f"locations_tutorial_highlighted_{name}.svg"] = _large_map(
                labels, edges, captions, edge_styles
            )

        for filename, svg in maps.items():
            (destination / filename).write_text(svg, encoding="utf8")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "static",
        help="asset root containing language directories (default: static)",
    )
    render_tutorial_maps(parser.parse_args().output)


if __name__ == "__main__":
    main()

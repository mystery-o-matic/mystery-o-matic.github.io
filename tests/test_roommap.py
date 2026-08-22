from itertools import combinations
from xml.etree import ElementTree

from networkx import Graph
from PIL import Image

from mystery_o_matic.locations.locations import Locations
from mystery_o_matic.roommap import (
    ROOM_GAP,
    _crossings,
    _fit_layout,
    _layout_is_clear,
    _wrap_inline_text,
    best_order,
    layout,
    positions,
    render,
    render_png,
)


def test_best_order_removes_avoidable_corridor_crossing():
    edges = [(0, 2), (1, 3)]

    order = best_order(4, edges)

    assert sorted(order) == [0, 1, 2, 3]
    assert _crossings(order, edges) == 0


def test_svg_is_landscape_and_escapes_room_text():
    svg = render(
        ["🍷", "🛏️", "🔒", "🛡️"],
        [(0, 1), (0, 2), (1, 3)],
        captions=["hall <&> lounge", "bed chamber", "dungeon", "armory"],
        inline=True,
        fill="#b2dfee",
        rx=190,
        ry=104,
        tile=40,
        font_size=19,
    )

    root = ElementTree.fromstring(svg)
    width = float(root.attrib["width"])
    height = float(root.attrib["height"])

    assert width > height
    assert "hall &lt;&amp;&gt; lounge" in svg


def test_png_uses_requested_raster_scale(tmp_path):
    image_path = tmp_path / "map.png"

    render_png(
        ["A", "B", "C", "D"],
        [(0, 1), (0, 2), (1, 3)],
        image_path,
        scale=2,
    )

    with Image.open(image_path) as image:
        assert image.size == (404, 300)


def test_vertical_path_layout_preserves_room_order():
    points = positions(
        range(5),
        [(0, 1), (1, 2), (2, 3), (3, 4)],
        ry=52,
        vertical=True,
    )

    assert [points[index][0] for index in range(5)] == [0, 0, 0, 0, 0]
    assert [points[index][1] for index in range(5)] == [-104, -52, 0, 52, 104]


def test_glyph_only_map_clips_corridor_without_drawing_tiles():
    svg = render(
        ["A", "B"],
        [(0, 1)],
        vertical=True,
        draw_tiles=False,
    )

    assert "<rect" not in svg
    assert 'd="M0.0,-9.0 L0.0,9.0"' in svg


def test_safe_four_room_layout_keeps_its_preferred_dimensions():
    edges = [(0, 2), (0, 3), (1, 3), (2, 3)]
    widths = [170.4, 194.8, 193.8, 198.5]

    preferred = layout(4, edges, rx=150, ry=110)
    fitted = _fit_layout(4, edges, widths, 52, rx=150, ry=110)

    assert fitted == preferred


def test_five_room_layout_expands_to_separate_long_labels():
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    widths = [120, 120, 200, 200, 120]
    preferred = layout(5, edges, rx=150, ry=110)

    assert not _layout_is_clear(preferred, edges, widths, 62)

    fitted = _fit_layout(5, edges, widths, 62, rx=150, ry=110)

    assert _layout_is_clear(fitted, edges, widths, 62)
    assert abs(fitted[2][0]) > abs(preferred[2][0])


def test_five_room_layout_moves_corridors_away_from_unrelated_rooms():
    edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
    widths = [120, 196, 120, 120, 120]
    height = 62
    preferred = layout(5, edges, rx=150, ry=110)

    # Its boxes are already separate; only the 0--2 corridor is too close to room 1.
    assert all(
        abs(preferred[first][0] - preferred[second][0])
        >= (widths[first] + widths[second]) / 2 + ROOM_GAP
        or abs(preferred[first][1] - preferred[second][1]) >= height + ROOM_GAP
        for first, second in combinations(range(5), 2)
    )
    assert not _layout_is_clear(preferred, edges, widths, height)

    fitted = _fit_layout(5, edges, widths, height, rx=150, ry=110)

    assert _layout_is_clear(fitted, edges, widths, height)


def test_vertical_layout_expands_its_step_for_tall_labels():
    edges = [(0, 1), (1, 2), (2, 3), (3, 4)]

    fitted = _fit_layout(
        5,
        edges,
        [190] * 5,
        118,
        rx=0,
        ry=100,
        vertical=True,
    )

    assert fitted[1][1] - fitted[0][1] == 118 + ROOM_GAP


def test_wrapping_uses_measured_raleway_width():
    assert _wrap_inline_text("command module", "🕹️", 20, 180) == [
        "command module",
        "🕹️",
    ]


def test_location_maps_draw_a_box_around_each_glyph(tmp_path):
    locations = object.__new__(Locations)
    locations.name = "castle"
    locations.graph = Graph(
        [
            ("ROOM0", "ROOM1"),
            ("ROOM0", "ROOM2"),
            ("ROOM1", "ROOM3"),
            ("ROOM2", "ROOM3"),
        ]
    )
    locations.representations = {
        "ROOM0": "🛡️",
        "ROOM1": "🛏️",
        "ROOM2": "🍷",
        "ROOM3": "🔒",
    }
    locations.indices = {
        "ROOM0": "ARMORY",
        "ROOM1": "BED_CHAMBER",
        "ROOM2": "GREAT_HALL",
        "ROOM3": "DUNGEON",
    }
    locations.names = {
        "en": {
            "ARMORY": "armory",
            "BED_CHAMBER": "bed chamber",
            "GREAT_HALL": "great hall",
            "DUNGEON": "dungeon",
        }
    }
    (tmp_path / "en").mkdir()

    locations.render_locations_language("en", tmp_path)

    svg = (tmp_path / "en" / "locations_small.svg").read_text(encoding="utf8")
    big_svg = (tmp_path / "en" / "locations_big.svg").read_text(encoding="utf8")
    assert svg.count("<rect") == 4
    assert 'rx="7.0"' in svg
    assert 'stroke="#1a1a1a"' in svg
    assert 'stroke="#808080" stroke-width="1.4"' in svg
    assert big_svg.count("<rect") == 4
    assert 'fill="#b2dfee"' in big_svg
    assert 'rx="16.0"' in big_svg
    assert 'stroke="#b2dfee"' in big_svg
    assert 'stroke="#808080" stroke-width="1.4"' in big_svg
    assert 'font-family="Raleway,' in big_svg
    assert "armory" in big_svg
    assert "bed chamber 🛏️" in big_svg
    assert "<tspan" in big_svg
    assert (tmp_path / "en" / "locations_small.png").is_file()
    assert not (tmp_path / "en" / "locations_big_mobile.svg").exists()


def test_location_sorting_is_top_to_bottom_and_left_to_right():
    locations = object.__new__(Locations)
    locations.name = "castle"
    locations.graph = Graph(
        [("ROOM0", "ROOM1"), ("ROOM0", "ROOM2"), ("ROOM2", "ROOM3")]
    )

    assert locations.sort_locations() == ["room0", "room3", "room1", "room2"]


def test_train_location_sorting_follows_the_carriage_path():
    locations = object.__new__(Locations)
    locations.name = "train"
    locations.graph = Graph(
        [
            ("ROOM0", "ROOM1"),
            ("ROOM1", "ROOM2"),
            ("ROOM2", "ROOM3"),
            ("ROOM3", "ROOM4"),
        ]
    )

    assert locations.sort_locations() == [
        "room0",
        "room1",
        "room2",
        "room3",
        "room4",
    ]

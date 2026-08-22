"""Draw room maps directly as SVG and raster images.

Proof of concept for porting the book's TikZ room maps to the website.

The earlier generated maps had two problems that are fatal at small sizes: the
connectors stop short of the rooms, so they read as loose strokes rather than
doorways, and `dot` lays the graph out tall and narrow, wasting most of the
box. This draws the rooms on an ellipse instead, which has two useful
properties:

  * room positions expand from the preferred ellipse until their actual label
    boxes are separate and every corridor clears rooms it does not connect to;
    this avoids the old defect where a corridor running across an unrelated
    room reads as a door that is not there;
  * the drawing fills a landscape box, which is the shape the page and the
    web layout actually have.

Only the cyclic room order is free, so we choose the one with the fewest
corridor-corridor crossings.

Emoji stay as text in the SVG, so the browser renders them with its own colour
font.
"""

from functools import lru_cache
from itertools import combinations, permutations
from math import cos, pi, sin

import drawsvg as draw

# --- style -----------------------------------------------------------------
TILE = 34.0  # room tile side, px
RADIUS = 7.0  # corner rounding
STROKE = "#1a1a1a"  # tile outline
LINK = "#8a8a8a"  # corridor
LINK_W = 3.0
BIG_FILL = "#b2dfee"  # established light-blue fill for the overview map
BIG_RADIUS = 16.0
BIG_LINK = "#808080"
BIG_LINK_W = 1.4
TILE_W = 1.6
PAD = 6.0  # keeps strokes off the viewBox edge
ROOM_GAP = 8.0  # minimum clear space between unrelated room boxes
CORRIDOR_GAP = 4.0  # minimum clear space around an unrelated corridor


def _estimated_text_width(text, size):
    """Portable fallback for text advance when no matching font is available."""
    w = 0.0
    for ch in text:
        if ch in "\u200d\ufe0e\ufe0f":  # emoji joiners/selectors have no advance
            continue
        if ord(ch) > 0x2100:  # emoji and friends are about square
            w += 1.15
        elif ch in " iljtfr.,:;'!|":
            w += 0.32
        elif ch.isupper() or ch in "mwMW@":
            w += 0.68
        elif ord(ch) > 0x400:  # Cyrillic runs a touch wider
            w += 0.60
        else:
            w += 0.53
    return w * size


def _measured_text_width(text, size):
    """Measure Raleway runs and reserve a square-ish advance for each emoji."""
    font_size = max(1, round(size))
    font = _text_font(font_size)
    scale = size / font_size
    width = 0.0
    plain = []

    def flush_plain():
        nonlocal width
        if plain:
            width += font.getlength("".join(plain)) * scale
            plain.clear()

    for ch in text:
        if ch in "\u200d\ufe0e\ufe0f":
            continue
        if ord(ch) > 0x2100:
            flush_plain()
            width += 1.15 * size
        else:
            plain.append(ch)
    flush_plain()
    return width


def _text_width(text, size):
    """Conservative text advance shared by wrapping, SVG, and PNG layouts."""
    return max(_estimated_text_width(text, size), _measured_text_width(text, size))


def _wrap_inline_text(caption, label, font_size, max_width):
    """Wrap a room name and keep its glyph on the final line."""
    words = caption.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and _text_width(candidate, font_size) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate

    with_label = f"{current} {label}".strip()
    if current and _text_width(with_label, font_size) > max_width:
        lines.append(current)
        lines.append(label)
    else:
        lines.append(with_label)
    return lines


def _inline_text_layout(labels, captions, font_size, tile, inline, max_inline_width):
    """Text, box widths, wrapped lines, box height, and line height."""
    if not inline or not captions:
        return None, None, None, tile, font_size

    texts = [f"{caption} {label}" for caption, label in zip(captions, labels)]
    if max_inline_width is None:
        widths = [_text_width(text, font_size) + font_size for text in texts]
        return texts, widths, None, tile, font_size

    line_sets = [
        _wrap_inline_text(caption, label, font_size, max_inline_width)
        for caption, label in zip(captions, labels)
    ]
    widths = [
        max(_text_width(line, font_size) for line in lines) + font_size
        for lines in line_sets
    ]
    line_height = font_size * 1.2
    max_lines = max(len(lines) for lines in line_sets)
    box_height = max(tile, max_lines * line_height + font_size * 0.7)
    return texts, widths, line_sets, box_height, line_height


def _crossings(order, edges):
    """Corridor-corridor crossings for one cyclic ordering of the rooms."""
    pos = {room: i for i, room in enumerate(order)}
    es = [tuple(sorted((pos[a], pos[b]))) for a, b in edges]
    total = 0
    for (a1, b1), (a2, b2) in combinations(es, 2):
        if len({a1, b1, a2, b2}) < 4:
            continue
        # they cross iff exactly one endpoint of the second lies between the
        # endpoints of the first, going round the circle
        if ((a1 < a2 < b1) + (a1 < b2 < b1)) == 1:
            total += 1
    return total


def best_order(n, edges, budget=5040):
    """Cyclic ordering of n rooms with the fewest crossings.

    The first room is pinned: rotations are equivalent, so only (n-1)!
    orderings are distinct. Exhaustive up to 8 rooms, which covers every map
    the generator makes; beyond that we keep the best of a truncated search.
    """
    best, best_cost = list(range(n)), None
    if n <= 2:
        return best
    for seen, perm in enumerate(permutations(range(1, n)), start=1):
        order = [0] + list(perm)
        cost = _crossings(order, edges)
        if best_cost is None or cost < best_cost:
            best, best_cost = order, cost
            if cost == 0:
                break
        if seen >= budget:
            break
    return best


def _path_order(n, edges):
    """Return one end-to-end ordering for a path graph."""
    neighbours = {room: [] for room in range(n)}
    for start, end in edges:
        neighbours[start].append(end)
        neighbours[end].append(start)

    endpoints = [room for room, adjacent in neighbours.items() if len(adjacent) == 1]
    if n == 1:
        return [0]
    if len(edges) != n - 1 or len(endpoints) != 2:
        raise ValueError("vertical room-map layout requires a path graph")

    order = []
    previous = None
    current = min(endpoints)
    while current is not None:
        order.append(current)
        candidates = [room for room in neighbours[current] if room != previous]
        previous, current = current, candidates[0] if candidates else None

    if len(order) != n:
        raise ValueError("vertical room-map layout requires a connected path graph")
    return order


def layout(n, edges, rx, ry, vertical=False):
    """Room centres in a vertical path or least-crossing ellipse."""
    order = _path_order(n, edges) if vertical else best_order(n, edges)
    pts = {}
    for slot, room in enumerate(order):
        if vertical:
            pts[room] = (0.0, (slot - (n - 1) / 2.0) * ry)
        else:
            ang = -pi / 2 + 2 * pi * slot / n  # first room at the top
            pts[room] = (rx * cos(ang), ry * sin(ang))
    return pts


def _segment_intersects_box(start, end, center, width, height):
    """Whether a closed line segment touches an axis-aligned rectangle."""
    x1, y1 = start
    x2, y2 = end
    cx, cy = center
    dx, dy = x2 - x1, y2 - y1
    lower_t, upper_t = 0.0, 1.0

    for origin, delta, lower, upper in (
        (x1, dx, cx - width / 2.0, cx + width / 2.0),
        (y1, dy, cy - height / 2.0, cy + height / 2.0),
    ):
        if abs(delta) < 1e-12:
            if origin < lower or origin > upper:
                return False
            continue

        first = (lower - origin) / delta
        second = (upper - origin) / delta
        lower_t = max(lower_t, min(first, second))
        upper_t = min(upper_t, max(first, second))
        if lower_t > upper_t:
            return False

    return True


def _layout_is_clear(
    points,
    edges,
    widths,
    height,
    room_gap=ROOM_GAP,
    corridor_gap=CORRIDOR_GAP,
):
    """Check room-room and corridor-room clearance for one positioned map."""
    for first, second in combinations(range(len(widths)), 2):
        dx = abs(points[first][0] - points[second][0])
        dy = abs(points[first][1] - points[second][1])
        required_x = (widths[first] + widths[second]) / 2.0 + room_gap
        required_y = height + room_gap
        if dx < required_x and dy < required_y:
            return False

    for start, end in edges:
        for room in range(len(widths)):
            if room in (start, end):
                continue
            if _segment_intersects_box(
                points[start],
                points[end],
                points[room],
                widths[room] + 2.0 * corridor_gap,
                height + 2.0 * corridor_gap,
            ):
                return False
    return True


def _fit_layout(
    n,
    edges,
    widths,
    height,
    rx,
    ry,
    vertical=False,
    room_gap=ROOM_GAP,
    corridor_gap=CORRIDOR_GAP,
):
    """Grow a preferred layout only when its actual room boxes need space."""
    if vertical:
        centre_gap = max(ry, height + room_gap)
        return layout(n, edges, rx, centre_gap, vertical=True)

    preferred = layout(n, edges, rx, ry)

    def scaled(scale):
        return {
            room: (point[0] * scale, point[1] * scale)
            for room, point in preferred.items()
        }

    def clear(scale):
        return _layout_is_clear(
            scaled(scale),
            edges,
            widths,
            height,
            room_gap=room_gap,
            corridor_gap=corridor_gap,
        )

    if clear(1.0):
        return preferred

    lower, upper = 1.0, 2.0
    for _ in range(32):
        if clear(upper):
            break
        lower, upper = upper, upper * 2.0
    else:
        raise ValueError("could not find a non-overlapping room-map layout")

    for _ in range(48):
        middle = (lower + upper) / 2.0
        if clear(middle):
            upper = middle
        else:
            lower = middle
    return scaled(upper)


def _trimmed_edge(start, end, start_width, end_width, height):
    """Clip a centre-to-centre corridor to rectangular room boundaries."""
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return x1, y1, x2, y2

    def boundary_fraction(width):
        horizontal = width / (2.0 * abs(dx)) if dx else float("inf")
        vertical = height / (2.0 * abs(dy)) if dy else float("inf")
        return min(horizontal, vertical)

    start_fraction = boundary_fraction(start_width)
    end_fraction = boundary_fraction(end_width)
    return (
        x1 + dx * start_fraction,
        y1 + dy * start_fraction,
        x2 - dx * end_fraction,
        y2 - dy * end_fraction,
    )


CAPTION_SIZE = 13.0
CAPTION_GAP = 5.0
TEXT_FONT_PLAIN = "Raleway, -apple-system, Helvetica, Arial, sans-serif"
TEXT_FONT = (
    "Raleway, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, "
    "Helvetica, Arial, sans-serif"
)


def _svg_text(text, size, x, y, family, **attributes):
    """Create consistently positioned SVG text through drawsvg."""
    return draw.Text(
        text, size, f"{x:.1f}", f"{y:.1f}", font_family=family, **attributes
    )


def render(
    labels,
    edges,
    rx=78.0,
    ry=52.0,
    tile=TILE,
    font_size=20.0,
    captions=None,
    inline=False,
    fill="#ffffff",
    vertical=False,
    draw_tiles=True,
    radius=RADIUS,
    stroke=STROKE,
    link=LINK,
    link_width=LINK_W,
    max_inline_width=None,
    edge_styles=None,
):
    """SVG for a map.

    labels   -- room glyphs, one per room, in index order
    edges    -- (i, j) index pairs, one per corridor
    captions -- optional room names. With inline=False they are drawn under
                each tile; with inline=True the box grows to hold
                "name glyph" inside a filled, rounded room label, wrapping
                long names when max_inline_width is set.
    fill     -- box fill colour.
    vertical -- arrange a path graph from top to bottom instead of on an ellipse.
    draw_tiles -- draw room boxes; glyph-only maps clip corridors to their bounds.
    max_inline_width -- wrap inline room labels at this approximate pixel width.
    edge_styles -- optional SVG attribute overrides keyed by an edge tuple.
    """
    n = len(labels)
    texts, widths, line_sets, box_height, line_height = _inline_text_layout(
        labels, captions, font_size, tile, inline, max_inline_width
    )
    room_widths = widths if widths else [tile] * n
    pts = _fit_layout(
        n,
        edges,
        room_widths,
        box_height,
        rx,
        ry,
        vertical=vertical,
    )
    half_width = tile / 2.0
    half_height = box_height / 2.0
    xs = [p[0] for p in pts.values()]
    ys = [p[1] for p in pts.values()]
    if widths:
        cap_h, hw = 0.0, max(widths) / 2.0
        minx, maxx = min(xs) - hw - PAD, max(xs) + hw + PAD
    else:
        cap_h = (CAPTION_GAP + CAPTION_SIZE) if captions else 0.0
        hw = half_width + (
            max((len(c) for c in captions), default=0) * CAPTION_SIZE * 0.55 / 2
            if captions
            else 0.0
        )
        minx, maxx = min(xs) - hw - PAD, max(xs) + hw + PAD
    miny = min(ys) - half_height - PAD
    maxy = max(ys) + half_height + PAD + cap_h
    w, h = maxx - minx, maxy - miny

    drawing = draw.Drawing(
        w,
        h,
        origin=(minx, miny),
        role="img",
        aria_label="map of the rooms and the corridors between them",
    )
    drawing.view_box = tuple(
        f"{value:.1f}"
        for value in (
            minx,
            miny,
            w,
            h,
        )
    )
    drawing.set_render_size(w=round(w), h=round(h))
    group = draw.Group()
    drawing.append(group)

    # Corridors come first. Filled tiles hide their line ends; glyph-only maps
    # trim the lines to the same room bounds instead.
    for a, b in edges:
        (x1, y1), (x2, y2) = pts[a], pts[b]
        if not draw_tiles:
            x1, y1, x2, y2 = _trimmed_edge(
                pts[a],
                pts[b],
                room_widths[a],
                room_widths[b],
                box_height,
            )
        line_style = {
            "stroke": link,
            "stroke_width": link_width,
            "stroke_linecap": "round",
        }
        if edge_styles:
            line_style.update(edge_styles.get((a, b), edge_styles.get((b, a), {})))
        group.append(
            draw.Line(
                f"{x1:.1f}",
                f"{y1:.1f}",
                f"{x2:.1f}",
                f"{y2:.1f}",
                **line_style,
            )
        )

    for i, label in enumerate(labels):
        x, y = pts[i]
        bw = widths[i] if widths else tile
        if draw_tiles:
            group.append(
                draw.Rectangle(
                    f"{x - bw / 2:.1f}",
                    f"{y - half_height:.1f}",
                    f"{bw:.1f}",
                    f"{box_height:.1f}",
                    rx=radius,
                    ry=radius,
                    fill=fill,
                    stroke=stroke,
                    stroke_width=TILE_W,
                )
            )
        family = (
            "Apple Color Emoji, Noto Color Emoji, Segoe UI Emoji, sans-serif"
            if not texts
            else f"{TEXT_FONT_PLAIN}, Apple Color Emoji, "
            "Noto Color Emoji, Segoe UI Emoji"
        )
        if line_sets:
            group.append(
                _svg_text(
                    line_sets[i],
                    font_size,
                    x,
                    y,
                    family,
                    center=True,
                    line_height=line_height / font_size,
                    line_offset=-0.5,
                    tspan_args={"dominant_baseline": "central"},
                )
            )
        else:
            body = texts[i] if texts else label
            group.append(_svg_text(body, font_size, x, y, family, center=True))
        if captions and not inline:
            group.append(
                _svg_text(
                    captions[i],
                    CAPTION_SIZE,
                    x,
                    y + half_height + CAPTION_GAP + CAPTION_SIZE * 0.8,
                    TEXT_FONT,
                    text_anchor="middle",
                    fill="#333",
                )
            )

    return drawing.as_svg(header="")


def positions(labels, edges, rx=78.0, ry=52.0, vertical=False):
    """Room centres, in drawing coordinates (y grows downward, as in SVG)."""
    return layout(len(labels), edges, rx, ry, vertical=vertical)


def render_png(
    labels,
    edges,
    path,
    scale=3.0,
    rx=78.0,
    ry=52.0,
    tile=TILE,
    font_size=20.0,
    captions=None,
    inline=False,
    fill="#ffffff",
    vertical=False,
    draw_tiles=True,
    radius=RADIUS,
    stroke=STROKE,
    link=LINK,
    link_width=LINK_W,
    max_inline_width=None,
):
    """Same drawing, rasterised. Only the Kindle view uses the PNGs.

    Drawn directly rather than by rasterising the SVG, so Pillow is the only
    image-rendering dependency.
    """
    from PIL import Image, ImageDraw

    n = len(labels)
    texts, widths, line_sets, box_height, line_height = _inline_text_layout(
        labels, captions, font_size, tile, inline, max_inline_width
    )
    room_widths = widths if widths else [tile] * n
    pts = _fit_layout(
        n,
        edges,
        room_widths,
        box_height,
        rx,
        ry,
        vertical=vertical,
    )
    half_width = tile / 2.0
    half_height = box_height / 2.0
    xs = [p[0] for p in pts.values()]
    ys = [p[1] for p in pts.values()]
    if widths:
        cap_h, hw = 0.0, max(widths) / 2.0
    else:
        cap_h = (CAPTION_GAP + CAPTION_SIZE) if captions else 0.0
        hw = half_width + (
            max((len(c) for c in captions), default=0) * CAPTION_SIZE * 0.55 / 2
            if captions
            else 0.0
        )
    minx, miny = min(xs) - hw - PAD, min(ys) - half_height - PAD
    w = (max(xs) + hw + PAD) - minx
    h = (max(ys) + half_height + PAD + cap_h) - miny

    S = scale
    im = Image.new("RGBA", (int(w * S), int(h * S)), (255, 255, 255, 0))
    d = ImageDraw.Draw(im)
    px = lambda p: ((p[0] - minx) * S, (p[1] - miny) * S)

    for a, b in edges:
        start, end = pts[a], pts[b]
        if not draw_tiles:
            x1, y1, x2, y2 = _trimmed_edge(
                start,
                end,
                room_widths[a],
                room_widths[b],
                box_height,
            )
            start, end = (x1, y1), (x2, y2)
        d.line(
            [px(start), px(end)],
            fill=link,
            width=max(1, int(link_width * S)),
        )
    font = _emoji_font(int(font_size * S))
    for i, label in enumerate(labels):
        x, y = px(pts[i])
        bw = (widths[i] if widths else tile) * S
        if draw_tiles:
            d.rounded_rectangle(
                [
                    x - bw / 2,
                    y - half_height * S,
                    x + bw / 2,
                    y + half_height * S,
                ],
                radius=radius * S,
                fill=fill,
                outline=stroke,
                width=max(1, int(TILE_W * S)),
            )
        if line_sets:
            tf = _text_font(int(font_size * S))
            for line_index, line in enumerate(line_sets[i]):
                line_y = (
                    y + (line_index - (len(line_sets[i]) - 1) / 2.0) * line_height * S
                )
                if line.endswith(label):
                    prefix = line[: -len(label)].rstrip()
                    name = f"{prefix} " if prefix else ""
                    nw = d.textlength(name, font=tf) if name else 0.0
                    gw = font_size * S * 1.15 if font is not None else 0.0
                    start = x - (nw + gw) / 2.0
                    if name:
                        d.text(
                            (start, line_y),
                            name,
                            font=tf,
                            anchor="lm",
                            fill="#111111",
                        )
                    if font is not None:
                        d.text(
                            (start + nw + gw / 2.0, line_y),
                            label,
                            font=font,
                            anchor="mm",
                            embedded_color=True,
                        )
                else:
                    d.text((x, line_y), line, font=tf, anchor="mm", fill="#111111")
        elif texts:
            # the emoji font carries no letters and the text font no emoji, so
            # the name and the glyph are drawn separately, side by side
            tf = _text_font(int(font_size * S))
            name = captions[i] + " "
            nw = d.textlength(name, font=tf)
            gw = font_size * S * 1.15
            start = x - (nw + gw) / 2
            d.text((start, y), name, font=tf, anchor="lm", fill="#111111")
            if font is not None:
                d.text(
                    (start + nw + gw / 2, y),
                    label,
                    font=font,
                    anchor="mm",
                    embedded_color=True,
                )
        elif font is not None:
            d.text((x, y), label, font=font, anchor="mm", embedded_color=True)
        if captions and not inline:
            tf = _text_font(int(CAPTION_SIZE * S))
            d.text(
                (x, y + (half_height + CAPTION_GAP) * S),
                captions[i],
                font=tf,
                anchor="ma",
                fill="#333333",
            )
    im.save(path, optimize=True)


@lru_cache(maxsize=None)  # noqa: UP033 -- deployment still runs Python 3.8
def _text_font(size):
    """Load Raleway for room names, with platform fonts as fallbacks."""
    import glob
    from os.path import expanduser

    from PIL import ImageFont

    for pattern in (
        "~/.local/share/fonts/**/Raleway-Regular.ttf",
        "~/.local/share/fonts/**/Raleway-Regular.otf",
        "~/Library/Fonts/Raleway-Regular.otf",
        "~/Library/Fonts/Raleway-Regular.ttf",
        "~/Library/Fonts/Raleway-VF.ttf",
        "~/Library/Fonts/google-fonts/ofl/raleway/Raleway[[]wght].ttf",
        "/usr/share/fonts/**/Raleway-Regular.ttf",
        "/usr/share/fonts/**/Raleway-Regular.otf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/**/DejaVuSans.ttf",
    ):
        for cand in sorted(glob.glob(expanduser(pattern), recursive=True)):
            try:
                return ImageFont.truetype(cand, size)
            except OSError:
                continue
    return ImageFont.load_default()


def _emoji_font(size):
    """A colour emoji font, if the platform has one."""
    import glob
    from os.path import expanduser

    from PIL import ImageFont

    for pattern in (
        "/System/Library/Fonts/Apple Color Emoji.ttc",
        "~/.local/share/fonts/**/NotoColorEmoji*.ttf",
        "~/.local/share/fonts/**/NotoEmoji*.ttf",
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
        "/usr/share/fonts/**/NotoColorEmoji*.ttf",
        "/usr/share/fonts/**/NotoEmoji*.ttf",
    ):
        for cand in sorted(glob.glob(expanduser(pattern), recursive=True)):
            # Apple's bitmap emoji font only accepts specific sizes.
            for candidate_size in (size, 137, 96, 64):
                try:
                    return ImageFont.truetype(cand, candidate_size)
                except OSError:
                    continue
    return None

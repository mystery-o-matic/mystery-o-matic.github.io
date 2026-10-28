from os import remove
from os.path import isfile
from shutil import copytree
from string import Template
from yattag import Doc, indent
from json import dump
import re

from mystery_o_matic.output import create_template
from mystery_o_matic.time import Time


def read_html_template(filename):
    with open(filename, "r") as f:
        template = create_template(f.read())
        return template


def save_html(outdir, language, html):
    filename = outdir + f"/{language}/index.html"
    with open(filename, "w") as f:
        f.write(html)

    return filename


def save_json(outdir, prefix, data):
    filename = outdir + "/data.js"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(prefix)
        dump(data, f, ensure_ascii=False, indent=4)


# These words refer to public facts in the case introduction. Resolving them
# never requires identifying an anonymous witness or solving the murder.
PUBLIC_CLUE_REFERENCES = {
    "en": (r"\bthe victim\b", r"\bthe crime scene\b", r"\bthe body\b"),
    "es": (r"\bla víctima\b", r"\bescena del crimen\b", r"\bcuerpo\b"),
    "ru": (r"\bжертв[аыуе]\b", r"\bмест[ае] преступления\b", r"\bтел[аое]\b"),
}
VICTIM_SCREAM_REFERENCES = {
    "en": r"\bscream from the victim\b",
    "es": r"\bgrito espeluznante de la víctima\b",
    "ru": r"\bкрик жертвы\b",
}
TIME_REFERENCE = r"(?<![\d:])\d{1,2}:\d{2}(?![\d:])"
# Recognize an explicit range in the displayed wording, not just two times.
# In particular, "either ... or ..." and before/after bounds are not ranges.
TIME_RANGE_REFERENCES = {
    "en": (
        rf"\bbetween\s+({TIME_REFERENCE})\s+and\s+({TIME_REFERENCE})",
        rf"\bfrom\s+({TIME_REFERENCE})\s+(?:to|until)\s+({TIME_REFERENCE})",
        rf"\bat\s+({TIME_REFERENCE})\s+and\s+stayed\s+until\s+({TIME_REFERENCE})",
    ),
    "es": (
        rf"\bentre\s+las\s+({TIME_REFERENCE})\s+y\s+las\s+({TIME_REFERENCE})",
        rf"\bdesde\s+las\s+({TIME_REFERENCE})\s+hasta\s+las\s+({TIME_REFERENCE})",
        rf"\ba\s+las\s+({TIME_REFERENCE})\s+y\s+me\s+quedé\s+hasta\s+las\s+({TIME_REFERENCE})",
    ),
    "ru": (
        rf"\bмежду\s+({TIME_REFERENCE})\s+и\s+({TIME_REFERENCE})",
        rf"\bс\s+({TIME_REFERENCE})\s+до\s+({TIME_REFERENCE})",
    ),
}


def get_clue_highlights(text, characters, intervals, *, language="en", victim=None,
                        crime_scene=None, room_labels=None):
    """Return explicit references, resolving victim/body/scene from public facts.

    Use the already-rendered wording, never the clue's hidden subject/object or
    time fields. In particular, $TELL_CHARn and $DESC_CHARn do not name a person,
    and "not before" can display a different time from the stored clue time.
    Rows use character names; columns use clock labels shared by all room tables;
    tables use room IDs. Victim and crime_scene come from the case introduction.
    Rows are scoped to explicitly referenced rooms via tableRows. If no room is
    referenced, rows apply to all tables. Pre-rendered activity text is matched
    against localized room labels, never against a clue's hidden place field.
    The victim's scream uses the public crime scene, just like murder-time clues.
    Body inspections only guide these tables when they state a time; weapon
    clues describing wounds do not highlight the victim or crime scene.
    Explicit time ranges include every displayed column between their endpoints.
    Separate alternatives and one-sided bounds highlight only their printed times,
    without filling in deductions.
    """
    tokens = {
        match.group("named") or match.group("braced")
        for match in create_template(text).pattern.finditer(text)
    }
    column_times = {time: Time(time).seconds for time in intervals}
    times = {Time(time).seconds for time in re.findall(TIME_REFERENCE, text)}
    for pattern in TIME_RANGE_REFERENCES[language]:
        for start, end in re.findall(pattern, text, re.IGNORECASE):
            start, end = Time(start).seconds, Time(end).seconds
            times.update(time for time in column_times.values() if start <= time <= end)
    mentions_scream = re.search(VICTIM_SCREAM_REFERENCES[language], text, re.IGNORECASE)
    rows = {
        name.lower() for i, name in enumerate(characters, 1)
        if "CHAR" + str(i) in tokens
    }
    tables = {
        token.split("_")[0].lower() for token in tokens
        if token and re.fullmatch(r"ROOM\d+(?:_LOC|_GEN)?", token)
    }
    # Ambient clues already contain the localized room name and icon, instead
    # of a $ROOMn token. Match that exact visible label, including Russian cases.
    tables.update(
        room for room, labels in (room_labels or {}).items()
        if any(label in text for label in labels)
    )
    victim_pattern, scene_pattern, body_pattern = PUBLIC_CLUE_REFERENCES[language]
    mentions_scene = (
        re.search(scene_pattern, text, re.IGNORECASE)
        or mentions_scream
        or (times and re.search(body_pattern, text, re.IGNORECASE))
    )
    if victim and (mentions_scene or re.search(victim_pattern, text, re.IGNORECASE)):
        rows.add(victim.lower())
    if crime_scene and mentions_scene:
        tables.add(crime_scene)
    highlights = {
        "rows": [] if tables else sorted(rows),
        "columns": [label for label, time in column_times.items() if time in times],
        "tables": sorted(tables),
    }
    if tables and rows:
        highlights["tableRows"] = {room: sorted(rows) for room in sorted(tables)}
    return highlights


def read_story(season, date):
    filename = "story/season-" + str(season) + "/" + date + ".html"
    if not isfile(filename):
        return ""

    with open(filename, "r") as f:
        return f.read()


def build_website(outdir, static_dir, language, html):
    copytree(static_dir, outdir, dirs_exist_ok=True)
    save_html(outdir, language, html)
    remove(outdir + f"/{language}/index.template.html")


def get_clue_table(name, height, width):

    html = f"""				<div class="col-12 text-center">
					<canvas id="clues-table-{name}" oncontextmenu="return false" height="{height}" width="{width}" onclick="checkCellClicked(this, event.offsetX, event.offsetY)">
						Your browser does not support the HTML canvas tag.</canvas>
				</div>
    """
    return html

def get_bullet_list(elements, name=""):
    doc, tag, text, line = Doc().ttl()

    with tag("ul", id=name):
        for element in elements:
            doc.asis("<li>")
            doc.asis(element)
            doc.asis("</li>")

    return indent(doc.getvalue())


def get_options_selector(elements, name="", notranslate=False):
    doc, tag, text, line = Doc().ttl()

    for label, value in elements:
        line("option", label, value=value)

    return indent(doc.getvalue())


def get_subtitle(subtitle, name=""):
    doc, tag, text, _ = Doc().ttl()
    with tag("h3"):
        text(subtitle)
    return indent(doc.getvalue())

def get_char_name(name):
    if name == "NOBODY":
        return name
    return (
        '<a href="#/" class="link-dark" onClick="openModalChar(event, \''
        + name.lower()
        + "')\">"
        + name.capitalize()
        + "</a>"
    )

def get_weapon_type_name(name, label=None):
    if label is None:
        label = name.lower()
    return (
        '<a href="#/" class="link-dark" onClick="openModalWeaponType(event, \''
        + name.lower()
        + "')\">"
        + label
        + "</a>"
    )

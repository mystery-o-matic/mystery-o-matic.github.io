from os import remove
from os.path import isfile
from shutil import copytree
from yattag import Doc, indent
from json import dump

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


def get_clue_highlights(clue, characters, intervals, *, victim=None, crime_scene=None):
    """Map a clue's declared public references to the table IDs and columns.

    The clue owns visibility decisions, including vagueness and changed alibis.
    This adapter never inspects rendered text or hidden event fields.
    """
    references = clue.highlight_references
    names = {"$CHAR" + str(i): name.lower() for i, name in enumerate(characters, 1)}
    rows = {names[character] for character in references.characters}
    tables = {room.lstrip("$").lower() for room in references.rooms}
    if references.victim_at_scene:
        if victim:
            rows.add(victim.lower())
        if crime_scene:
            tables.add(crime_scene)

    column_times = {label: Time(label).seconds for label in intervals}
    times = set(references.times)
    columns = [
        label for label, time in column_times.items()
        if time in times or any(start <= time <= end for start, end in references.time_ranges)
    ]
    highlights = {
        "rows": [] if tables else sorted(rows),
        "columns": columns,
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

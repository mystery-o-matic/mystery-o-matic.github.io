from os import remove
from os.path import isfile
from shutil import copytree
from string import Template
from yattag import Doc, indent
from json import dump

from mystery_o_matic.output import create_template


def read_html_template(filename):
    with open(filename, "r") as f:
        template = create_template(f.read())
        return template


def save_html(outdir, html):
    filename = outdir + "/index.html"
    with open(filename, "w") as f:
        f.write(html)

    return filename


def save_json(outdir, prefix, data):
    filename = outdir + "/data.js"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(prefix)
        dump(data, f, ensure_ascii=False, indent=4)


def read_story(season, date):
    filename = "story/season-" + str(season) + "/" + date + ".html"
    if not isfile(filename):
        return ""

    with open(filename, "r") as f:
        return f.read()


def build_website(outdir, static_dir, html):
    save_html(outdir, html)
    copytree(static_dir, outdir, dirs_exist_ok=True)
    remove(outdir + "/index.template.html")


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

    for i, element in enumerate(elements):
        if notranslate:
            line("option", element, value=element, klass="notranslate")
        else:
            line("option", element, value=element)

    return indent(doc.getvalue())


def get_subtitle(subtitle, name=""):
    doc, tag, text, _ = Doc().ttl()
    with tag("h3"):
        text(subtitle)
    return indent(doc.getvalue())


def get_clues_list(elements):
    html = ""
    for element in elements:
        html += get_card(element)
        html += "\n"
    return html

# TODO: rewrite using yattag
def get_card(title, inner_html, index):
    html_template = """<div class="card" style="display:none; height: 10rem;" id="clue-$index">
  <div class="card-body">
    <h5 class="card-title">$title</h5>
    <p class="card-text" onClick="toggleClueStrikeout(this)">$innerHTML</p>
  </div>
</div>"""
    html_template = Template(html_template)
    return html_template.substitute(title=title, innerHTML=inner_html, index=index)


def get_char_name(name):
    if name == "NOBODY":
        return name
    return (
        '<a href="#/" class="link-dark" onClick="openModal(\''
        + name.lower()
        + "')\">"
        + name.capitalize()
        + "</a>"
    )

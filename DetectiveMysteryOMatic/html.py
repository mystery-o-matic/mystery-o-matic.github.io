from os import remove
from shutil import copytree
from string import Template
from yattag import Doc, indent

def create_template(str):
	return Template(str)

def read_html_template(filename):
	with open(filename, 'r') as f:
		template = create_template(f.read())
		return template


def save_html(outdir, html):
	filename = outdir + "/index.html"
	with open(filename, 'w') as f:
		f.write(html)

	return filename

def build_website(outdir, static_dir, html):
	save_html(outdir, html)
	copytree(static_dir, outdir, dirs_exist_ok=True)
	remove(outdir + "/index.template.html")

def get_bullet_list(elements, name = ''):
	doc, tag, text, line = Doc().ttl()

	with tag('ul', id = name):
		for element in elements:
			line('li', element, klass="priority")

	return indent(doc.getvalue())

def get_options_selector(elements, name = ''):
	doc, tag, text, line = Doc().ttl()

	for i, element in enumerate(elements):
		line('option', element, value=element)

	return indent(doc.getvalue())

def get_subtitle(subtitle, name = ''):
	doc, tag, text, _ = Doc().ttl()
	with tag('h3'):
		text(subtitle)
	return indent(doc.getvalue())

def get_clues_list(elements):
	html = ""
	for element in elements:
		html += get_accordion(element)
		html += "\n"
	return html

def get_accordion(title, inner_html, index):
	html_template = """
	<div class="accordion">
  <div class="accordion-item">
    <h2 class="accordion-header" id="panelsStayOpen-heading-$index">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" aria-expanded="false" data-bs-target="#panelsStayOpen-collapse-$index" aria-controls="panelsStayOpen-collapse-$index" onClick="markedAsViewed(this)">
        $title
      </button>
    </h2>
    <div id="panelsStayOpen-collapse-$index" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-heading-$index">
      <div class="accordion-body" onClick="toggleClueStrikeout(this)">
	    $innerHTML
      </div>
	</div>
  </div>
</div>"""
	html_template = Template(html_template)
	return html_template.substitute(title = title, innerHTML = inner_html, index = index)

def get_char_name(name):
	if (name == "NOBODY"):
		return name
	return '<a href="#/" class="link-dark" onClick="openModal(\''+ name.lower() + '\')">' + name.capitalize() + '</a>'

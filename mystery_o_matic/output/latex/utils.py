from contextlib import suppress
from os import makedirs
from string import Template

from emoji import demojize

class TexTemplate(Template):
    delimiter = "$$"

def create_tex_template(str):
    return TexTemplate(str)

def read_tex_template(filename):
    try:
        with open(filename, "r", encoding='utf-8') as f:
            template = create_tex_template(f.read())
            return template
    except FileNotFoundError:
        raise ValueError(f"Template file not found: {filename}")
    except UnicodeDecodeError:
        raise ValueError(f"Template file has invalid encoding: {filename}")

def get_bullet_list(elements, name=""):
    r = "\\begin{itemize}\n"
    for element in elements:
        r += "\\item " + element + "\n"
    r += "\\end{itemize}"
    return r

def get_enumeration_list(elements, name=""):
    r = "\\begin{enumerate}\n"
    for element in elements:
        r += "\\item " + element + "\n"
    r += "\\end{enumerate}"
    return r

def save_tex(outdir, language, tex):
    output_dir = f"{outdir}/{language}"
    with suppress(OSError):
        makedirs(output_dir)

    filename = f"{output_dir}/mystery.tex"
    try:
        with open(filename, "w", encoding='utf-8') as f:
            f.write(tex)
    except OSError as e:
        raise RuntimeError(f"Failed to save LaTeX file: {e}")

    return filename

def get_char_name(name):
    if name == "NOBODY":
        return name
    return name.capitalize()

def get_emoji_name(emoji_char):
    # Use emoji.demojize to get the name in the format ":emoji_name:"
    emoji_name = demojize(emoji_char)
    emoji_name = emoji_name.strip(":").replace("_", "-")
    # Strip the colons to return just the canonical name
    return "\\emoji{" + emoji_name + "}"

def replace_emojis(text):
    no_emojis = demojize(text).replace("(:", "(\\emoji{")
    no_emojis = no_emojis.replace(":)", "})")
    no_emojis = no_emojis.replace("_", "-")
    return no_emojis

def generate_latex_clue_table(name, num_columns, num_rows, include_header = True):
    # Define the LaTeX column specifier string
    column_spec = '|c|c|' + '|'.join(['>{\\centering}m{0.04\\paperwidth}' for _ in range(num_columns)]) + '|'

    # Start building the LaTeX table code
    latex_code = "\\begin{tabular}{" + column_spec + "}\n\\hline\n"

    # First row with $$ROOM0REP and times

    multirow_number = num_rows
    if (include_header):
        multirow_number += 1

    latex_code += "\\multirow{ "+ str(multirow_number) + "}{*}{ $$" + name + " } "

    if (include_header):
        latex_code += "& \\emoji{mantelpiece-clock} & "
        # Add the $$TIME elements in the first row
        time_cells = [f"$$TIME{i}" for i in range(num_columns)]
        latex_code += " & ".join(time_cells) + " \\tabularnewline\n"

        # Add individual clines for each column from the second to the last
        for col in range(2, num_columns + 2):
            latex_code += f"\\cline{{{col}-{num_columns + 2}}} "
        latex_code += "\n"

    # Rows with $$CHAR1, $$CHAR2, $$CHAR3
    for char_num in range(1, num_rows + 1):
        latex_code += f" & $$CHAR{char_num} & " + " & ".join([""] * num_columns) + " \\tabularnewline\n"

        # Add individual clines for each column in the current row
        if (char_num < 3):
            for col in range(2, num_columns + 2):
                latex_code += f"\\cline{{{col}-{num_columns + 2}}} "
            latex_code += "\n"

    # End the table
    latex_code += "\\hline\n\\end{tabular}\\\\\n"

    return latex_code

def generate_latex_weapons_table(number_weapons):
    latex_code = '\\begin{tabular}{|>{\centering}p{0.172\paperwidth}|>{\centering}p{0.172\paperwidth}|>{\centering}p{0.172\paperwidth}|>{\centering}p{0.172\paperwidth}|}\n'
    latex_code += "\\hline\n"
    for i in range(number_weapons):
        latex_code += f"$$ROOM{i}WEAPONREP & "

    latex_code = latex_code[:-2] + " \\tabularnewline\n"
    latex_code += "\\hline\n\\end{tabular}\n"
    return latex_code

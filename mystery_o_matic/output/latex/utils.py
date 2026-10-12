from contextlib import suppress
from os import makedirs
import re
from string import Template

from emoji import demojize


class TexTemplate(Template):
    delimiter = "$$"


def create_tex_template(str):
    return TexTemplate(str)


def get_bullet_list(elements, customItem=None):
    r = "\\begin{itemize}\n"
    for element in elements:
        if customItem is not None:
            r += f"\\item[{customItem}] " + element + "\n"
        else:
            r += "\\item " + element + "\n"
    r += "\\end{itemize}"
    return r


def get_enumeration_list(elements):
    r = "\\begin{enumerate}\n"
    for element in elements:
        r += "\\item " + element + "\n"
    r += "\\end{enumerate}"
    return r


def save_solution(outdir, solution):
    with suppress(OSError):
        makedirs(outdir)

    filename = f"{outdir}/solution.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(solution)
    except OSError as e:
        raise RuntimeError(f"Failed to save content to file: {e}")


def save_tex(outdir, language, tex, filename):
    output_dir = f"{outdir}/{language}"
    with suppress(OSError):
        makedirs(output_dir)

    filename = f"{output_dir}/{filename}"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(tex)
    except OSError as e:
        raise RuntimeError(f"Failed to save LaTeX file: {e}")

    return filename


def get_char_name(name):
    if name == "NOBODY":
        return name
    return "\\textbf{" + name.capitalize() + "}"


def get_emoji_name(emoji_char):
    # Use emoji.demojize to get the name in the format ":emoji_name:"
    emoji_name = demojize(emoji_char)
    emoji_name = emoji_name.strip(":").replace("_", "-").lower()
    # Strip the colons to return just the canonical name
    return "\\emoji{" + emoji_name + "}"


def replace_emojis(text):
    no_emojis = demojize(text).replace("(:", "(\\emoji{")
    no_emojis = no_emojis.replace(":)", "})")
    no_emojis = no_emojis.replace("_", "-")
    # The emoji package uses lowercase names, including t-rex.
    no_emojis = re.sub(
        r"\\emoji\{([^}]+)\}",
        lambda match: "\\emoji{" + match.group(1).lower() + "}",
        no_emojis,
    )
    return no_emojis


def replace_opening_quotes(text):
    text = text.replace(' "', " ``")
    if text.startswith('"'):
        return "``" + text[1:]
    return text


def generate_latex_clue_table(
    name, num_columns, char_names, final_locs, victim, include_header=True
):
    num_rows = len(char_names)
    # Define the LaTeX column specifier string
    column_spec = (
        "|>{\\centering}m{0.025\\paperwidth}|c|"
        + "|".join([">{\\centering}m{0.030\\paperwidth}" for _ in range(num_columns)])
        + "|"
    )

    # Start building the LaTeX table code
    latex_code = "\\begin{tabular}{" + column_spec + "}\n\\hline\n"

    # First row with $$ROOM0REP and times

    multirow_number = num_rows
    if include_header:
        multirow_number += 1

    latex_code += (
        "\\multirow{ "
        + str(multirow_number)
        + "}{*}{ \\negthinspace\\negthickspace{}$$"
        + name
        + " } "
    )

    if include_header:
        latex_code += "& {\\footnotesize{}\\emoji{mantelpiece-clock}} & "
        # Add the $$TIME elements in the first row
        time_cells = [
            "{\\footnotesize{}" + f"$$TIME{i}" + "}" for i in range(num_columns)
        ]
        latex_code += " & ".join(time_cells) + " \\tabularnewline\n"

        latex_code += "\\hhline{~|" + "-|" * (num_columns + 1) + "}\n"

    # Sort the characters by name
    char_nums = sorted(range(1, num_rows + 1), key=lambda k: char_names[k - 1])
    # Rows with $$CHAR1, $$CHAR2, $$CHAR3
    for char_index, char_num in enumerate(char_nums):
        char_index += 1  # Start from dark gray row
        latex_code += "& {\\footnotesize{}" + f" $$CHAR{char_num} " + "}"
        if char_index % 2:
            latex_code += " \\cellcolor{Dark-Gray-Table} "
        else:
            latex_code += " \\cellcolor{Light-Gray-Table} "

        latex_code += " & "

        for i in range(num_columns - 1):
            if char_index % 2:
                latex_code += " \\cellcolor{Dark-Gray-Table} "
            else:
                latex_code += " \\cellcolor{Light-Gray-Table} "
            latex_code += " & "

        if (
            "$CHAR" + str(char_num),
            "$" + name.replace("REP", ""),
        ) in final_locs.items():
            if victim == "$CHAR" + str(char_num):
                latex_code += " \\D "
            else:
                latex_code += " \\Y "
        else:
            latex_code += " \\N "

        if char_index % 2:
            latex_code += " \\cellcolor{Dark-Gray-Table} "
        else:
            latex_code += " \\cellcolor{Light-Gray-Table} "

        latex_code += " \\tabularnewline\n"

        if char_index < num_rows:
            # hhline stays visible above colortbl's shaded cells.
            latex_code += "\\hhline{~|" + "-|" * (num_columns + 1) + "}\n"

    # End the table
    latex_code += "\\hline\n\\end{tabular}\\\\\n"

    return latex_code


def generate_latex_weapons_table(number_weapons, column_width=None):
    # Dynamically set column format based on number_weapons
    page_width = None

    if column_width is not None:
        if not 0 < column_width <= 1:
            raise ValueError("weapon column width must be a fraction of paper width")
        page_width = column_width
    elif number_weapons == 5:
        page_width = 0.12
    else:
        page_width = 0.172

    column_format = "|".join(
        [">{\\centering}p{" + str(page_width) + "\\paperwidth}"] * number_weapons
    )
    latex_code = "\\renewcommand{\\arraystretch}{1.4}\n"
    latex_code += f"\\begin{{tabular}}{{|{column_format}|}}\n"

    # Add the first row
    latex_code += "\\hline\n"
    for i in range(number_weapons):
        latex_code += f"$$ROOM{i}WEAPONREP & "

    # Remove the last unnecessary "&" and add row end
    latex_code = latex_code[:-2] + " \\tabularnewline\n"

    # Finish the table
    latex_code += "\\hline\n\\end{tabular}\n"
    latex_code += "\\renewcommand{\\arraystretch}{1}\n"
    return latex_code

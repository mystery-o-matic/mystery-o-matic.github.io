"""Seasonal settings, fixed to a mystery's generation date."""


def get_seasonal_theme(mystery_date):
    """Halloween runs from October 29 through October 31, inclusive, each year."""
    if mystery_date.month == 10 and 29 <= mystery_date.day <= 31:
        return "halloween"
    return ""


# Replace only the bold setting description; keep the sentence's time/place
# context. These are atmosphere, never room names, activities or clues.
HALLOWEEN_SETTINGS = {
    "mansion": {
        "en": "the spooky mansion where everything started",
        "es": "la inquietante mansión donde todo comenzó",
        "ru": "зловещем особняке, где всё началось",
    },
    "ship": {
        "en": "an eerie pirate ship",
        "es": "un siniestro barco pirata",
        "ru": "зловещий пиратский корабль",
    },
    "egypt": {
        "en": "an ominous pyramid in Ancient Egypt",
        "es": "una siniestra pirámide en el Antiguo Egipto",
        "ru": "зловещую пирамиду Древнего Египта",
    },
    "island": {
        "en": "an eerie, deserted tropical island",
        "es": "una inquietante isla tropical desierta",
        "ru": "жуткий необитаемый тропический остров",
    },
    "castle": {
        "en": "a spooky castle in the Middle Ages",
        "es": "un siniestro castillo en la Edad Media",
        "ru": "зловещий замок Средневековья",
    },
    "museum": {
        "en": "an eerily empty museum",
        "es": "un museo inquietantemente vacío",
        "ru": "жуткий пустой музей ночью",
    },
    "train": {
        "en": "the spooky Orient Express",
        "es": "inquietante Orient Express",
        "ru": "зловещий Восточный экспресс",
    },
    "space station": {
        "en": "an eerie, high-tech space station",
        "es": "una inquietante estación espacial de alta tecnología",
        "ru": "жуткую высокотехнологичную космическую станцию",
    },
    "zoo": {
        "en": "a spooky, abandoned zoo",
        "es": "un siniestro zoológico abandonado",
        "ru": "жуткий заброшенный зоопарк",
    },
    "hospital": {
        "en": "an eerily deserted hospital",
        "es": "un hospital inquietantemente desierto",
        "ru": "жуткую пустую больницу",
    },
    "sport club": {
        "en": "an eerily empty sport club",
        "es": "un club deportivo inquietantemente desierto",
        "ru": "жуткий пустой спортивный клуб",
    },
    "abandoned school": {
        "en": "a spooky, abandoned school",
        "es": "una siniestra escuela abandonada",
        "ru": "жуткую заброшенную школу",
    },
    "arctic base": {
        "en": "an eerie, abandoned arctic military base",
        "es": "una siniestra base militar ártica abandonada",
        "ru": "зловещей заброшенной арктической военной базе",
    },
}

HALLOWEEN_LABELS = {
    "en": "Halloween Special",
    "es": "Especial de Halloween",
    "ru": "Спецвыпуск на Хэллоуин",
}

def get_location_intro(locations, language, theme):
    intro = locations.intro[language]
    if theme != "halloween":
        return intro
    setting = HALLOWEEN_SETTINGS.get(locations.name, {}).get(language)
    before, opening, remainder = intro.partition("<b>")
    _, closing, after = remainder.partition("</b>")
    if setting is None or not opening or not closing:
        return intro
    return before + opening + setting + closing + after

from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are back into <b>the mansion where everything started</b>!"
    intro["es"] = " han vuelto a <b>la mansión donde todo comenzó</b>!"
    intro["ru"] = " снова в <b>особняке, где всё началось</b>!"

    labels = {}
    labels["en"] = {
        "KITCHEN": "kitchen",
        "DINING": "dining room",
        "BEDROOM": "bedroom",
        "BATHROOM": "bathroom",
        "GARDEN": "garden",
    }
    labels["es"] = {
        "KITCHEN": "la cocina",
        "DINING": "el comedor",
        "BEDROOM": "el dormitorio",
        "BATHROOM": "el baño",
        "GARDEN": "el jardín",
    }
    labels["ru"] = {
        "KITCHEN": "кухня",
        "DINING": "столовая",
        "BEDROOM": "спальня",
        "BATHROOM": "ванная",
        "GARDEN": "сад",
    }
    labels["ru_loc"] = {
        "KITCHEN": "кухне",
        "DINING": "столовой",
        "BEDROOM": "спальне",
        "BATHROOM": "ванной",
        "GARDEN": "саду",
    }
    labels["ru_gen"] = {
        "KITCHEN": "кухни",
        "DINING": "столовой",
        "BEDROOM": "спальни",
        "BATHROOM": "ванной",
        "GARDEN": "сада",
    }

    representations = {
        "KITCHEN": "🍲",
        "DINING": "🪑",
        "BEDROOM": "🛏️",
        "BATHROOM": "🚽",
        "GARDEN": "🌳",
    }

    activities = make_ambient_activities(labels, representations)

    # Activities that another character could reasonably walk in on — no
    # toileting, no showering, no changing clothes, nothing that would make
    # the actor want privacy. Keeps puzzles internally consistent: anyone
    # else passing through the room at the same time doesn't strain belief.
    stay_activities = {
        "KITCHEN": [
            {"en": "to make a sandwich",       "es": "a preparar un sándwich",     "ru": "приготовить сэндвич"},
            {"en": "to brew some coffee",      "es": "a preparar café",            "ru": "сварить кофе"},
            {"en": "to wash the dishes",       "es": "a lavar los platos",         "ru": "помыть посуду"},
            {"en": "to grab a quick snack",    "es": "a buscar un bocadillo",      "ru": "перекусить"},
        ],
        "BATHROOM": [
            {"en": "to brush my teeth",        "es": "a cepillarme los dientes",   "ru": "почистить зубы"},
            {"en": "to wash my hands",         "es": "a lavarme las manos",        "ru": "помыть руки"},
            {"en": "to wash my face",          "es": "a lavarme la cara",          "ru": "умыться"},
            {"en": "to refill the soap",       "es": "a rellenar el jabón",        "ru": "наполнить мыльницу"},
        ],
        "BEDROOM": [
            {"en": "to fold some clothes",     "es": "a doblar ropa",              "ru": "сложить одежду"},
            {"en": "to make the bed",          "es": "a hacer la cama",            "ru": "застелить кровать"},
            {"en": "to look for a book",       "es": "a buscar un libro",          "ru": "найти книгу"},
            {"en": "to open the curtains",     "es": "a abrir las cortinas",       "ru": "раздвинуть шторы"},
        ],
        "DINING": [
            {"en": "to set the table",         "es": "a poner la mesa",            "ru": "накрыть на стол"},
            {"en": "to clear the table",       "es": "a recoger la mesa",          "ru": "убрать со стола"},
            {"en": "to grab a glass of water", "es": "a buscar un vaso de agua",   "ru": "взять стакан воды"},
            {"en": "to wipe down the table",   "es": "a limpiar la mesa",          "ru": "протереть стол"},
            {"en": "to light the candles",     "es": "a encender las velas",       "ru": "зажечь свечи"},
        ],
        "GARDEN": [
            {"en": "to water the plants",      "es": "a regar las plantas",        "ru": "полить растения"},
            {"en": "to pull some weeds",       "es": "a arrancar malas hierbas",   "ru": "выдернуть сорняки"},
            {"en": "to prune the bushes",      "es": "a podar los arbustos",       "ru": "подстричь кусты"},
            {"en": "to pick some flowers",     "es": "a recoger flores",           "ru": "сорвать цветы"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

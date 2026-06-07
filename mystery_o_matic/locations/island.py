from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported to <b>a deserted tropical island</b>!"
    intro["es"] = " han sido transportados a <b>una isla tropical desierta</b>!"
    intro["ru"] = " перенеслись на <b>необитаемый тропический остров</b>!"

    labels = {}
    labels["en"] = {
        "BEACH": "beach",
        "JUNGLE": "jungle",
        "CAVE": "cave",
        "CLIFF": "cliff",
        "VOLCANO": "volcano",
    }
    labels["es"] = {
        "BEACH": "la playa",
        "JUNGLE": "la jungla",
        "CAVE": "la cueva",
        "CLIFF": "el acantilado",
        "VOLCANO": "el volcán",
    }
    labels["ru"] = {
        "BEACH": "пляж",
        "JUNGLE": "джунгли",
        "CAVE": "пещера",
        "CLIFF": "утёс",
        "VOLCANO": "вулкан",
    }
    labels["ru_loc"] = {
        "BEACH": "пляже",
        "JUNGLE": "джунглях",
        "CAVE": "пещере",
        "CLIFF": "утёсе",
        "VOLCANO": "вулкане",
    }
    labels["ru_gen"] = {
        "BEACH": "пляжа",
        "JUNGLE": "джунглей",
        "CAVE": "пещеры",
        "CLIFF": "утёса",
        "VOLCANO": "вулкана",
    }

    representations = {
        "BEACH": "🏖️",
        "JUNGLE": "🌴",
        "CAVE": "🦇",
        "CLIFF": "⛰️",
        "VOLCANO": "🌋",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "BEACH": [
            {"en": "to collect seashells",           "es": "a recoger conchas marinas",                "ru": "пособирать ракушки"},
            {"en": "to gather driftwood",            "es": "a recoger madera de la playa",             "ru": "собрать плавник"},
            {"en": "to look out at the waves",       "es": "a mirar las olas",                         "ru": "посмотреть на волны"},
            {"en": "to fill a canteen",              "es": "a llenar una cantimplora",                 "ru": "наполнить флягу"},
        ],
        "JUNGLE": [
            {"en": "to chop some wood",              "es": "a cortar leña",                            "ru": "наколоть дров"},
            {"en": "to gather some fruit",           "es": "a recolectar fruta",                       "ru": "набрать фруктов"},
            {"en": "to set a snare",                 "es": "a poner una trampa",                       "ru": "поставить силок"},
            {"en": "to look for fresh water",        "es": "a buscar agua dulce",                      "ru": "поискать пресную воду"},
        ],
        "CAVE": [
            {"en": "to light a torch",               "es": "a encender una antorcha",                  "ru": "зажечь факел"},
            {"en": "to examine the cave drawings",   "es": "a examinar los dibujos rupestres",         "ru": "рассмотреть наскальные рисунки"},
            {"en": "to gather some bat guano",       "es": "a recoger guano de murciélago",            "ru": "собрать гуано"},
            {"en": "to scout for an exit",           "es": "a buscar una salida",                      "ru": "разведать выход"},
        ],
        "CLIFF": [
            {"en": "to scan the horizon",            "es": "a otear el horizonte",                     "ru": "осмотреть горизонт"},
            {"en": "to look for a ship",             "es": "a buscar un barco",                        "ru": "высмотреть корабль"},
            {"en": "to examine the rocks",           "es": "a examinar las rocas",                     "ru": "осмотреть скалы"},
            {"en": "to listen to the surf",          "es": "a escuchar el oleaje",                     "ru": "послушать прибой"},
        ],
        "VOLCANO": [
            {"en": "to inspect the summit",          "es": "a inspeccionar la cima",                   "ru": "осмотреть вершину"},
            {"en": "to take some rock samples",      "es": "a tomar muestras de roca",                 "ru": "взять образцы породы"},
            {"en": "to peer into the crater",        "es": "a asomarme al cráter",                     "ru": "заглянуть в кратер"},
            {"en": "to check the wind direction",    "es": "a comprobar la dirección del viento",      "ru": "проверить направление ветра"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

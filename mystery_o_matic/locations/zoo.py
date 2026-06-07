from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported into <b>an abandoned zoo</b>!"
    intro["es"] = " han sido transportados a <b>un zoológico abandonado</b>!"
    intro["ru"] = " перенеслись в <b>заброшенный зоопарк</b> ночью!"

    labels = {}
    labels["en"] = {
        "LION ENCLOSURE": "lion enclosure",
        "REPTILE HOUSE": "reptile house",
        "AVIARY": "aviary",
        "MONKEY ISLAND": "monkey island",
        "AQUARIUM": "aquarium",
    }
    labels["es"] = {
        "LION ENCLOSURE": "el recinto de leones",
        "REPTILE HOUSE": "la casa de reptiles",
        "AVIARY": "el aviario",
        "MONKEY ISLAND": "la isla de monos",
        "AQUARIUM": "el acuario",
    }
    labels["ru"] = {
        "LION ENCLOSURE": "вольер львов",
        "REPTILE HOUSE": "террариум",
        "AVIARY": "вольер птиц",
        "MONKEY ISLAND": "остров обезьян",
        "AQUARIUM": "аквариум",
    }
    labels["ru_loc"] = {
        "LION ENCLOSURE": "вольере львов",
        "REPTILE HOUSE": "террариуме",
        "AVIARY": "вольере птиц",
        "MONKEY ISLAND": "острове обезьян",
        "AQUARIUM": "аквариуме",
    }
    labels["ru_gen"] = {
        "LION ENCLOSURE": "вольера львов",
        "REPTILE HOUSE": "террариума",
        "AVIARY": "вольера птиц",
        "MONKEY ISLAND": "острова обезьян",
        "AQUARIUM": "аквариума",
    }

    representations = {
        "LION ENCLOSURE": "🦁",
        "REPTILE HOUSE": "🦎",
        "AVIARY": "🦜",
        "MONKEY ISLAND": "🐒",
        "AQUARIUM": "🐠",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "LION ENCLOSURE": [
            {"en": "to feed the lions",              "es": "a dar de comer a los leones",              "ru": "покормить львов"},
            {"en": "to refill the water trough",     "es": "a rellenar el abrevadero",                 "ru": "наполнить поилку"},
            {"en": "to rake out the bedding",        "es": "a rastrillar el lecho",                    "ru": "перетряхнуть подстилку"},
            {"en": "to check the gate latch",        "es": "a comprobar el cerrojo",                   "ru": "проверить засов"},
        ],
        "REPTILE HOUSE": [
            {"en": "to check the heat lamps",        "es": "a revisar las lámparas de calor",          "ru": "проверить тепловые лампы"},
            {"en": "to refill the water bowls",      "es": "a rellenar los cuencos de agua",           "ru": "наполнить миски водой"},
            {"en": "to feed the snakes",             "es": "a dar de comer a las serpientes",          "ru": "покормить змей"},
            {"en": "to clean a terrarium",           "es": "a limpiar un terrario",                    "ru": "почистить террариум"},
        ],
        "AVIARY": [
            {"en": "to refill the seed feeders",     "es": "a rellenar los comederos",                 "ru": "наполнить кормушки"},
            {"en": "to top up the bird bath",        "es": "a llenar la fuente de los pájaros",        "ru": "наполнить поилку"},
            {"en": "to clean the perches",           "es": "a limpiar las perchas",                    "ru": "почистить жёрдочки"},
            {"en": "to check the netting",           "es": "a revisar las redes",                      "ru": "проверить сетку"},
        ],
        "MONKEY ISLAND": [
            {"en": "to scatter some fruit",          "es": "a esparcir fruta",                         "ru": "разбросать фрукты"},
            {"en": "to check the swing ropes",       "es": "a revisar las cuerdas de los columpios",   "ru": "проверить канаты"},
            {"en": "to refill the water trough",     "es": "a rellenar el abrevadero",                 "ru": "наполнить поилку"},
            {"en": "to rake the playground",         "es": "a rastrillar el área de juego",            "ru": "разровнять площадку"},
        ],
        "AQUARIUM": [
            {"en": "to feed the fish",               "es": "a dar de comer a los peces",               "ru": "покормить рыб"},
            {"en": "to clean the tank glass",        "es": "a limpiar el cristal del acuario",         "ru": "помыть стекло"},
            {"en": "to check the filters",           "es": "a comprobar los filtros",                  "ru": "проверить фильтры"},
            {"en": "to top up the water",            "es": "a rellenar el agua",                       "ru": "долить воды"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

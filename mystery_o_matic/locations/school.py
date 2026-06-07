from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported into <b>an abandoned school</b>!"
    intro["es"] = " han sido transportados a <b>una escuela abandonada</b>!"
    intro["ru"] = " перенеслись в <b>заброшенную школу</b> ночью!"

    labels = {}
    labels["en"] = {
        "ART CLASSROOM": "art classroom",
        "SCIENCE LAB": "science lab",
        "GYM": "gym",
        "LIBRARY": "library",
        "CAFETERIA": "cafeteria",
    }
    labels["es"] = {
        "ART CLASSROOM": "el aula de arte",
        "SCIENCE LAB": "el laboratorio de ciencias",
        "GYM": "el gimnasio",
        "LIBRARY": "la biblioteca",
        "CAFETERIA": "la cafetería",
    }
    labels["ru"] = {
        "ART CLASSROOM": "класс рисования",
        "SCIENCE LAB": "лаборатория",
        "GYM": "спортзал",
        "LIBRARY": "библиотека",
        "CAFETERIA": "столовая",
    }
    labels["ru_loc"] = {
        "ART CLASSROOM": "классе рисования",
        "SCIENCE LAB": "лаборатории",
        "GYM": "спортзале",
        "LIBRARY": "библиотеке",
        "CAFETERIA": "столовой",
    }
    labels["ru_gen"] = {
        "ART CLASSROOM": "класса рисования",
        "SCIENCE LAB": "лаборатории",
        "GYM": "спортзала",
        "LIBRARY": "библиотеки",
        "CAFETERIA": "столовой",
    }

    representations = {
        "ART CLASSROOM": "🎨",
        "SCIENCE LAB": "🔬",
        "GYM": "💪",
        "LIBRARY": "📚",
        "CAFETERIA": "🍽️",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "ART CLASSROOM": [
            {"en": "to clean the brushes",           "es": "a limpiar los pinceles",                   "ru": "вымыть кисти"},
            {"en": "to set out the paints",          "es": "a preparar las pinturas",                  "ru": "разложить краски"},
            {"en": "to wash the easels",             "es": "a lavar los caballetes",                   "ru": "помыть мольберты"},
            {"en": "to tape up a new poster",        "es": "a colgar un cartel nuevo",                 "ru": "приклеить новый плакат"},
        ],
        "SCIENCE LAB": [
            {"en": "to calibrate the scales",        "es": "a calibrar las balanzas",                  "ru": "откалибровать весы"},
            {"en": "to label the test tubes",        "es": "a etiquetar los tubos de ensayo",          "ru": "подписать пробирки"},
            {"en": "to refill the beakers",          "es": "a rellenar los vasos de precipitados",     "ru": "наполнить мензурки"},
            {"en": "to wipe down the benches",       "es": "a limpiar las mesas",                      "ru": "протереть столы"},
        ],
        "GYM": [
            {"en": "to set up the cones",            "es": "a colocar los conos",                      "ru": "расставить конусы"},
            {"en": "to mop the floor",               "es": "a trapear el suelo",                       "ru": "помыть пол"},
            {"en": "to inflate a basketball",        "es": "a inflar un balón de baloncesto",          "ru": "накачать баскетбольный мяч"},
            {"en": "to rack the dumbbells",          "es": "a colocar las mancuernas",                 "ru": "расставить гантели"},
        ],
        "LIBRARY": [
            {"en": "to shelve some books",           "es": "a colocar algunos libros",                 "ru": "расставить книги"},
            {"en": "to look for a book",             "es": "a buscar un libro",                        "ru": "найти книгу"},
            {"en": "to dust the encyclopedias",      "es": "a quitar el polvo de las enciclopedias",   "ru": "вытереть пыль с энциклопедий"},
            {"en": "to update the catalog",          "es": "a actualizar el catálogo",                 "ru": "обновить каталог"},
        ],
        "CAFETERIA": [
            {"en": "to wipe down the trays",         "es": "a limpiar las bandejas",                   "ru": "протереть подносы"},
            {"en": "to refill the napkins",          "es": "a reponer las servilletas",                "ru": "пополнить салфетки"},
            {"en": "to set out the cups",            "es": "a colocar los vasos",                      "ru": "расставить стаканы"},
            {"en": "to grab a quick snack",          "es": "a buscar un bocadillo",                    "ru": "перекусить"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

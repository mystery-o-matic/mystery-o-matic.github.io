from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported into <b>an empty museum</b>!"
    intro["es"] = " han sido transportados a <b>un museo vacío</b>!"
    intro["ru"] = " перенеслись в <b>пустой музей ночью</b>!"

    labels = {}
    labels["en"] = {
        "DINOSAUR EXHIBIT": "dinosaur exhibit",
        "EGYPTIAN EXHIBIT": "egyptian exhibit",
        "MEDIEVAL EXHIBIT": "medieval exhibit",
        "SPACE EXHIBIT": "space exhibit",
        "OCEAN EXHIBIT": "ocean exhibit",
    }
    labels["es"] = {
        "DINOSAUR EXHIBIT": "la exhibición de dinosaurios",
        "EGYPTIAN EXHIBIT": "la exhibición egipcia",
        "MEDIEVAL EXHIBIT": "la exhibición medieval",
        "SPACE EXHIBIT": "la exhibición espacial",
        "OCEAN EXHIBIT": "la exhibición oceánica",
    }
    labels["ru"] = {
        "DINOSAUR EXHIBIT": "зал динозавров",
        "EGYPTIAN EXHIBIT": "египетский зал",
        "MEDIEVAL EXHIBIT": "средневековый зал",
        "SPACE EXHIBIT": "космический зал",
        "OCEAN EXHIBIT": "океанский зал",
    }
    labels["ru_loc"] = {
        "DINOSAUR EXHIBIT": "зале динозавров",
        "EGYPTIAN EXHIBIT": "египетском зале",
        "MEDIEVAL EXHIBIT": "средневековом зале",
        "SPACE EXHIBIT": "космическом зале",
        "OCEAN EXHIBIT": "океанском зале",
    }
    labels["ru_gen"] = {
        "DINOSAUR EXHIBIT": "зала динозавров",
        "EGYPTIAN EXHIBIT": "египетского зала",
        "MEDIEVAL EXHIBIT": "средневекового зала",
        "SPACE EXHIBIT": "космического зала",
        "OCEAN EXHIBIT": "океанского зала",
    }

    representations = {
        "DINOSAUR EXHIBIT": "🦖",
        "EGYPTIAN EXHIBIT": "⚱️",
        "MEDIEVAL EXHIBIT": "🛡️",
        "SPACE EXHIBIT": "🪐",
        "OCEAN EXHIBIT": "🐠",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "DINOSAUR EXHIBIT": [
            {"en": "to dust the fossils",            "es": "a quitar el polvo de los fósiles",         "ru": "вытереть пыль с окаменелостей"},
            {"en": "to read the placards",           "es": "a leer los carteles",                      "ru": "прочитать таблички"},
            {"en": "to polish the display case",     "es": "a pulir la vitrina",                       "ru": "отполировать витрину"},
            {"en": "to take a few photos",           "es": "a sacar algunas fotos",                    "ru": "сделать несколько фотографий"},
        ],
        "EGYPTIAN EXHIBIT": [
            {"en": "to dust the sarcophagi",         "es": "a quitar el polvo de los sarcófagos",      "ru": "вытереть пыль с саркофагов"},
            {"en": "to read the hieroglyph translations","es": "a leer las traducciones de los jeroglíficos","ru": "прочитать перевод иероглифов"},
            {"en": "to polish the display case",     "es": "a pulir la vitrina",                       "ru": "отполировать витрину"},
            {"en": "to take a few photos",           "es": "a sacar algunas fotos",                    "ru": "сделать несколько фотографий"},
        ],
        "MEDIEVAL EXHIBIT": [
            {"en": "to polish a suit of armor",      "es": "a pulir una armadura",                     "ru": "отполировать доспехи"},
            {"en": "to dust the swords",             "es": "a quitar el polvo de las espadas",         "ru": "вытереть пыль с мечей"},
            {"en": "to read the placards",           "es": "a leer los carteles",                      "ru": "прочитать таблички"},
            {"en": "to take a few photos",           "es": "a sacar algunas fotos",                    "ru": "сделать несколько фотографий"},
        ],
        "SPACE EXHIBIT": [
            {"en": "to polish the meteorite",        "es": "a pulir el meteorito",                     "ru": "отполировать метеорит"},
            {"en": "to dust the telescope lens",     "es": "a limpiar la lente del telescopio",        "ru": "протереть линзу телескопа"},
            {"en": "to read the placards",           "es": "a leer los carteles",                      "ru": "прочитать таблички"},
            {"en": "to take a few photos",           "es": "a sacar algunas fotos",                    "ru": "сделать несколько фотографий"},
        ],
        "OCEAN EXHIBIT": [
            {"en": "to clean the tank glass",        "es": "a limpiar el cristal del tanque",          "ru": "помыть стекло аквариума"},
            {"en": "to feed the fish",               "es": "a dar de comer a los peces",               "ru": "покормить рыб"},
            {"en": "to read the placards",           "es": "a leer los carteles",                      "ru": "прочитать таблички"},
            {"en": "to take a few photos",           "es": "a sacar algunas fotos",                    "ru": "сделать несколько фотографий"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported back in time to <b>a castle in the Middle Ages</b>!"
    intro["es"] = " han sido transportados en el tiempo a <b>un castillo en la Edad Media</b>!"
    intro["ru"] = " перенеслись в прошлое в <b>замок Средневековья</b>!"

    labels = {}
    labels["en"] = {
        "GREAT HALL": "great hall",
        "BED CHAMBER": "bed chamber",
        "DUNGEON": "dungeon",
        "ARMORY": "armory",
        "GARDEN": "garden",
    }
    labels["es"] = {
        "GREAT HALL": "el gran salón",
        "BED CHAMBER": "el dormitorio principal",
        "DUNGEON": "la mazmorra",
        "ARMORY": "la armería",
        "GARDEN": "el jardín",
    }
    labels["ru"] = {
        "GREAT HALL": "большой зал",
        "BED CHAMBER": "опочивальня",
        "DUNGEON": "темница",
        "ARMORY": "оружейная",
        "GARDEN": "сад",
    }
    labels["ru_loc"] = {
        "GREAT HALL": "большом зале",
        "BED CHAMBER": "опочивальне",
        "DUNGEON": "темнице",
        "ARMORY": "оружейной",
        "GARDEN": "саду",
    }
    labels["ru_gen"] = {
        "GREAT HALL": "большого зала",
        "BED CHAMBER": "опочивальни",
        "DUNGEON": "темницы",
        "ARMORY": "оружейной",
        "GARDEN": "сада",
    }

    representations = {
        "GREAT HALL": "🍷",
        "BED CHAMBER": "🛏️",
        "DUNGEON": "🔒",
        "ARMORY": "🛡️",
        "GARDEN": "🌳",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "GREAT HALL": [
            {"en": "to light the chandeliers",       "es": "a encender los candelabros",               "ru": "зажечь канделябры"},
            {"en": "to polish the goblets",          "es": "a pulir las copas",                        "ru": "начистить кубки"},
            {"en": "to arrange the chairs",          "es": "a acomodar las sillas",                    "ru": "расставить стулья"},
            {"en": "to dust the banners",            "es": "a quitar el polvo de los estandartes",     "ru": "вытереть пыль со знамён"},
        ],
        "BED CHAMBER": [
            {"en": "to fold the linens",             "es": "a doblar las sábanas",                     "ru": "сложить простыни"},
            {"en": "to open the shutters",           "es": "a abrir los postigos",                     "ru": "открыть ставни"},
            {"en": "to light a candle",              "es": "a encender una vela",                      "ru": "зажечь свечу"},
        ],
        "DUNGEON": [
            {"en": "to light the torches",           "es": "a encender las antorchas",                 "ru": "зажечь факелы"},
            {"en": "to oil the locks",               "es": "a engrasar las cerraduras",                "ru": "смазать замки"},
            {"en": "to check the cell doors",        "es": "a revisar las puertas de las celdas",      "ru": "проверить двери камер"},
        ],
        "ARMORY": [
            {"en": "to sharpen a sword",             "es": "a afilar una espada",                      "ru": "наточить меч"},
            {"en": "to polish a shield",             "es": "a pulir un escudo",                        "ru": "отполировать щит"},
            {"en": "to count the arrows",            "es": "a contar las flechas",                     "ru": "пересчитать стрелы"},
            {"en": "to oil the chainmail",           "es": "a engrasar la cota de malla",              "ru": "смазать кольчугу"},
        ],
        "GARDEN": [
            {"en": "to water the plants",            "es": "a regar las plantas",                      "ru": "полить растения"},
            {"en": "to pull some weeds",             "es": "a arrancar malas hierbas",                 "ru": "выдернуть сорняки"},
            {"en": "to prune the bushes",            "es": "a podar los arbustos",                     "ru": "подстричь кусты"},
            {"en": "to pick some flowers",           "es": "a recoger flores",                         "ru": "сорвать цветы"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

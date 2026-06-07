from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported back in time to <b>the famous Orient Express</b> during its last voyage!"
    intro["es"] = " han sido transportados en el tiempo al <b>famoso Orient Express</b> durante su último viaje!"
    intro["ru"] = " перенеслись в прошлое на <b>знаменитый Восточный экспресс</b> во время его последнего рейса!"

    labels = {}
    labels["en"] = {
        "LOCOMOTIVE": "locomotive",
        "LUGGAGE": "luggage carriage",
        "DINING": "dining carriage",
        "SLEEPING": "sleeping carriage",
        "LOUNGE": "lounge carriage",
    }
    labels["es"] = {
        "LOCOMOTIVE": "la locomotora",
        "LUGGAGE": "el vagón de equipaje",
        "DINING": "el vagón comedor",
        "SLEEPING": "el vagón dormitorio",
        "LOUNGE": "el vagón salón",
    }
    labels["ru"] = {
        "LOCOMOTIVE": "локомотив",
        "LUGGAGE": "багажный вагон",
        "DINING": "вагон-ресторан",
        "SLEEPING": "спальный вагон",
        "LOUNGE": "салон-вагон",
    }
    labels["ru_loc"] = {
        "LOCOMOTIVE": "локомотиве",
        "LUGGAGE": "багажном вагоне",
        "DINING": "вагоне-ресторане",
        "SLEEPING": "спальном вагоне",
        "LOUNGE": "салоне-вагоне",
    }
    labels["ru_gen"] = {
        "LOCOMOTIVE": "локомотива",
        "LUGGAGE": "багажного вагона",
        "DINING": "вагона-ресторана",
        "SLEEPING": "спального вагона",
        "LOUNGE": "салона-вагона",
    }

    representations = {
        "LOCOMOTIVE": "🚂",
        "LUGGAGE": "🧳",
        "DINING": "🍽️",
        "SLEEPING": "🛌",
        "LOUNGE": "🪑",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "LOCOMOTIVE": [
            {"en": "to shovel some coal",            "es": "a echar carbón al horno",                  "ru": "подбросить угля"},
            {"en": "to check the gauges",            "es": "a revisar los manómetros",                 "ru": "проверить манометры"},
            {"en": "to oil the pistons",             "es": "a engrasar los pistones",                  "ru": "смазать поршни"},
            {"en": "to refill the water tank",       "es": "a llenar el depósito de agua",             "ru": "наполнить бак"},
        ],
        "LUGGAGE": [
            {"en": "to stack a few trunks",          "es": "a apilar unos baúles",                     "ru": "сложить чемоданы"},
            {"en": "to label some crates",           "es": "a etiquetar las cajas",                    "ru": "подписать ящики"},
            {"en": "to check the manifest",          "es": "a revisar el manifiesto",                  "ru": "сверить опись"},
            {"en": "to look for my suitcase",        "es": "a buscar mi maleta",                       "ru": "найти свой чемодан"},
        ],
        "DINING": [
            {"en": "to pour the wine",               "es": "a servir el vino",                         "ru": "разлить вино"},
            {"en": "to set the silverware",          "es": "a poner los cubiertos",                    "ru": "разложить столовое серебро"},
            {"en": "to light the candles",           "es": "a encender las velas",                     "ru": "зажечь свечи"},
            {"en": "to polish the glasses",          "es": "a pulir las copas",                        "ru": "натереть бокалы"},
        ],
        "SLEEPING": [
            {"en": "to fold the linens",             "es": "a doblar las sábanas",                     "ru": "сложить простыни"},
            {"en": "to plump the pillows",           "es": "a ahuecar las almohadas",                  "ru": "взбить подушки"},
            {"en": "to restock the towels",          "es": "a reponer las toallas",                    "ru": "пополнить запас полотенец"},
            {"en": "to draw the curtains",           "es": "a correr las cortinas",                    "ru": "задёрнуть шторы"},
        ],
        "LOUNGE": [
            {"en": "to pour a drink",                "es": "a servir un trago",                        "ru": "налить выпить"},
            {"en": "to tidy the magazines",          "es": "a ordenar las revistas",                   "ru": "разложить журналы"},
            {"en": "to fluff the cushions",          "es": "a ahuecar los cojines",                    "ru": "взбить подушки"},
            {"en": "to wipe down the bar",           "es": "a limpiar la barra",                       "ru": "протереть барную стойку"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

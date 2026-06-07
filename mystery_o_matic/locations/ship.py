from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported back in time to <b>a pirate ship</b>!"
    intro["es"] = " han sido transportados en el tiempo a <b>un barco pirata</b>!"
    intro["ru"] = " перенеслись в прошлое на <b>пиратский корабль</b>!"

    labels = {}
    labels["en"] = {
        "GALLEY": "galley",
        "NAVIGATION ROOM": "navigation room",
        "CAPTAIN CABIN": "captain cabin",
        "MAIN DECK": "main deck",
        "CARGO HOLD": "cargo hold",
    }
    labels["es"] = {
        "GALLEY": "la cocina",
        "NAVIGATION ROOM": "la sala de navegación",
        "CAPTAIN CABIN": "la cabina del capitán",
        "MAIN DECK": "la cubierta principal",
        "CARGO HOLD": "la bodega de carga",
    }
    labels["ru"] = {
        "GALLEY": "камбуз",
        "NAVIGATION ROOM": "штурманская рубка",
        "CAPTAIN CABIN": "капитанская каюта",
        "MAIN DECK": "главная палуба",
        "CARGO HOLD": "грузовой трюм",
    }
    labels["ru_loc"] = {
        "GALLEY": "камбузе",
        "NAVIGATION ROOM": "штурманской рубке",
        "CAPTAIN CABIN": "капитанской каюте",
        "MAIN DECK": "главной палубе",
        "CARGO HOLD": "грузовом трюме",
    }
    labels["ru_gen"] = {
        "GALLEY": "камбуза",
        "NAVIGATION ROOM": "штурманской рубки",
        "CAPTAIN CABIN": "капитанской каюты",
        "MAIN DECK": "главной палубы",
        "CARGO HOLD": "грузового трюма",
    }

    representations = {
        "GALLEY": "🍲",
        "NAVIGATION ROOM": "🧭",
        "CAPTAIN CABIN": "🛏️",
        "MAIN DECK": "⚓",
        "CARGO HOLD": "📦",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "GALLEY": [
            {"en": "to brew some grog",              "es": "a preparar un poco de grog",               "ru": "сварить грог"},
            {"en": "to wash the dishes",             "es": "a lavar los platos",                       "ru": "помыть посуду"},
            {"en": "to grab a quick bite",           "es": "a buscar algo de comer",                   "ru": "перекусить"},
            {"en": "to restock the salt cod",        "es": "a reponer el bacalao salado",              "ru": "пополнить запас солёной трески"},
        ],
        "NAVIGATION ROOM": [
            {"en": "to study a chart",               "es": "a estudiar un mapa",                       "ru": "изучить карту"},
            {"en": "to wind the chronometer",        "es": "a darle cuerda al cronómetro",             "ru": "завести хронометр"},
            {"en": "to log the latest sighting",     "es": "a anotar el último avistamiento",          "ru": "записать последнее наблюдение"},
        ],
        "MAIN DECK": [
            {"en": "to swab the deck",               "es": "a fregar la cubierta",                     "ru": "вымыть палубу"},
            {"en": "to adjust the sails",            "es": "a ajustar las velas",                      "ru": "поправить паруса"},
            {"en": "to coil a rope",                 "es": "a enrollar un cabo",                       "ru": "смотать канат"},
            {"en": "to check the rigging",           "es": "a revisar el aparejo",                     "ru": "проверить такелаж"},
        ],
        "CAPTAIN CABIN": [
            {"en": "to update the ship's log",       "es": "a actualizar el diario de a bordo",        "ru": "заполнить судовой журнал"},
            {"en": "to polish the captain's compass","es": "a pulir el compás del capitán",            "ru": "начистить капитанский компас"},
            {"en": "to fetch a spyglass",            "es": "a buscar un catalejo",                     "ru": "взять подзорную трубу"},
            {"en": "to dust the desk",               "es": "a quitar el polvo del escritorio",         "ru": "вытереть пыль со стола"},
        ],
        "CARGO HOLD": [
            {"en": "to lash down the crates",        "es": "a amarrar las cajas",                      "ru": "закрепить ящики"},
            {"en": "to check the manifest",          "es": "a revisar el inventario",                  "ru": "сверить опись груза"},
            {"en": "to look for my chest",           "es": "a buscar mi baúl",                         "ru": "найти свой сундук"},
            {"en": "to count the barrels",           "es": "a contar los barriles",                    "ru": "пересчитать бочки"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

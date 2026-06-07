from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are stranded in <b>an abandoned arctic military base</b> during a blizzard!"
    intro["es"] = " han quedado atrapados en <b>una base militar ártica abandonada</b> durante una tormenta de nieve!"
    intro["ru"] = " оказались в <b>заброшенной арктической военной базе</b> во время метели!"

    labels = {}
    labels["en"] = {
        "COMMAND CENTER": "command center",
        "ARMORY": "armory",
        "BARRACKS": "barracks",
        "RADIO ROOM": "radio room",
        "MESS HALL": "mess hall",
    }
    labels["es"] = {
        "COMMAND CENTER": "el centro de mando",
        "ARMORY": "la armería",
        "BARRACKS": "los barracones",
        "RADIO ROOM": "la sala de radio",
        "MESS HALL": "el comedor",
    }
    labels["ru"] = {
        "COMMAND CENTER": "командный центр",
        "ARMORY": "оружейная",
        "BARRACKS": "казарма",
        "RADIO ROOM": "радиорубка",
        "MESS HALL": "столовая",
    }
    labels["ru_loc"] = {
        "COMMAND CENTER": "командном центре",
        "ARMORY": "оружейной",
        "BARRACKS": "казарме",
        "RADIO ROOM": "радиорубке",
        "MESS HALL": "столовой",
    }
    labels["ru_gen"] = {
        "COMMAND CENTER": "командного центра",
        "ARMORY": "оружейной",
        "BARRACKS": "казармы",
        "RADIO ROOM": "радиорубки",
        "MESS HALL": "столовой",
    }

    representations = {
        "COMMAND CENTER": "🖥️",
        "ARMORY": "🔒",
        "BARRACKS": "🛏️",
        "RADIO ROOM": "📡",
        "MESS HALL": "🍽️",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "COMMAND CENTER": [
            {"en": "to check the monitors",          "es": "a revisar los monitores",                  "ru": "проверить мониторы"},
            {"en": "to log the latest readings",     "es": "a registrar las últimas lecturas",         "ru": "записать последние показания"},
            {"en": "to review the weather charts",   "es": "a revisar los partes meteorológicos",      "ru": "просмотреть карты погоды"},
            {"en": "to print out a report",          "es": "a imprimir un informe",                    "ru": "распечатать отчёт"},
        ],
        "ARMORY": [
            {"en": "to clean a rifle",               "es": "a limpiar un rifle",                       "ru": "почистить винтовку"},
            {"en": "to inventory the equipment",     "es": "a hacer inventario del equipo",            "ru": "провести инвентаризацию"},
            {"en": "to oil a holster",               "es": "a engrasar una funda",                     "ru": "смазать кобуру"},
            {"en": "to count the rounds",            "es": "a contar los cartuchos",                   "ru": "пересчитать патроны"},
        ],
        "BARRACKS": [
            {"en": "to make my bunk",                "es": "a hacer mi litera",                        "ru": "застелить койку"},
            {"en": "to fold my uniform",             "es": "a doblar mi uniforme",                     "ru": "сложить форму"},
            {"en": "to polish my boots",             "es": "a lustrar mis botas",                      "ru": "начистить ботинки"},
            {"en": "to sort the mail",               "es": "a clasificar el correo",                   "ru": "разобрать почту"},
        ],
        "RADIO ROOM": [
            {"en": "to tune the radio",              "es": "a sintonizar la radio",                    "ru": "настроить радио"},
            {"en": "to send a status check",         "es": "a enviar un parte de situación",           "ru": "отправить отчёт о состоянии"},
            {"en": "to log an incoming call",        "es": "a registrar una llamada entrante",         "ru": "записать входящий вызов"},
            {"en": "to swap a fuse",                 "es": "a cambiar un fusible",                     "ru": "заменить предохранитель"},
        ],
        "MESS HALL": [
            {"en": "to brew a pot of coffee",        "es": "a preparar una jarra de café",             "ru": "заварить кофе"},
            {"en": "to wipe down the trays",         "es": "a limpiar las bandejas",                   "ru": "протереть подносы"},
            {"en": "to restock the pantry",          "es": "a reponer la despensa",                    "ru": "пополнить кладовую"},
            {"en": "to grab a quick meal",           "es": "a comer algo rápido",                      "ru": "перекусить"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

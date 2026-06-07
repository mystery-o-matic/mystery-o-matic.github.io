from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported into the future to <b>a high-tech space station</b> orbiting an unknown planet!"
    intro["es"] = " han sido transportados al futuro a <b>una estación espacial de alta tecnología</b> orbitando un planeta desconocido!"
    intro["ru"] = " перенеслись в будущее на <b>высокотехнологичную космическую станцию</b>, вращающуюся вокруг неизвестной планеты!"

    labels = {}
    labels["en"] = {
        "COMMAND": "command module",
        "LAB": "lab module",
        "AIRLOCK": "airlock module",
        "SLEEPING": "sleeping module",
        "GARDEN": "garden module",
    }
    labels["es"] = {
        "COMMAND": "el módulo de comando",
        "LAB": "el módulo de laboratorio",
        "AIRLOCK": "el módulo de esclusa",
        "SLEEPING": "el módulo de descanso",
        "GARDEN": "el módulo de jardín",
    }
    labels["ru"] = {
        "COMMAND": "командный модуль",
        "LAB": "лабораторный модуль",
        "AIRLOCK": "шлюзовой модуль",
        "SLEEPING": "жилой модуль",
        "GARDEN": "садовый модуль",
    }
    labels["ru_loc"] = {
        "COMMAND": "командном модуле",
        "LAB": "лабораторном модуле",
        "AIRLOCK": "шлюзовом модуле",
        "SLEEPING": "жилом модуле",
        "GARDEN": "садовом модуле",
    }
    labels["ru_gen"] = {
        "COMMAND": "командного модуля",
        "LAB": "лабораторного модуля",
        "AIRLOCK": "шлюзового модуля",
        "SLEEPING": "жилого модуля",
        "GARDEN": "садового модуля",
    }

    representations = {
        "COMMAND": "🕹️",
        "LAB": "🔬",
        "AIRLOCK": "🔒",
        "SLEEPING": "🛌",
        "GARDEN": "🥔",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "COMMAND": [
            {"en": "to check the telemetry",         "es": "a revisar la telemetría",                  "ru": "проверить телеметрию"},
            {"en": "to adjust the orbit",            "es": "a ajustar la órbita",                      "ru": "скорректировать орбиту"},
            {"en": "to update the heading",          "es": "a actualizar el rumbo",                    "ru": "обновить курс"},
            {"en": "to log the readings",            "es": "a registrar las lecturas",                 "ru": "записать показания"},
        ],
        "LAB": [
            {"en": "to calibrate the centrifuge",    "es": "a calibrar la centrífuga",                 "ru": "откалибровать центрифугу"},
            {"en": "to label some samples",          "es": "a etiquetar las muestras",                 "ru": "подписать образцы"},
            {"en": "to mix some reagents",           "es": "a mezclar reactivos",                      "ru": "смешать реактивы"},
            {"en": "to log the results",             "es": "a registrar los resultados",               "ru": "записать результаты"},
        ],
        "AIRLOCK": [
            {"en": "to inspect the seal",            "es": "a inspeccionar el sello",                  "ru": "проверить уплотнение"},
            {"en": "to log the cycle counter",       "es": "a anotar el contador de ciclos",           "ru": "записать счётчик циклов"},
            {"en": "to stow the suits",              "es": "a guardar los trajes",                     "ru": "убрать скафандры"},
            {"en": "to check the pressure gauge",    "es": "a comprobar el manómetro",                 "ru": "проверить манометр"},
        ],
        "SLEEPING": [
            {"en": "to secure the lockers",          "es": "a cerrar los casilleros",                  "ru": "закрыть шкафчики"},
            {"en": "to stow a sleeping bag",         "es": "a guardar un saco de dormir",              "ru": "убрать спальный мешок"},
            {"en": "to fold a harness",              "es": "a doblar un arnés",                        "ru": "сложить ремни"},
            {"en": "to grab a sweater",              "es": "a buscar un suéter",                       "ru": "взять кофту"},
        ],
        "GARDEN": [
            {"en": "to water the hydroponics",       "es": "a regar el hidropónico",                   "ru": "полить гидропонику"},
            {"en": "to harvest some potatoes",       "es": "a cosechar patatas",                       "ru": "собрать картофель"},
            {"en": "to check the grow lights",       "es": "a revisar las luces de cultivo",           "ru": "проверить фитолампы"},
            {"en": "to prune the vines",             "es": "a podar las enredaderas",                  "ru": "подрезать лозу"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

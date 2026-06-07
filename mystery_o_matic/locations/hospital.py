from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported into <b>a deserted hospital</b>!"
    intro["es"] = " han sido transportados a <b>un hospital desierto</b>!"
    intro["ru"] = " перенеслись в <b>пустую больницу</b> ночью!"

    labels = {}
    labels["en"] = {
        "ER": "emergency room",
        "ICU": "intensive care unit",
        "OPERATING THEATER": "operating theater",
        "PHARMACY": "pharmacy",
        "LOBBY": "lobby",
    }
    labels["es"] = {
        "ER": "la sala de urgencias",
        "ICU": "la unidad de cuidados intensivos",
        "OPERATING THEATER": "el quirófano",
        "PHARMACY": "la farmacia",
        "LOBBY": "el vestíbulo",
    }
    labels["ru"] = {
        "ER": "приёмное отделение",
        "ICU": "реанимация",
        "OPERATING THEATER": "операционная",
        "PHARMACY": "аптека",
        "LOBBY": "вестибюль",
    }
    labels["ru_loc"] = {
        "ER": "приёмном отделении",
        "ICU": "реанимации",
        "OPERATING THEATER": "операционной",
        "PHARMACY": "аптеке",
        "LOBBY": "вестибюле",
    }
    labels["ru_gen"] = {
        "ER": "приёмного отделения",
        "ICU": "реанимации",
        "OPERATING THEATER": "операционной",
        "PHARMACY": "аптеки",
        "LOBBY": "вестибюля",
    }

    representations = {
        "ER": "🚑",
        "ICU": "🛏️",
        "OPERATING THEATER": "🔪",
        "PHARMACY": "💊",
        "LOBBY": "💺",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "ER": [
            {"en": "to restock the bandages",        "es": "a reponer las vendas",                     "ru": "пополнить запас бинтов"},
            {"en": "to log the triage notes",        "es": "a anotar el triaje",                       "ru": "записать данные сортировки"},
            {"en": "to sterilize the trolley",       "es": "a esterilizar el carro",                   "ru": "простерилизовать тележку"},
            {"en": "to refill the saline drip",      "es": "a rellenar el suero",                      "ru": "пополнить капельницу"},
        ],
        "ICU": [
            {"en": "to check the monitors",          "es": "a revisar los monitores",                  "ru": "проверить мониторы"},
            {"en": "to log the vital signs",         "es": "a anotar los signos vitales",              "ru": "записать показания приборов"},
            {"en": "to dim the lights",              "es": "a atenuar las luces",                      "ru": "приглушить свет"},
            {"en": "to refill the IV bag",           "es": "a rellenar la bolsa intravenosa",          "ru": "заменить капельницу"},
        ],
        "OPERATING THEATER": [
            {"en": "to sterilize the instruments",   "es": "a esterilizar el instrumental",            "ru": "простерилизовать инструменты"},
            {"en": "to lay out the trays",           "es": "a preparar las bandejas",                  "ru": "разложить лотки"},
            {"en": "to restock the gowns",           "es": "a reponer las batas",                      "ru": "пополнить запас халатов"},
            {"en": "to adjust the surgical lamp",    "es": "a ajustar la lámpara quirúrgica",          "ru": "настроить операционную лампу"},
        ],
        "PHARMACY": [
            {"en": "to check the medicine shelves",  "es": "a revisar las estanterías de medicamentos","ru": "проверить полки с лекарствами"},
            {"en": "to log a dispensation",          "es": "a registrar una entrega",                  "ru": "зарегистрировать выдачу"},
            {"en": "to restock the antibiotics",     "es": "a reponer los antibióticos",               "ru": "пополнить запас антибиотиков"},
            {"en": "to count the tablets",           "es": "a contar las pastillas",                   "ru": "пересчитать таблетки"},
        ],
        "LOBBY": [
            {"en": "to tidy the magazines",          "es": "a ordenar las revistas",                   "ru": "разложить журналы"},
            {"en": "to refill the water cooler",     "es": "a rellenar el dispensador de agua",        "ru": "заправить кулер"},
            {"en": "to dust the chairs",             "es": "a quitar el polvo de las sillas",          "ru": "вытереть пыль со стульев"},
            {"en": "to update the noticeboard",      "es": "a actualizar el tablón de anuncios",       "ru": "обновить объявления"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported into <b>an empty sport club</b>!"
    intro["es"] = " han sido transportados a <b>un club deportivo desierto</b>!"
    intro["ru"] = " перенеслись в <b>пустой спортивный клуб</b> ночью!"

    labels = {}
    labels["en"] = {
        "GYM": "gym",
        "POOL": "swimming pool",
        "SAUNA": "sauna",
        "COURT": "sports court",
        "LOUNGE": "lounge",
    }
    labels["es"] = {
        "GYM": "el gimnasio",
        "POOL": "la piscina",
        "SAUNA": "la sauna",
        "COURT": "la cancha deportiva",
        "LOUNGE": "el salón",
    }
    labels["ru"] = {
        "GYM": "тренажёрный зал",
        "POOL": "бассейн",
        "SAUNA": "сауна",
        "COURT": "спортивная площадка",
        "LOUNGE": "зал отдыха",
    }
    labels["ru_loc"] = {
        "GYM": "тренажёрном зале",
        "POOL": "бассейне",
        "SAUNA": "сауне",
        "COURT": "спортивной площадке",
        "LOUNGE": "зале отдыха",
    }
    labels["ru_gen"] = {
        "GYM": "тренажёрного зала",
        "POOL": "бассейна",
        "SAUNA": "сауны",
        "COURT": "спортивной площадки",
        "LOUNGE": "зала отдыха",
    }

    representations = {
        "GYM": "💪",
        "POOL": "🏊",
        "SAUNA": "🧖",
        "COURT": "🏀",
        "LOUNGE": "🛋️",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "GYM": [
            {"en": "to rack the dumbbells",          "es": "a colocar las mancuernas",                 "ru": "расставить гантели"},
            {"en": "to wipe down the machines",      "es": "a limpiar las máquinas",                   "ru": "протереть тренажёры"},
            {"en": "to refill the water bottles",    "es": "a rellenar las botellas de agua",          "ru": "наполнить бутылки водой"},
            {"en": "to restock the towels",          "es": "a reponer las toallas",                    "ru": "пополнить запас полотенец"},
        ],
        "POOL": [
            {"en": "to skim the surface",            "es": "a quitar las hojas de la superficie",      "ru": "очистить поверхность от мусора"},
            {"en": "to check the chlorine level",    "es": "a comprobar el nivel de cloro",            "ru": "проверить уровень хлора"},
            {"en": "to fold the towels",             "es": "a doblar las toallas",                     "ru": "сложить полотенца"},
            {"en": "to adjust the lane ropes",       "es": "a ajustar las corcheras",                  "ru": "поправить разделительные канаты"},
        ],
        "SAUNA": [
            {"en": "to refill the water bucket",     "es": "a rellenar el cubo de agua",               "ru": "наполнить ведро водой"},
            {"en": "to lay out fresh towels",        "es": "a colocar toallas limpias",                "ru": "разложить свежие полотенца"},
            {"en": "to wipe down the benches",       "es": "a limpiar los bancos",                     "ru": "протереть скамьи"},
            {"en": "to sweep the floor",             "es": "a barrer el suelo",                        "ru": "подмести пол"},
        ],
        "COURT": [
            {"en": "to mop up a wet patch",          "es": "a secar una mancha de humedad",            "ru": "вытереть мокрое место"},
            {"en": "to set up the net",              "es": "a montar la red",                          "ru": "натянуть сетку"},
            {"en": "to inflate a basketball",        "es": "a inflar un balón de baloncesto",          "ru": "накачать мяч"},
            {"en": "to mark the lines",              "es": "a marcar las líneas",                      "ru": "разметить линии"},
        ],
        "LOUNGE": [
            {"en": "to tidy the magazines",          "es": "a ordenar las revistas",                   "ru": "разложить журналы"},
            {"en": "to refill the water cooler",     "es": "a rellenar el dispensador de agua",        "ru": "заправить кулер"},
            {"en": "to fluff the cushions",          "es": "a ahuecar los cojines",                    "ru": "взбить подушки"},
            {"en": "to dust the side tables",        "es": "a quitar el polvo de las mesitas",         "ru": "вытереть пыль со столиков"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

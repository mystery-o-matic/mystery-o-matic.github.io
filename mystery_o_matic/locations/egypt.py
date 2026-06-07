from mystery_o_matic.locations.helpers import make_ambient_activities

def get_data():
    intro = {}
    intro["en"] = " are transported back in time to <b>a pyramid in Ancient Egypt</b>!"
    intro["es"] = " han sido transportados en el tiempo a <b>una pirámide en el Antiguo Egipto</b>!"
    intro["ru"] = " перенеслись в прошлое в <b>пирамиду Древнего Египта</b>!"

    labels = {}
    labels["en"] = {
        "THRONE ROOM": "throne room",
        "BURIAL PLACE": "burial chamber",
        "TEMPLE": "temple",
        "DESERT": "desert",
        "GARDEN": "garden",
    }
    labels["es"] = {
        "THRONE ROOM": "el cuarto del trono",
        "BURIAL PLACE": "la cámara funeraria",
        "TEMPLE": "el templo",
        "DESERT": "el desierto",
        "GARDEN": "el jardín",
    }
    labels["ru"] = {
        "THRONE ROOM": "тронный зал",
        "BURIAL PLACE": "погребальная камера",
        "TEMPLE": "храм",
        "DESERT": "пустыня",
        "GARDEN": "сад",
    }
    labels["ru_loc"] = {
        "THRONE ROOM": "тронном зале",
        "BURIAL PLACE": "погребальной камере",
        "TEMPLE": "храме",
        "DESERT": "пустыне",
        "GARDEN": "саду",
    }
    labels["ru_gen"] = {
        "THRONE ROOM": "тронного зала",
        "BURIAL PLACE": "погребальной камеры",
        "TEMPLE": "храма",
        "DESERT": "пустыни",
        "GARDEN": "сада",
    }

    representations = {
        "THRONE ROOM": "👑",
        "BURIAL PLACE": "⚱️",
        "TEMPLE": "📿",
        "DESERT": "🏜️",
        "GARDEN": "🌳",
    }

    activities = make_ambient_activities(labels, representations)


    stay_activities = {
        "THRONE ROOM": [
            {"en": "to polish the throne",           "es": "a pulir el trono",                         "ru": "отполировать трон"},
            {"en": "to dust the regalia",            "es": "a quitar el polvo de las insignias",       "ru": "вытереть пыль с регалий"},
            {"en": "to light the braziers",          "es": "a encender los braseros",                  "ru": "зажечь жаровни"},
            {"en": "to arrange the cushions",        "es": "a acomodar los cojines",                   "ru": "поправить подушки"},
        ],
        "BURIAL PLACE": [
            {"en": "to light the incense",           "es": "a encender el incienso",                   "ru": "зажечь благовония"},
            {"en": "to place fresh offerings",       "es": "a colocar nuevas ofrendas",                "ru": "положить свежие подношения"},
            {"en": "to dust the sarcophagus",        "es": "a limpiar el polvo del sarcófago",         "ru": "вытереть пыль с саркофага"},
            {"en": "to sweep the floor",             "es": "a barrer el suelo",                        "ru": "подмести пол"},
        ],
        "TEMPLE": [
            {"en": "to light the candles",           "es": "a encender las velas",                     "ru": "зажечь свечи"},
            {"en": "to polish the altar",            "es": "a pulir el altar",                         "ru": "отполировать алтарь"},
            {"en": "to sweep the floor",             "es": "a barrer el suelo",                        "ru": "подмести пол"},
            {"en": "to refill the offering bowl",    "es": "a rellenar el cuenco de ofrendas",         "ru": "наполнить чашу подношений"},
        ],
        "DESERT": [
            {"en": "to refill the water skins",      "es": "a rellenar los odres de agua",             "ru": "наполнить бурдюки водой"},
            {"en": "to watch the dunes",             "es": "a mirar las dunas",                        "ru": "понаблюдать за дюнами"},
            {"en": "to shake sand from my sandals",  "es": "a sacudir la arena de mis sandalias",      "ru": "вытряхнуть песок из сандалий"},
            {"en": "to scan the horizon",            "es": "a otear el horizonte",                     "ru": "осмотреть горизонт"},
        ],
        "GARDEN": [
            {"en": "to water the plants",            "es": "a regar las plantas",                      "ru": "полить растения"},
            {"en": "to pull some weeds",             "es": "a arrancar malas hierbas",                 "ru": "выдернуть сорняки"},
            {"en": "to prune the bushes",            "es": "a podar los arbustos",                     "ru": "подстричь кусты"},
            {"en": "to pick some flowers",           "es": "a recoger flores",                         "ru": "сорвать цветы"},
        ],
    }

    return (intro, labels, representations, activities, stay_activities)

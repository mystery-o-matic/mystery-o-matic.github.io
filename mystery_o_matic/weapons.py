from random import shuffle, choice

classic_weapons = [
    {"$PISTOL": "🔫"},
    {"$KNIFE": "🔪", "$SCISSORS": "✂️", "$AXE": "🪓", "$SCREWDRIVER": "🪛"},
    {"$POISON": "⚗️"},
    {"$HAMMER": "🔨", "$WRENCH": "🔧", "$CANDLESTICK": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

weapon_labels = {}

weapon_labels["en"] = {
    "$PISTOL": "pistol",
    "$KNIFE": "knife",
    "$SCISSORS": "scissors",
    "$AXE": "axe",
    "$SCREWDRIVER": "screwdriver",
    "$POISON": "poison",
    "$HAMMER": "hammer",
    "$WRENCH": "wrench",
    "$CANDLESTICK": "candlestick",
    "$ROPE": "rope",
    "$CHAIN": "chain",
    "$ARCHERY_BOW": "archery bow",
    "$DAGGER": "dagger",
    "$TRIDENT": "trident",
    "$SWORD": "sword",
    "$ROCK": "rock",
    "$CURSE": "curse",
    "$WIRE_EXTENSION": "wire extension",
    "$SONIC_BLASTER": "sonic blaster",
}

weapon_labels["es"] = {
    "$PISTOL": "la pistola",
    "$KNIFE": "el cuchillo",
    "$SCISSORS": "las tijeras",
    "$AXE": "el hacha",
    "$SCREWDRIVER": "el destornillador",
    "$POISON": "el veneno",
    "$HAMMER": "el martillo",
    "$WRENCH": "la llave inglesa",
    "$CANDLESTICK": "el candelabro",
    "$ROPE": "la soga",
    "$CHAIN": "la cadena",
    "$ARCHERY_BOW": "el arco",
    "$DAGGER": "la daga",
    "$TRIDENT": "el tridente",
    "$SWORD": "la espada",
    "$ROCK": "la roca",
    "$CURSE": "la maldición",
    "$WIRE_EXTENSION": "el cable alargador",
    "$SONIC_BLASTER": "el arma sónica",
}

weapon_labels["ru"] = {
    "$PISTOL": "пистолет",
    "$KNIFE": "нож",
    "$SCISSORS": "ножницы",
    "$AXE": "топор",
    "$SCREWDRIVER": "отвёртка",
    "$POISON": "яд",
    "$HAMMER": "молоток",
    "$WRENCH": "гаечный ключ",
    "$CANDLESTICK": "канделябр",
    "$ROPE": "верёвка",
    "$CHAIN": "цепь",
    "$ARCHERY_BOW": "лук со стрелами",
    "$DAGGER": "кинжал",
    "$TRIDENT": "трезубец",
    "$SWORD": "меч",
    "$ROCK": "камень",
    "$CURSE": "проклятие",
    "$WIRE_EXTENSION": "удлинитель",
    "$SONIC_BLASTER": "звуковое оружие",
}

ship_weapons = [
    {"$ARCHERY_BOW": "🏹"},
    {"$DAGGER": "🗡️", "$TRIDENT": "🔱", "$SWORD": "⚔️"},
    {"$POISON": "⚗️"},
    {"$HAMMER": "🔨", "$WRENCH": "🔧", "$CANDLESTICK": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

ancient_egypt_weapons = [
    {"$ARCHERY_BOW": "🏹"},
    {"$DAGGER": "🗡️"},
    {"$POISON": "⚗️", "$CURSE": "📜"},
    {"$ROCK": "🪨", "$CANDLESTICK": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

medieval_castle_weapons = [
    {"$ARCHERY_BOW": "🏹"},
    {"$DAGGER": "🗡️", "$TRIDENT": "🔱", "$SWORD": "⚔️"},
    {"$POISON": "⚗️"},
    {"$ROCK": "🪨", "$CANDLESTICK": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

space_station_weapons = [
    {"$PISTOL": "🔫"},
    {"$KNIFE": "🔪", "$SCISSORS": "✂️", "$AXE": "🪓", "$SCREWDRIVER": "🪛"},
    {"$POISON": "⚗️", "$SONIC_BLASTER": "🔊"},
    {"$HAMMER": "🔨", "$WRENCH": "🔧"},
    {"$ROPE": "🪢", "$WIRE_EXTENSION": "🔌"},
]

museum_weapons = [
    {"$ARCHERY_BOW": "🏹"},
    {"$DAGGER": "🗡️", "$SCISSORS": "✂️", "$TRIDENT": "🔱", "$SWORD": "⚔️"},
    {"$POISON": "⚗️", "$CURSE": "📜"},
    {"$ROCK": "🪨", "$CANDLESTICK": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

island_weapons = [
    {"$ARCHERY_BOW": "🏹"},
    {"$DAGGER": "🗡️", "$AXE": "🪓", "$TRIDENT": "🔱", "$SWORD": "⚔️", "$KNIFE": "🔪"},
    {"$POISON": "⚗️", "$CURSE": "📜"},
    {"$ROCK": "🪨", "$CANDLESTICK": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

zoo_weapons = [
    {"$PISTOL": "🔫"},
    {"$KNIFE": "🔪", "$SCISSORS": "✂️", "$AXE": "🪓", "$SCREWDRIVER": "🪛"},
    {"$POISON": "⚗️"},
    {"$ROCK": "🪨", "$HAMMER": "🔨", "$WRENCH": "🔧"},
    {"$ROPE": "🪢", "$WIRE_EXTENSION": "🔌"},
]

hospital_weapons = [
    {"$PISTOL": "🔫"},
    {"$KNIFE": "🔪", "$SCISSORS": "✂️", "$AXE": "🪓", "$SCREWDRIVER": "🪛"},
    {"$POISON": "⚗️"},
    {"$CANDLESTICK": "🕯️", "$HAMMER": "🔨", "$WRENCH": "🔧"},
    {"$ROPE": "🪢", "$WIRE_EXTENSION": "🔌", "$CHAIN": "⛓️"},
]

sport_club_weapons = [
    {"$PISTOL": "🔫"},
    {"$KNIFE": "🔪", "$SCISSORS": "✂️", "$AXE": "🪓", "$SCREWDRIVER": "🪛"},
    {"$POISON": "⚗️"},
    {"$HAMMER": "🔨", "$WRENCH": "🔧", "$CANDLESTICK": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️", "$WIRE_EXTENSION": "🔌"},
]

school_weapons = [
    {"$ARCHERY_BOW": "🏹"},
    {"$KNIFE": "🔪", "$SCISSORS": "✂️", "$AXE": "🪓", "$SCREWDRIVER": "🪛"},
    {"$POISON": "⚗️"},
    {"$HAMMER": "🔨", "$WRENCH": "🔧", "$CANDLESTICK": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️", "$WIRE_EXTENSION": "🔌"},
]

def get_available_weapons(num_weapons, location_name):

    if location_name == "mansion":
        weapons_sets = classic_weapons[:]
    elif location_name == "ship":
        weapons_sets = ship_weapons[:]
    elif location_name == "egypt":
        weapons_sets = ancient_egypt_weapons[:]
    elif location_name == "castle":
        weapons_sets = medieval_castle_weapons[:]
    elif location_name == "train":
        weapons_sets = classic_weapons[:]
    elif location_name == "space station":
        weapons_sets = space_station_weapons[:]
    elif location_name == "museum":
        weapons_sets = museum_weapons[:]
    elif location_name == "island":
        weapons_sets = island_weapons[:]
    elif location_name == "zoo":
        weapons_sets = zoo_weapons[:]
    elif location_name == "hospital":
        weapons_sets = hospital_weapons[:]
    elif location_name == "sport club":
        weapons_sets = sport_club_weapons[:]
    elif location_name == "abandoned school":
        weapons_sets = school_weapons[:]
    else:
        raise ValueError("Unknown available weapons for" + location_name)

    shuffle(weapons_sets)
    weapons_available = {}
    for weapons_icons in weapons_sets[:num_weapons]:
        weapons_list = list(weapons_icons.items())
        weapon, icon = choice(weapons_list)
        weapons_available[weapon] = icon

    return weapons_available, weapon_labels


def get_weapon_type(weapon):
    if weapon == "$PISTOL" or weapon == "$ARCHERY_BOW":
        return "projectile"
    elif weapon == "$ROPE" or weapon == "$CHAIN" or weapon == "$WIRE_EXTENSION":
        return "strangulation"
    elif (
        weapon == "$KNIFE"
        or weapon == "$DAGGER"
        or weapon == "$SCISSORS"
        or weapon == "$AXE"
        or weapon == "$SCREWDRIVER"
        or weapon == "$TRIDENT"
        or weapon == "$SWORD"
    ):
        return "sharp force"
    elif weapon == "$POISON" or weapon == "$CURSE" or weapon == "$SONIC_BLASTER":
        return "poisoning"
    elif (
        weapon == "$ROCK"
        or weapon == "$HAMMER"
        or weapon == "$WRENCH"
        or weapon == "$CANDLESTICK"
    ):
        return "blunt force"
    else:
        raise ValueError("Unknown type of weapon: " + weapon)

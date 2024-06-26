from random import shuffle, choice

all_weapons = [
    {"$PISTOL": "🔫"},
    {"$KNIFE": "🔪", "$SCISSORS": "✂️", "$AXE": "🪓", "$SCREWDRIVER": "🪛"},
    {"$POISON": "⚗️"},
    {"$HAMMER": "🔨", "$WRENCH": "🔧", "$CANDELABRUM": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

weapon_labels = {}

weapon_labels['en'] = {
    "$PISTOL": "pistol",
    "$KNIFE": "knife",
    "$SCISSORS": "scissors",
    "$AXE": "axe",
    "$SCREWDRIVER": "screwdriver",
    "$POISON": "poison",
    "$HAMMER": "hammer",
    "$WRENCH": "wrench",
    "$CANDELABRUM": "candelabrum",
    "$ROPE": "rope",
    "$CHAIN": "chain",
    "$ARCHERY_BOW": "archery bow",
    "$DAGGER": "dagger",
    "$TRIDENT": "trident",
    "$SWORD": "sword",
    "$ROCK": "rock",
    "$POISON": "poison",
    "$CURSE": "curse"
}

weapon_labels['es'] = {
    "$PISTOL": "la pistola",
    "$KNIFE": "el cuchillo",
    "$SCISSORS": "las tijeras",
    "$AXE": "el hacha",
    "$SCREWDRIVER": "el destornillador",
    "$POISON": "el veneno",
    "$HAMMER": "el martillo",
    "$WRENCH": "la llave inglesa",
    "$CANDELABRUM": "el candelabro",
    "$ROPE": "la soga",
    "$CHAIN": "la cadena",
    "$ARCHERY_BOW": "el arco",
    "$DAGGER": "la daga",
    "$TRIDENT": "el tridente",
    "$SWORD": "la espada",
    "$ROCK": "la roca",
    "$POISON": "el veneno",
    "$CURSE": "la maldición"
}

ship_weapons = [
    {"$ARCHERY_BOW": "🏹"},
    {"$DAGGER": "🗡️", "$TRIDENT": "🔱", "$SWORD": "⚔️"},
    {"$POISON": "⚗️"},
    {"$HAMMER": "🔨", "$WRENCH": "🔧", "$CANDELABRUM": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

ancient_egypt_weapons = [
    {"$ARCHERY_BOW": "🏹"},
    {"$DAGGER": "🗡️"},
    {"$POISON": "⚗️", "$CURSE": "📜"},
    {"$ROCK": "🪨", "$CANDELABRUM": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

medieval_castle_weapons = [
    {"$ARCHERY_BOW": "🏹"},
    {"$DAGGER": "🗡️", "$TRIDENT": "🔱", "$SWORD": "⚔️"},
    {"$POISON": "⚗️"},
    {"$ROCK": "🪨", "$CANDELABRUM": "🕯️"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

space_station_weapons = [
    {"$PISTOL": "🔫"},
    {"$KNIFE": "🔪", "$SCISSORS": "✂️", "$AXE": "🪓", "$SCREWDRIVER": "🪛"},
    {"$POISON": "⚗️"},
    {"$HAMMER": "🔨", "$WRENCH": "🔧"},
    {"$ROPE": "🪢", "$CHAIN": "⛓️"},
]

def get_available_weapons(num_weapons, location_name):

    if location_name == "mansion":
        weapons_sets = all_weapons[:]
    elif location_name == "ship":
        weapons_sets = ship_weapons[:]
    elif location_name == "egypt":
        weapons_sets = ancient_egypt_weapons[:]
    elif location_name == "castle":
        weapons_sets = medieval_castle_weapons[:]
    elif location_name == "train":
        weapons_sets = all_weapons[:]
    elif location_name == "space station":
        weapons_sets = space_station_weapons[:]
    else:
        assert False, "Unknown available weapons for" + location_name

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
    elif weapon == "$ROPE" or weapon == "$CHAIN":
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
    elif weapon == "$POISON" or weapon == "$CURSE":
        return "poisoning"
    elif (
        weapon == "$ROCK"
        or weapon == "$HAMMER"
        or weapon == "$WRENCH"
        or weapon == "$CANDELABRUM"
    ):
        return "blunt force"
    else:
        assert False, "Unknown type of weapon: " + weapon

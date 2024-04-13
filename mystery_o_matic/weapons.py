from random import shuffle, choice

all_weapons = [
    {"pistol": "🔫"},
    {"knife": "🔪", "scissors": "✂️", "axe": "🪓", "screwdriver": "🪛"},
    {"poison": "⚗️"},
    {"hammer": "🔨", "wrench": "🔧", "candelabrum": "🕯️"},
    {"rope": "🪢", "chain": "⛓️"}
]

ancient_egypt_weapons = [
    {"archery bow": "🏹"},
    {"dagger": "🗡️"},
    {"poison": "⚗️", "curse": "📜"},
    {"rock": "🪨", "candelabrum": "🕯️"},
    {"rope": "🪢", "chain": "⛓️"}
]

medieval_castle_weapons = [
    {"archery bow": "🏹"},
    {"dagger": "🗡️", "trident": "🔱", "sword": "⚔️"},
    {"poison": "⚗️"},
    {"rock": "🪨", "candelabrum": "🕯️"},
    {"rope": "🪢", "chain": "⛓️"}
]

def get_available_weapons(num_weapons, location_name):

    if (location_name == "mansion"):
        weapons_sets = all_weapons[:]
    elif (location_name == "egypt"):
        weapons_sets = ancient_egypt_weapons[:]
    elif (location_name == "castle"):
        weapons_sets = medieval_castle_weapons[:]
    else:
        assert False, "Unknown available weapons for" + location_name

    shuffle(weapons_sets)
    weapons_available = {}
    for weapons_icons in weapons_sets[:num_weapons]:
        weapons_list = list(weapons_icons.items())
        weapon, icon = choice(weapons_list)
        weapons_available[weapon] = icon

    return weapons_available

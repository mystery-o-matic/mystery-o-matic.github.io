from random import shuffle, choice

weapons_sets = [
    {"pistol": "🔫"},
    {"knife": "🔪", "dagger": "🗡️", "scissors": "✂️", "axe": "🪓", "screwdriver": "🪛"},
    {"poison": "⚗️"},
    {"hammer": "🔨", "wrench": "🔧", "candelabrum": "🕯️"},
    {"rope": "🪢", "chain": "⛓️"}
]

def get_available_weapons():
    shuffle(weapons_sets)
    weapons_available = {}
    for weapons_icons in weapons_sets[:4]:
        weapons_list = list(weapons_icons.items())
        weapon, icon = choice(weapons_list)
        weapons_available[weapon] = icon

    return weapons_available

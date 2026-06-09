"""Distinguishing features ("tells") for the character-profile mechanic.

Each character is assigned ONE unique tell. Foggy sightings (which today render
the seen person as a bare "somebody") instead render "someone <clue form>", and
the player resolves who that is by reading the tell in the suspect's profile.

Each entry carries two localized forms per language:
  - "clue": the form used inside a sighting, including the connective and the
    correct grammatical case (e.g. EN "wearing a crimson silk scarf",
    RU prepositional/instrumental). It follows the word "someone/alguien/кого-то".
  - "bio":  the bare nominative noun phrase shown in the profile modal
    (e.g. EN "a crimson silk scarf").

The pool is universal (period/location-neutral) so it works in every setting,
and is comfortably larger than the maximum cast size (6) so a unique assignment
is always possible.

NOTE: the Russian forms are authored to the best of our ability and should be
reviewed by a native speaker before a wide release (worn items use "в" +
prepositional, carried items / mannerisms use "с" + instrumental).
"""

# Fixed per-character identity emoji, mirroring the (secret) book where each
# character's portrait is a specific emoji. Shown in the profile modal.
CHARACTER_EMOJIS = {
    "alice": "👱‍♀️",   # blonde-woman
    "bob": "👱‍♂️",     # blond-haired-man
    "carol": "👩",      # woman
    "dave": "🧔",       # bearded-person
    "eddie": "👦",      # boy
    "frida": "👩‍🦳",   # white-haired-woman
}

# Coarse gender/age descriptor per character ("a woman" / "a man" / "a boy"),
# used as an EXCLUSIVE alternative to a trait on a foggy sighting: a clue shows
# either a specific tell, or this category, or a plain "somebody" — never a tell
# and a category together. The player resolves it via the character emojis shown
# in the profiles. RU forms are accusative (the seen object), authored to the
# best of our ability — review by a native speaker (see note above).
CHARACTER_DESCRIPTORS = {
    "alice": {"en": "a woman", "es": "una mujer", "ru": "женщину"},
    "bob":   {"en": "a man",   "es": "un hombre", "ru": "мужчину"},
    "carol": {"en": "a woman", "es": "una mujer", "ru": "женщину"},
    "dave":  {"en": "a man",   "es": "un hombre", "ru": "мужчину"},
    "eddie": {"en": "a man",   "es": "un hombre", "ru": "мужчину"},
    "frida": {"en": "a woman", "es": "una mujer", "ru": "женщину"},
}

# Coarse property-based foggy-sighting categories — even less specific than the
# exact trait or the gender. Keyed by fog_kind; only offered when the cast is
# MIXED on that property (some traits carry the flag, some don't), so the hint
# still narrows. Baked-in phrases (no per-character token), resolved to yes/no at
# clue-build time. To add a category: flag the relevant traits, add a "<x>_yes"/
# "<x>_no" pair here + FOG_* constants, and list it in mystery.py's selection.
COARSE_PHRASES = {
    "hat_yes":     {"en": "someone with some kind of hat",
                    "es": "alguien con algún tipo de sombrero",
                    "ru": "кого-то в какой-то шляпе"},
    "hat_no":      {"en": "someone without any kind of hat",
                    "es": "alguien sin ningún tipo de sombrero",
                    "ru": "кого-то без шляпы"},
    "glasses_yes": {"en": "someone wearing glasses",
                    "es": "alguien con gafas",
                    "ru": "кого-то в очках"},
    "glasses_no":  {"en": "someone without glasses",
                    "es": "alguien sin gafas",
                    "ru": "кого-то без очков"},
}

ALL_TRAITS = [
    {
        "id": "crimson_scarf",
        "emoji": "🧣",
        "clue": {"en": "wearing a crimson silk scarf",
                 "es": "con un pañuelo de seda carmesí",
                 "ru": "в малиновом шёлковом шарфе"},
        "bio": {"en": "a crimson silk scarf",
                "es": "un pañuelo de seda carmesí",
                "ru": "малиновый шёлковый шарф"},
    },
    {
        "id": "tortoiseshell_glasses",
        "emoji": "👓",
        "glasses": True,
        "clue": {"en": "wearing round tortoiseshell glasses",
                 "es": "con gafas redondas de carey",
                 "ru": "в круглых черепаховых очках"},
        "bio": {"en": "round tortoiseshell glasses",
                "es": "unas gafas redondas de carey",
                "ru": "круглые черепаховые очки"},
    },
    {
        "id": "baseball_cap",
        "emoji": "🧢",
        "hat": True,
        "clue": {"en": "wearing a faded baseball cap",
                 "es": "con una gorra de béisbol descolorida",
                 "ru": "в выцветшей бейсболке"},
        "bio": {"en": "a faded baseball cap",
                "es": "una gorra de béisbol descolorida",
                "ru": "выцветшая бейсболка"},
    },
    {
        "id": "gloves",
        "emoji": "🧤",
        "clue": {"en": "wearing a pair of gloves",
                 "es": "con un par de guantes",
                 "ru": "в перчатках"},
        "bio": {"en": "a pair of gloves",
                "es": "un par de guantes",
                "ru": "перчатки"},
    },
    {
        "id": "satin_bow",
        "emoji": "🎀",
        "clue": {"en": "wearing a large satin bow",
                 "es": "con un gran lazo de raso",
                 "ru": "с большим атласным бантом"},
        "bio": {"en": "a large satin bow",
                "es": "un gran lazo de raso",
                "ru": "большой атласный бант"},
    },
    {
        "id": "leather_jacket",
        "emoji": "🧥",
        "clue": {"en": "wearing a worn leather jacket",
                 "es": "con una chaqueta de cuero gastada",
                 "ru": "в потёртой кожаной куртке"},
        "bio": {"en": "a worn leather jacket",
                "es": "una chaqueta de cuero gastada",
                "ru": "потёртая кожаная куртка"},
    },
    {
        "id": "diamond_gem",
        "emoji": "💎",
        "clue": {"en": "wearing a sparkling diamond",
                 "es": "con un diamante reluciente",
                 "ru": "со сверкающим бриллиантом"},
        "bio": {"en": "a sparkling diamond",
                "es": "un diamante reluciente",
                "ru": "сверкающий бриллиант"},
    },
    {
        "id": "brass_watch",
        "emoji": "⌚",
        "clue": {"en": "wearing a brass wristwatch",
                 "es": "con un reloj de pulsera de latón",
                 "ru": "с латунными наручными часами"},
        "bio": {"en": "a brass wristwatch",
                "es": "un reloj de pulsera de latón",
                "ru": "латунные наручные часы"},
    },
    {
        "id": "white_cane",
        "emoji": "🦯",
        "clue": {"en": "carrying a slender white cane",
                 "es": "con un bastón blanco delgado",
                 "ru": "с тонкой белой тростью"},
        "bio": {"en": "a slender white cane",
                "es": "un bastón blanco delgado",
                "ru": "тонкая белая трость"},
    },
    {
        "id": "enamel_mug",
        "emoji": "☕",
        "clue": {"en": "carrying a chipped enamel mug",
                 "es": "con una taza de esmalte desportillada",
                 "ru": "со щербатой эмалированной кружкой"},
        "bio": {"en": "a chipped enamel mug",
                "es": "una taza de esmalte desportillada",
                "ru": "щербатая эмалированная кружка"},
    },
    {
        "id": "top_hat",
        "emoji": "🎩",
        "hat": True,
        "clue": {"en": "wearing a velvet top hat",
                 "es": "con un sombrero de copa de terciopelo",
                 "ru": "в бархатном цилиндре"},
        "bio": {"en": "a velvet top hat",
                "es": "un sombrero de copa de terciopelo",
                "ru": "бархатный цилиндр"},
    },
    {
        "id": "folding_fan",
        "emoji": "🪭",
        "clue": {"en": "carrying an ornate folding fan",
                 "es": "con un abanico plegable ornamentado",
                 "ru": "с богато украшенным веером"},
        "bio": {"en": "an ornate folding fan",
                "es": "un abanico plegable ornamentado",
                "ru": "богато украшенный веер"},
    },
    {
        "id": "signet_ring",
        "emoji": "💍",
        "clue": {"en": "wearing a gold signet ring",
                 "es": "con un anillo de sello de oro",
                 "ru": "с золотым перстнем"},
        "bio": {"en": "a gold signet ring",
                "es": "un anillo de sello de oro",
                "ru": "золотой перстень"},
    },
    {
        "id": "military_medal",
        "emoji": "🎖️",
        "clue": {"en": "wearing a military medal",
                 "es": "con una medalla militar",
                 "ru": "с военной медалью"},
        "bio": {"en": "a military medal",
                "es": "una medalla militar",
                "ru": "военная медаль"},
    },
    {
        "id": "rose_lapel",
        "emoji": "🌹",
        "clue": {"en": "wearing a red rose in their lapel",
                 "es": "con una rosa roja en la solapa",
                 "ru": "с красной розой в петлице"},
        "bio": {"en": "a red rose in their lapel",
                "es": "una rosa roja en la solapa",
                "ru": "красная роза в петлице"},
    },
    {
        "id": "leather_briefcase",
        "emoji": "💼",
        "clue": {"en": "carrying a leather briefcase",
                 "es": "con un maletín de cuero",
                 "ru": "с кожаным портфелем"},
        "bio": {"en": "a leather briefcase",
                "es": "un maletín de cuero",
                "ru": "кожаный портфель"},
    },
    {
        "id": "silk_necktie",
        "emoji": "👔",
        "clue": {"en": "wearing a striped silk necktie",
                 "es": "con una corbata de seda a rayas",
                 "ru": "в полосатом шёлковом галстуке"},
        "bio": {"en": "a striped silk necktie",
                "es": "una corbata de seda a rayas",
                "ru": "полосатый шёлковый галстук"},
    },
    {
        "id": "dark_sunglasses",
        "emoji": "🕶️",
        "glasses": True,
        "clue": {"en": "wearing dark sunglasses",
                 "es": "con gafas de sol oscuras",
                 "ru": "в тёмных солнцезащитных очках"},
        "bio": {"en": "dark sunglasses",
                "es": "unas gafas de sol oscuras",
                "ru": "тёмные солнцезащитные очки"},
    },
    {
        "id": "goggles",
        "emoji": "🥽",
        "glasses": True,
        "clue": {"en": "wearing a pair of goggles",
                 "es": "con unas gafas protectoras",
                 "ru": "в защитных очках"},
        "bio": {"en": "a pair of goggles",
                "es": "unas gafas protectoras",
                "ru": "защитные очки"},
    },
    {
        "id": "beaded_handbag",
        "emoji": "👜",
        "clue": {"en": "carrying a beaded handbag",
                 "es": "con un bolso de cuentas",
                 "ru": "с расшитой бисером сумочкой"},
        "bio": {"en": "a beaded handbag",
                "es": "un bolso de cuentas",
                "ru": "расшитая бисером сумочка"},
    },
    {
        "id": "white_lab_coat",
        "emoji": "🥼",
        "clue": {"en": "wearing a white lab coat",
                 "es": "con una bata blanca de laboratorio",
                 "ru": "в белом лабораторном халате"},
        "bio": {"en": "a white lab coat",
                "es": "una bata blanca de laboratorio",
                "ru": "белый лабораторный халат"},
    },
    {
        "id": "canvas_backpack",
        "emoji": "🎒",
        "clue": {"en": "carrying a battered canvas backpack",
                 "es": "con una mochila de lona desgastada",
                 "ru": "с потрёпанным холщовым рюкзаком"},
        "bio": {"en": "a battered canvas backpack",
                "es": "una mochila de lona desgastada",
                "ru": "потрёпанный холщовый рюкзак"},
    },
    {
        "id": "wool_socks",
        "emoji": "🧦",
        "clue": {"en": "wearing thick wool socks",
                 "es": "con gruesos calcetines de lana",
                 "ru": "в толстых шерстяных носках"},
        "bio": {"en": "thick wool socks",
                "es": "unos gruesos calcetines de lana",
                "ru": "толстые шерстяные носки"},
    },
    {
        # 👒 (:woman's_hat:) — a touch silly, kept by request. Safe because trait
        # emojis only ever render as raw unicode in HTML (stripped from LaTeX),
        # so the curly-apostrophe shortname never reaches the \emoji{} pipeline.
        "id": "straw_hat",
        "emoji": "👒",
        "hat": True,
        "clue": {"en": "wearing a wide-brimmed straw hat",
                 "es": "con un sombrero de paja de ala ancha",
                 "ru": "в широкополой соломенной шляпе"},
        "bio": {"en": "a wide-brimmed straw hat",
                "es": "un sombrero de paja de ala ancha",
                "ru": "широкополая соломенная шляпа"},
    },
]

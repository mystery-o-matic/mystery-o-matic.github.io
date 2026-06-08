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
        "clue": {"en": "wearing round tortoiseshell glasses",
                 "es": "con gafas redondas de carey",
                 "ru": "в круглых черепаховых очках"},
        "bio": {"en": "round tortoiseshell glasses",
                "es": "unas gafas redondas de carey",
                "ru": "круглые черепаховые очки"},
    },
    {
        "id": "tweed_cap",
        "emoji": "🧢",
        "clue": {"en": "wearing a moth-eaten tweed cap",
                 "es": "con una gorra de tweed apolillada",
                 "ru": "в потёртой твидовой кепке"},
        "bio": {"en": "a moth-eaten tweed cap",
                "es": "una gorra de tweed apolillada",
                "ru": "потёртая твидовая кепка"},
    },
    {
        "id": "emerald_gloves",
        "emoji": "🧤",
        "clue": {"en": "wearing emerald-green gloves",
                 "es": "con guantes de color verde esmeralda",
                 "ru": "в изумрудно-зелёных перчатках"},
        "bio": {"en": "emerald-green gloves",
                "es": "unos guantes de color verde esmeralda",
                "ru": "изумрудно-зелёные перчатки"},
    },
    {
        "id": "polka_bowtie",
        "emoji": "🎀",
        "clue": {"en": "wearing a polka-dot bow tie",
                 "es": "con una pajarita de lunares",
                 "ru": "в галстуке-бабочке в горошек"},
        "bio": {"en": "a polka-dot bow tie",
                "es": "una pajarita de lunares",
                "ru": "галстук-бабочка в горошек"},
    },
    {
        "id": "straw_hat",
        "emoji": "👒",
        "clue": {"en": "wearing a wide-brimmed straw hat",
                 "es": "con un sombrero de paja de ala ancha",
                 "ru": "в широкополой соломенной шляпе"},
        "bio": {"en": "a wide-brimmed straw hat",
                "es": "un sombrero de paja de ala ancha",
                "ru": "широкополая соломенная шляпа"},
    },
    {
        "id": "fur_coat",
        "emoji": "🧥",
        "clue": {"en": "wearing a fur-trimmed coat",
                 "es": "con un abrigo con ribete de piel",
                 "ru": "в пальто с меховой оторочкой"},
        "bio": {"en": "a fur-trimmed coat",
                "es": "un abrigo con ribete de piel",
                "ru": "пальто с меховой оторочкой"},
    },
    {
        "id": "pearl_earring",
        "emoji": "💎",
        "clue": {"en": "wearing a single pearl earring",
                 "es": "con un solo pendiente de perla",
                 "ru": "с одной жемчужной серёжкой"},
        "bio": {"en": "a single pearl earring",
                "es": "un solo pendiente de perla",
                "ru": "одна жемчужная серёжка"},
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
        "id": "ivory_cane",
        "emoji": "🦯",
        "clue": {"en": "carrying an ivory-handled cane",
                 "es": "con un bastón con mango de marfil",
                 "ru": "с тростью с рукоятью из слоновой кости"},
        "bio": {"en": "an ivory-handled cane",
                "es": "un bastón con mango de marfil",
                "ru": "трость с рукоятью из слоновой кости"},
    },
    {
        "id": "paperback_book",
        "emoji": "📕",
        "clue": {"en": "carrying a worn paperback book",
                 "es": "con un libro de bolsillo gastado",
                 "ru": "с потрёпанной книгой в мягкой обложке"},
        "bio": {"en": "a worn paperback book",
                "es": "un libro de bolsillo gastado",
                "ru": "потрёпанная книга в мягкой обложке"},
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
        "id": "silver_streak",
        "emoji": "🦳",
        "clue": {"en": "with a silver streak in their hair",
                 "es": "con un mechón plateado en el pelo",
                 "ru": "с серебристой прядью в волосах"},
        "bio": {"en": "a silver streak in their hair",
                "es": "un mechón plateado en el pelo",
                "ru": "серебристая прядь в волосах"},
    },
    {
        "id": "ink_fingers",
        "emoji": "🖋️",
        "clue": {"en": "with ink-stained fingers",
                 "es": "con los dedos manchados de tinta",
                 "ru": "с испачканными чернилами пальцами"},
        "bio": {"en": "ink-stained fingers",
                "es": "los dedos manchados de tinta",
                "ru": "испачканные чернилами пальцы"},
    },
    {
        "id": "top_hat",
        "emoji": "🎩",
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
                 "es": "con un abanico ornamentado",
                 "ru": "с резным веером"},
        "bio": {"en": "an ornate folding fan",
                "es": "un abanico ornamentado",
                "ru": "резной веер"},
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
        "id": "military_medals",
        "emoji": "🎖️",
        "clue": {"en": "wearing a row of military medals",
                 "es": "con una hilera de medallas militares",
                 "ru": "с рядом военных медалей"},
        "bio": {"en": "a row of military medals",
                "es": "una hilera de medallas militares",
                "ru": "ряд военных медалей"},
    },
    {
        "id": "rose_boutonniere",
        "emoji": "🌹",
        "clue": {"en": "wearing a red rose boutonnière",
                 "es": "con una rosa roja en la solapa",
                 "ru": "с красной розой в петлице"},
        "bio": {"en": "a red rose boutonnière",
                "es": "una rosa roja en la solapa",
                "ru": "красная роза в петлице"},
    },
]

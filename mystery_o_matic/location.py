from random import shuffle, choice

from networkx import (
    gnp_random_graph,
    relabel_nodes,
    Graph,
    is_planar,
    is_connected,
    planar_layout,
)
from networkx.drawing.nx_agraph import to_agraph

locations = ["egypt", "castle", "train", "ship", "space station", "mansion", "museum", "island", "zoo", "hospital", "sport club", "abandoned school"]

mansions_labels = {}
mansions_labels["en"] = {
    "KITCHEN": "kitchen",
    "DINING": "dining room",
    "BEDROOM": "bedroom",
    "BATHROOM": "bathroom",
    "GARDEN": "garden",
}

mansions_labels["es"] = {
    "KITCHEN": "la cocina",
    "DINING": "el comedor",
    "BEDROOM": "el dormitorio",
    "BATHROOM": "el baño",
    "GARDEN": "el jardín",
}

mansions_labels["ru"] = {
    "KITCHEN": "кухня",
    "DINING": "столовая",
    "BEDROOM": "спальня",
    "BATHROOM": "ванная",
    "GARDEN": "сад",
}

mansions_labels["ru_loc"] = {
    "KITCHEN": "кухне",
    "DINING": "столовой",
    "BEDROOM": "спальне",
    "BATHROOM": "ванной",
    "GARDEN": "саду",
}

mansions_labels["ru_gen"] = {
    "KITCHEN": "кухни",
    "DINING": "столовой",
    "BEDROOM": "спальни",
    "BATHROOM": "ванной",
    "GARDEN": "сада",
}

mansion_intro = {}
mansion_intro["en"] = " are back into <b>the mansion where everything started</b>!"
mansion_intro["es"] = " han vuelto a <b>la mansión donde todo comenzó</b>!"
mansion_intro["ru"] = " снова в <b>особняке, где всё началось</b>!"

mansion_representations = {
    "KITCHEN": "🍲",
    "DINING": "🪑",
    "BEDROOM": "🛏️",
    "BATHROOM": "🚽",
    "GARDEN": "🌳",
}

mansion_activities = {
    "KITCHEN": [
        {"en": "noticed someone cooking", "es": "noté a alguien cocinando", "ru": "заметил(а), как кто-то готовит"},
        {
            "en": "heard someone washing the dishes",
            "es": "escuché a alguien lavando los platos",
            "ru": "услышал(а), как кто-то моет посуду",
        },
        {
            "en": "heard the clatter of pots in the kitchen (🍲)",
            "es": "escuché el ruido de ollas en la cocina (🍲)",
            "ru": "услышал(а) стук кастрюль на кухне (🍲)",
        },
        {"en": "heard a voice coming from the kitchen (🍲)", "es": "escuché una voz que venía desde la cocina (🍲)", "ru": "услышал(а) голос с кухни (🍲)"},
    ],
    "BATHROOM": [
        {
            "en": "heard someone brushing their teeth",
            "es": "escuché a alguien cepillándose los dientes",
            "ru": "услышал(а), как кто-то чистит зубы",
        },
        {
            "en": "heard someone flushing the toilet",
            "es": "escuché a alguien tirando de la cadena",
            "ru": "услышал(а), как кто-то спускает воду",
        },
        {
            "en": "heard the splash of shower in the bathroom (🚽)",
            "es": "escuché el chapoteo de la ducha en el baño (🚽)",
            "ru": "услышал(а) шум душа в ванной (🚽)",
        },
        {"en": "heard a voice coming from the bathroom (🚽)", "es": "escuché una voz que venía desde el baño (🚽)", "ru": "услышал(а) голос из ванной (🚽)"},
    ],
    "GARDEN": [
        {
            "en": "heard someone whistling in the garden (🌳)",
            "es": "escuché a alguien silbando en el jardín (🌳)",
            "ru": "услышал(а), как кто-то насвистывает в саду (🌳)",
        },
        {
            "en": "looked outside and saw someone pruning the bushes",
            "es": "miré afuera y vi a alguien podando los arbustos",
            "ru": "выглянул(а) наружу и увидел(а), как кто-то подстригает кусты",
        },
        {"en": "heard a voice coming from the garden (🌳)", "es": "escuché una voz que venía desde el jardín (🌳)", "ru": "услышал(а) голос из сада (🌳)"},
    ],
    "BEDROOM": [
        {
            "en": "heard someone snoring in the bedroom (🛏️)",
            "es": "escuché a alguien roncando en el dormitorio (🛏️)",
            "ru": "услышал(а) чей-то храп в спальне (🛏️)",
        },
        {"en": "heard a voice coming from the bedroom (🛏️)", "es": "escuché una voz que venía desde el dormitorio (🛏️)", "ru": "услышал(а) голос из спальни (🛏️)"},
    ],
    "DINING": [
        {
            "en": "heard someone playing the piano in the dining room (🪑)",
            "es": "escuché a alguien tocando el piano en el comedor (🪑)",
            "ru": "услышал(а), как кто-то играет на пианино в столовой (🪑)",
        },
        {"en": "heard a voice coming from the dining room (🪑)", "es": "escuché una voz que venía desde el comedor (🪑)", "ru": "услышал(а) голос из столовой (🪑)"},
    ],
}

ship_intro = {}
ship_intro["en"] = " are transported back in time to <b>a pirate ship</b>!"
ship_intro["es"] = " han sido transportados en el tiempo a <b>un barco pirata</b>!"
ship_intro["ru"] = " перенеслись в прошлое на <b>пиратский корабль</b>!"

ship_labels = {}
ship_labels["en"] = {
    "GALLEY": "galley",
    "NAVIGATION ROOM": "navigation room",
    "CAPTAIN CABIN": "captain cabin",
    "MAIN DECK": "main deck",
    "CARGO HOLD": "cargo hold",
}

ship_labels["es"] = {
    "GALLEY": "la cocina",
    "NAVIGATION ROOM": "la sala de navegación",
    "CAPTAIN CABIN": "la cabina del capitán",
    "MAIN DECK": "la cubierta principal",
    "CARGO HOLD": "la bodega de carga",
}

ship_labels["ru"] = {
    "GALLEY": "камбуз",
    "NAVIGATION ROOM": "штурманская рубка",
    "CAPTAIN CABIN": "капитанская каюта",
    "MAIN DECK": "главная палуба",
    "CARGO HOLD": "грузовой трюм",
}

ship_labels["ru_loc"] = {
    "GALLEY": "камбузе",
    "NAVIGATION ROOM": "штурманской рубке",
    "CAPTAIN CABIN": "капитанской каюте",
    "MAIN DECK": "главной палубе",
    "CARGO HOLD": "грузовом трюме",
}

ship_labels["ru_gen"] = {
    "GALLEY": "камбуза",
    "NAVIGATION ROOM": "штурманской рубки",
    "CAPTAIN CABIN": "капитанской каюты",
    "MAIN DECK": "главной палубы",
    "CARGO HOLD": "грузового трюма",
}

ship_representations = {
    "GALLEY": "🍲",
    "NAVIGATION ROOM": "🧭",
    "CAPTAIN CABIN": "🛏️",
    "MAIN DECK": "⚓",
    "CARGO HOLD": "📦",
}

ship_activities = {
    "GALLEY": [
        {"en": "noticed someone cooking", "es": "noté a alguien cocinando", "ru": "заметил(а), как кто-то готовит"},
        {
            "en": "heard someone washing the dishes",
            "es": "escuché a alguien lavando los platos",
            "ru": "услышал(а), как кто-то моет посуду",
        },
        {"en": "heard a voice coming from the galley (🍲)", "es": "escuché una voz que venía desde la cocina (🍲)", "ru": "услышал(а) голос с камбуза (🍲)"},
    ],
    "NAVIGATION ROOM": [
        {"en": "saw someone studying a map", "es": "vi a alguien mirando un mapa", "ru": "увидел(а), как кто-то изучает карту"},
        {
            "en": "heard a voice coming from the navigation room (🧭)",
            "es": "escuché una voz que venía desde la sala de navegación (🧭)",
            "ru": "услышал(а) голос из штурманской рубки (🧭)",
        },
    ],
    "MAIN DECK": [
        {
            "en": "heard someone loading a cannon",
            "es": "escuché a alguien cargando un cañón",
            "ru": "услышал(а), как кто-то заряжает пушку",
        },
        {
            "en": "heard someone adjusting the sails",
            "es": "escuché a alguien ajustando las velas",
            "ru": "услышал(а), как кто-то поправляет паруса",
        },
        {"en": "heard a voice coming from the main deck (⚓)", "es": "escuché una voz que venía desde la cubierta principal (⚓)", "ru": "услышал(а) голос с главной палубы (⚓)"},
    ],
    "CAPTAIN CABIN": [
        {
            "en": "heard someone snoring in the captain cabin (🛏️)",
            "es": "escuché a alguien roncando en la cabina del capitán (🛏️)",
            "ru": "услышал(а) чей-то храп в капитанской каюте (🛏️)",
        },
        {"en": "heard a voice coming from the captain cabin (🛏️)", "es": "escuché una voz que venía desde la cabina del capitán (🛏️)", "ru": "услышал(а) голос из капитанской каюты (🛏️)"},
    ],
    "CARGO HOLD": [
        {
            "en": "heard someone rummaging in the cargo hold (📦)",
            "es": "escuché a alguien revisando la bodega de carga (📦)",
            "ru": "услышал(а), как кто-то роется в грузовом трюме (📦)",
        },
        {"en": "heard a voice coming from the cargo hold (📦)", "es": "escuché una voz que venía desde la bodega de carga (📦)", "ru": "услышал(а) голос из грузового трюма (📦)"},
    ],
}

egypt_intro = {}
egypt_intro["en"] = (
    " are transported back in time to <b>a pyramid in Ancient Egypt</b>!"
)
egypt_intro["es"] = (
    " han sido transportados en el tiempo a <b>una pirámide en el Antiguo Egipto</b>!"
)
egypt_intro["ru"] = " перенеслись в прошлое в <b>пирамиду Древнего Египта</b>!"

island_intro = {}
island_intro["en"] = " are transported to <b>a deserted tropical island</b>!"
island_intro["es"] = " han sido transportados a <b>una isla tropical desierta</b>!"
island_intro["ru"] = " перенеслись на <b>необитаемый тропический остров</b>!"

island_labels = {}
island_labels["en"] = {
    "BEACH": "beach",
    "JUNGLE": "jungle",
    "CAVE": "cave",
    "CLIFF": "cliff",
    "VOLCANO": "volcano",
}

island_labels["es"] = {
    "BEACH": "la playa",
    "JUNGLE": "la jungla",
    "CAVE": "la cueva",
    "CLIFF": "el acantilado",
    "VOLCANO": "el volcán",
}

island_labels["ru"] = {
    "BEACH": "пляж",
    "JUNGLE": "джунгли",
    "CAVE": "пещера",
    "CLIFF": "утёс",
    "VOLCANO": "вулкан",
}

island_labels["ru_loc"] = {
    "BEACH": "пляже",
    "JUNGLE": "джунглях",
    "CAVE": "пещере",
    "CLIFF": "утёсе",
    "VOLCANO": "вулкане",
}

island_labels["ru_gen"] = {
    "BEACH": "пляжа",
    "JUNGLE": "джунглей",
    "CAVE": "пещеры",
    "CLIFF": "утёса",
    "VOLCANO": "вулкана",
}

island_representations = {
    "BEACH": "🏖️",
    "JUNGLE": "🌴",
    "CAVE": "🦇",
    "CLIFF": "⛰️",
    "VOLCANO": "🌋"
}
island_activities = {
    "BEACH": [
        {
            "en": "looked around and saw someone collecting seashells (🏖️)",
            "es": "miré alrededor y vi a alguien recogiendo conchas marinas (🏖️)",
            "ru": "осмотрелся(ась) и увидел(а), как кто-то собирает ракушки (🏖️)",
        },
    ],
    "JUNGLE": [
        {
            "en": "heard someone chopping wood in the jungle (🌴)",
            "es": "escuché a alguien cortando leña en la jungla (🌴)",
            "ru": "услышал(а), как кто-то рубит дрова в джунглях (🌴)",
        },
    ],
    "CAVE": [
        {
            "en": "heard a voice coming from the cave (🦇)",
            "es": "escuché una voz que venía desde la cueva (🦇)",
            "ru": "услышал(а) голос из пещеры (🦇)",
        },
    ],
    "CLIFF": [
        {
            "en": "saw someone climbing the cliff (⛰️)",
            "es": "vi a alguien escalando el acantilado (⛰️)",
            "ru": "увидел(а), как кто-то карабкается на утёс (⛰️)",
        },
    ],
    "VOLCANO": [
        {
            "en": "saw someone inspecting the volcano summit (🌋)",
            "es": "vi a alguien inspeccionando la cima del volcán (🌋)",
            "ru": "увидел(а), как кто-то осматривает кратер вулкана (🌋)",
        },
    ],
}

egypt_labels = {}
egypt_labels["en"] = {
    "THRONE ROOM": "throne room",
    "BURIAL PLACE": "burial chamber",
    "TEMPLE": "temple",
    "DESERT": "desert",
    "GARDEN": "garden",
}

egypt_labels["es"] = {
    "THRONE ROOM": "el cuarto del trono",
    "BURIAL PLACE": "la cámara funeraria",
    "TEMPLE": "el templo",
    "DESERT": "el desierto",
    "GARDEN": "el jardín",
}

egypt_labels["ru"] = {
    "THRONE ROOM": "тронный зал",
    "BURIAL PLACE": "погребальная камера",
    "TEMPLE": "храм",
    "DESERT": "пустыня",
    "GARDEN": "сад",
}

egypt_labels["ru_loc"] = {
    "THRONE ROOM": "тронном зале",
    "BURIAL PLACE": "погребальной камере",
    "TEMPLE": "храме",
    "DESERT": "пустыне",
    "GARDEN": "саду",
}

egypt_labels["ru_gen"] = {
    "THRONE ROOM": "тронного зала",
    "BURIAL PLACE": "погребальной камеры",
    "TEMPLE": "храма",
    "DESERT": "пустыни",
    "GARDEN": "сада",
}

egypt_representations = {
    "THRONE ROOM": "👑",
    "BURIAL PLACE": "⚱️",
    "TEMPLE": "📿",
    "DESERT": "🏜️",
    "GARDEN": "🌳",
}

egypt_activities = {
    "THRONE ROOM": [
        {
            "en": "saw someone from a distance sitting on the throne",
            "es": "vi a alguien sentado en el trono a lo lejos",
            "ru": "издалека увидел(а), как кто-то сидит на троне",
        },
        {
            "en": "saw someone from afar polishing the throne",
            "es": "vi a alguien puliendo el trono a lo lejos",
            "ru": "издалека увидел(а), как кто-то полирует трон",
        },
        {"en": "heard a voice coming from the throne room (👑)", "es": "escuché una voz que venía desde el cuarto del trono (👑)", "ru": "услышал(а) голос из тронного зала (👑)"},
    ],
    "BURIAL PLACE": [
        {
            "en": "saw someone at a distance praying in the burial chamber (⚱️)",
            "es": "vi a alguien rezando en la cámara funeraria a lo lejos (⚱️)",
            "ru": "издалека увидел(а), как кто-то молится в погребальной камере (⚱️)",
        },
        {"en": "heard a voice coming from the burial chamber (⚱️)", "es": "escuché una voz que venía desde la cámara funeraria (⚱️)", "ru": "услышал(а) голос из погребальной камеры (⚱️)"},
    ],
    "TEMPLE": [
        {
            "en": "saw someone at a distance praying in the temple (📿)",
            "es": "vi a alguien a la distancia rezando en el templo (📿)",
            "ru": "издалека увидел(а), как кто-то молится в храме (📿)",
        },
        {
            "en": "saw someone from afar lighting candles in the temple (📿)",
            "es": "vi a alguien a la distancia encendiendo velas en el templo (📿)",
            "ru": "издалека увидел(а), как кто-то зажигает свечи в храме (📿)",
        },
        {"en": "heard a voice coming from the temple (📿)", "es": "escuché una voz que venía desde el templo (📿)", "ru": "услышал(а) голос из храма (📿)"},
    ],
    "DESERT": [
        {
            "en": "looked outside and saw someone riding a camel in the desert (🏜️)",
            "es": "miré afuera y vi a alguien montando un camello en el desierto (🏜️)",
            "ru": "выглянул(а) наружу и увидел(а), как кто-то едет на верблюде в пустыне (🏜️)",
        },
    ],
    "GARDEN": [
        {
            "en": "heard someone whistling in the garden (🌳)",
            "es": "escuché a alguien silbando en el jardín (🌳)",
            "ru": "услышал(а), как кто-то насвистывает в саду (🌳)",
        },
        {
            "en": "looked outside and saw someone pruning the bushes",
            "es": "miré afuera y vi a alguien podando los arbustos",
            "ru": "выглянул(а) наружу и увидел(а), как кто-то подстригает кусты",
        },
        {"en": "heard a voice coming from the garden (🌳)", "es": "escuché una voz que venía desde el jardín (🌳)", "ru": "услышал(а) голос из сада (🌳)"},
    ],
}

medieval_castle_intro = {}
medieval_castle_intro["en"] = (
    " are transported back in time to <b>a castle in the Middle Ages</b>!"
)
medieval_castle_intro["es"] = (
    " han sido transportados en el tiempo a <b>un castillo en la Edad Media</b>!"
)
medieval_castle_intro["ru"] = " перенеслись в прошлое в <b>замок Средневековья</b>!"

medieval_castle_labels = {}
medieval_castle_labels["en"] = {
    "GREAT HALL": "great hall",
    "BED CHAMBER": "bed chamber",
    "DUNGEON": "dungeon",
    "ARMORY": "armory",
    "GARDEN": "garden",
}

medieval_castle_labels["es"] = {
    "GREAT HALL": "el gran salón",
    "BED CHAMBER": "el dormitorio principal",
    "DUNGEON": "la mazmorra",
    "ARMORY": "la armería",
    "GARDEN": "el jardín",
}

medieval_castle_labels["ru"] = {
    "GREAT HALL": "большой зал",
    "BED CHAMBER": "опочивальня",
    "DUNGEON": "темница",
    "ARMORY": "оружейная",
    "GARDEN": "сад",
}

medieval_castle_labels["ru_loc"] = {
    "GREAT HALL": "большом зале",
    "BED CHAMBER": "опочивальне",
    "DUNGEON": "темнице",
    "ARMORY": "оружейной",
    "GARDEN": "саду",
}

medieval_castle_labels["ru_gen"] = {
    "GREAT HALL": "большого зала",
    "BED CHAMBER": "опочивальни",
    "DUNGEON": "темницы",
    "ARMORY": "оружейной",
    "GARDEN": "сада",
}

medieval_castle_representations = {
    "GREAT HALL": "🍷",
    "BED CHAMBER": "🛏️",
    "DUNGEON": "🔒",
    "ARMORY": "🛡️",
    "GARDEN": "🌳",
}

medieval_castle_activities = {
    "GREAT HALL": [
        {
            "en": "heard someone playing the harp in the great hall (🍷)",
            "es": "escuché a alguien tocando el arpa en el gran salón (🍷)",
            "ru": "услышал(а), как кто-то играет на арфе в большом зале (🍷)",
        },
        {
            "en": "saw someone from a distance dancing in the great hall (🍷)",
            "es": "vi a alguien bailando en el gran salón (🍷) a lo lejos",
            "ru": "издалека увидел(а), как кто-то танцует в большом зале (🍷)",
        },
        {"en": "heard a voice coming from the great hall (🍷)", "es": "escuché una voz que venía desde el gran salón (🍷)", "ru": "услышал(а) голос из большого зала (🍷)"},
    ],
    "ARMORY": [
        {
            "en": "saw someone from afar sharpening a sword in the armory (🛡️)",
            "es": "vi a alguien afilando una espada en la armería (🛡️) a lo lejos ",
            "ru": "издалека увидел(а), как кто-то точит меч в оружейной (🛡️)",
        },
        {
            "en": "saw someone at a distance polishing a shield in the armory (🛡️)",
            "es": "vi a alguien puliendo un escudo en la armería (🛡️) a lo lejos",
            "ru": "издалека увидел(а), как кто-то полирует щит в оружейной (🛡️)",
        },
        {"en": "heard a voice coming from the armory (🛡️)", "es": "escuché una voz que venía desde la armería (🛡️)", "ru": "услышал(а) голос из оружейной (🛡️)"},
    ],
    "DUNGEON": [
        {
            "en": "heard someone screaming in the dungeon (🔒)",
            "es": "escuché a alguien gritando en la mazmorra (🔒)",
            "ru": "услышал(а) чей-то крик из темницы (🔒)",
        },
        {"en": "heard a voice coming from the dungeon (🔒)", "es": "escuché una voz que venía desde la mazmorra (🔒)", "ru": "услышал(а) голос из темницы (🔒)"},
    ],
    "BED CHAMBER": [
        {
            "en": "heard someone snoring in the bed chamber (🛏️)",
            "es": "escuché a alguien roncando en el dormitorio principal (🛏️)",
            "ru": "услышал(а) чей-то храп в опочивальне (🛏️)",
        },
        {"en": "heard a voice coming from the bed chamber (🛏️)", "es": "escuché una voz que venía desde el dormitorio principal (🛏️)", "ru": "услышал(а) голос из опочивальни (🛏️)"},
    ],
    "GARDEN": [
        {
            "en": "heard someone whistling in the garden (🌳)",
            "es": "escuché a alguien silbando en el jardín (🌳)",
            "ru": "услышал(а), как кто-то насвистывает в саду (🌳)",
        },
        {
            "en": "looked outside and saw someone pruning the bushes",
            "es": "miré afuera y vi a alguien podando los arbustos",
            "ru": "выглянул(а) наружу и увидел(а), как кто-то подстригает кусты",
        },
        {"en": "heard a voice coming from the garden (🌳)", "es": "escuché una voz que venía desde el jardín (🌳)", "ru": "услышал(а) голос из сада (🌳)"},
    ],
}

museum_intro = {}
museum_intro["en"] = " are transported into <b>an empty museum at night</b>!"
museum_intro["es"] = " han sido transportados a <b>un museo vacío por la noche</b>!"
museum_intro["ru"] = " перенеслись в <b>пустой музей ночью</b>!"

museum_labels = {}
museum_labels["en"] = {
    "DINOSAUR EXHIBIT": "dinosaur exhibit",
    "EGYPTIAN EXHIBIT": "egyptian exhibit",
    "MEDIEVAL EXHIBIT": "medieval exhibit",
    "SPACE EXHIBIT": "space exhibit",
    "OCEAN EXHIBIT": "ocean exhibit",
}

museum_labels["es"] = {
    "DINOSAUR EXHIBIT": "la exhibición de dinosaurios",
    "EGYPTIAN EXHIBIT": "la exhibición egipcia",
    "MEDIEVAL EXHIBIT": "la exhibición medieval",
    "SPACE EXHIBIT": "la exhibición espacial",
    "OCEAN EXHIBIT": "la exhibición oceánica",
}

museum_labels["ru"] = {
    "DINOSAUR EXHIBIT": "зал динозавров",
    "EGYPTIAN EXHIBIT": "египетский зал",
    "MEDIEVAL EXHIBIT": "средневековый зал",
    "SPACE EXHIBIT": "космический зал",
    "OCEAN EXHIBIT": "океанский зал",
}

museum_labels["ru_loc"] = {
    "DINOSAUR EXHIBIT": "зале динозавров",
    "EGYPTIAN EXHIBIT": "египетском зале",
    "MEDIEVAL EXHIBIT": "средневековом зале",
    "SPACE EXHIBIT": "космическом зале",
    "OCEAN EXHIBIT": "океанском зале",
}

museum_labels["ru_gen"] = {
    "DINOSAUR EXHIBIT": "зала динозавров",
    "EGYPTIAN EXHIBIT": "египетского зала",
    "MEDIEVAL EXHIBIT": "средневекового зала",
    "SPACE EXHIBIT": "космического зала",
    "OCEAN EXHIBIT": "океанского зала",
}

museum_representations = {
    "DINOSAUR EXHIBIT": "🦖",
    "EGYPTIAN EXHIBIT": "⚱️",
    "MEDIEVAL EXHIBIT": "🛡️",
    "SPACE EXHIBIT": "🪐",
    "OCEAN EXHIBIT": "🐠",
}

museum_activities = {
    "DINOSAUR EXHIBIT": [
        {"en": "heard a voice coming from the dinosaur exhibit (🦖)", "es": "escuché una voz que venía desde la exhibición de dinosaurios (🦖)", "ru": "услышал(а) голос из зала динозавров (🦖)"}
    ],
    "EGYPTIAN EXHIBIT": [
        {"en": "heard a voice coming from the egyptian exhibit (⚱️)", "es": "escuché una voz que venía desde la exhibición egipcia (⚱️)", "ru": "услышал(а) голос из египетского зала (⚱️)"}
    ],
    "MEDIEVAL EXHIBIT": [
        {"en": "heard a voice coming from the medieval exhibit (🛡️)", "es": "escuché una voz que venía desde la exhibición medieval (🛡️)", "ru": "услышал(а) голос из средневекового зала (🛡️)"}
    ],
    "SPACE EXHIBIT": [
        {"en": "heard a voice coming from the space exhibit (🪐)", "es": "escuché una voz que venía desde la exhibición espacial (🪐)", "ru": "услышал(а) голос из космического зала (🪐)"}
    ],
    "OCEAN EXHIBIT": [
        {"en": "heard a voice coming from the ocean exhibit (🐠)", "es": "escuché una voz que venía desde la exhibición oceánica (🐠)", "ru": "услышал(а) голос из океанского зала (🐠)"}
    ]
}

train_intro = {}
train_intro["en"] = (
    " are transported back in time to <b>the famous Orient Express</b> during its last voyage!"
)
train_intro["es"] = (
    " han sido transportados en el tiempo al <b>famoso Orient Express</b> durante su último viaje!"
)
train_intro["ru"] = " перенеслись в прошлое на <b>знаменитый Восточный экспресс</b> во время его последнего рейса!"

train_labels = {}
train_labels["en"] = {
    "LOCOMOTIVE": "locomotive",
    "LUGGAGE": "luggage carriage",
    "DINING": "dining carriage",
    "SLEEPING": "sleeping carriage",
    "LOUNGE": "lounge carriage",
}

train_labels["es"] = {
    "LOCOMOTIVE": "la locomotora",
    "LUGGAGE": "el vagón de equipaje",
    "DINING": "el vagón comedor",
    "SLEEPING": "el vagón dormitorio",
    "LOUNGE": "el vagón salón",
}

train_labels["ru"] = {
    "LOCOMOTIVE": "локомотив",
    "LUGGAGE": "багажный вагон",
    "DINING": "вагон-ресторан",
    "SLEEPING": "спальный вагон",
    "LOUNGE": "салон-вагон",
}

train_labels["ru_loc"] = {
    "LOCOMOTIVE": "локомотиве",
    "LUGGAGE": "багажном вагоне",
    "DINING": "вагоне-ресторане",
    "SLEEPING": "спальном вагоне",
    "LOUNGE": "салоне-вагоне",
}

train_labels["ru_gen"] = {
    "LOCOMOTIVE": "локомотива",
    "LUGGAGE": "багажного вагона",
    "DINING": "вагона-ресторана",
    "SLEEPING": "спального вагона",
    "LOUNGE": "салона-вагона",
}

train_representations = {
    "LOCOMOTIVE": "🚂",
    "LUGGAGE": "🧳",
    "DINING": "🍽️",
    "SLEEPING": "🛌",
    "LOUNGE": "🪑",
}

train_activities = {
    "LOCOMOTIVE": [
        {
            "en": "glanced out the window and saw someone shoveling coal into the locomotive’s furnace (🚂)",
            "es": "miré por la ventana y vi a alguien echando carbón al horno de la locomotora (🚂)",
            "ru": "взглянул(а) в окно и увидел(а), как кто-то бросает уголь в топку локомотива (🚂)",
        },
        {
            "en": "heard a loud clang of tools in the locomotive (🚂)",
            "es": "escuché un golpe fuerte de herramientas en la locomotora (🚂)",
            "ru": "услышал(а) громкий лязг инструментов в локомотиве (🚂)",
        },
        {
            "en": "heard the whistle of the locomotive",
            "es": "escuché el silbido de la locomotora",
            "ru": "услышал(а) свисток локомотива",
        },
        {"en": "heard a voice coming from the locomotive (🚂)", "es": "escuché una voz que venía desde la locomotora (🚂)", "ru": "услышал(а) голос из локомотива (🚂)"},
    ],
    "LUGGAGE": [
        {
            "en": "heard someone rummaging in luggage carriage (🧳)",
            "es": "escuché a alguien revisando el vagón de carga (🧳)",
            "ru": "услышал(а), как кто-то роется в багажном вагоне (🧳)",
        },
        {"en": "heard a voice coming from the luggage carriage (🧳)", "es": "escuché una voz que venía desde el vagón de carga (🧳)", "ru": "услышал(а) голос из багажного вагона (🧳)"},
    ],
    "DINING": [
        {
            "en": "glanced out my window and saw someone eating in the dining carriage (🍽️)",
            "es": "miré por la ventana y vi a alguien comiendo en el vagón comedor (🍽️)",
            "ru": "взглянул(а) в окно и увидел(а), как кто-то ест в вагоне-ресторане (🍽️)",
        },
        {
            "en": "saw someone pouring wine in the dining carriage (🍽️)",
            "es": "vi a alguien sirviendose vino en el vagón comedor (🍽️)",
            "ru": "увидел(а), как кто-то наливает вино в вагоне-ресторане (🍽️)",
        },
        {
            "en": "heard someone playing the piano in the dining carriage (🍽️)",
            "es": "escuché a alguien tocando el piano en el vagón comedor (🍽️)",
            "ru": "услышал(а), как кто-то играет на пианино в вагоне-ресторане (🍽️)",
        },
        {"en": "heard a voice coming from the dining carriage (🍽️)", "es": "escuché una voz que venía desde el vagón comedor (🍽️)", "ru": "услышал(а) голос из вагона-ресторана (🍽️)"},
    ],
    "SLEEPING": [
        {
            "en": "heard someone snoring in the sleeping carriage (🛌)",
            "es": "escuché a alguien roncando en el vagón dormitorio (🛌)",
            "ru": "услышал(а) чей-то храп в спальном вагоне (🛌)",
        },
        {
            "en": "saw someone adjusting the curtains in the sleeping carriage (🛌)",
            "es": "vi a alguien ajustando las cortinas en el vagón dormitorio (🛌)",
            "ru": "увидел(а), как кто-то поправляет шторы в спальном вагоне (🛌)",
        },
        {"en": "heard a voice coming from the sleeping carriage (🛌)", "es": "escuché una voz que venía desde el vagón dormitorio (🛌)", "ru": "услышал(а) голос из спального вагона (🛌)"},
    ],
    "LOUNGE": [
        {
            "en": "glanced out my window and saw someone reading in the lounge carriage (🪑)",
            "es": "miré por la ventana y vi a alguien leyendo en el vagón salón (🪑)",
            "ru": "взглянул(а) в окно и увидел(а), как кто-то читает в салон-вагоне (🪑)",
        },
        {"en": "heard a voice coming from the lounge carriage (🪑)", "es": "escuché una voz que venía desde el vagón salón (🪑)", "ru": "услышал(а) голос из салон-вагона (🪑)"},
    ],
}

space_station_intro = {}
space_station_intro["en"] = (
    " are transported into the future to <b>a high-tech space station</b> orbiting an unknown planet!"
)
space_station_intro["es"] = (
    " han sido transportados al futuro a <b>una estación espacial de alta tecnología</b> orbitando un planeta desconocido!"
)
space_station_intro["ru"] = " перенеслись в будущее на <b>высокотехнологичную космическую станцию</b>, вращающуюся вокруг неизвестной планеты!"

space_station_labels = {}
space_station_labels["en"] = {
    "COMMAND": "command module",
    "LAB": "lab module",
    "AIRLOCK": "airlock module",
    "SLEEPING": "sleeping module",
    "GARDEN": "garden module",
}

space_station_labels["es"] = {
    "COMMAND": "el módulo de comando",
    "LAB": "el módulo de laboratorio",
    "AIRLOCK": "el módulo de esclusa",
    "SLEEPING": "el módulo de descanso",
    "GARDEN": "el módulo de jardín",
}

space_station_labels["ru"] = {
    "COMMAND": "командный модуль",
    "LAB": "лабораторный модуль",
    "AIRLOCK": "шлюзовой модуль",
    "SLEEPING": "жилой модуль",
    "GARDEN": "садовый модуль",
}

space_station_labels["ru_loc"] = {
    "COMMAND": "командном модуле",
    "LAB": "лабораторном модуле",
    "AIRLOCK": "шлюзовом модуле",
    "SLEEPING": "жилом модуле",
    "GARDEN": "садовом модуле",
}

space_station_labels["ru_gen"] = {
    "COMMAND": "командного модуля",
    "LAB": "лабораторного модуля",
    "AIRLOCK": "шлюзового модуля",
    "SLEEPING": "жилого модуля",
    "GARDEN": "садового модуля",
}

space_station_representations = {
    "COMMAND": "🕹️",
    "LAB": "🔬",
    "AIRLOCK": "🔒",
    "SLEEPING": "🛌",
    "GARDEN": "🥔",
}

space_station_activities = {
    "COMMAND": [
        {
            "en": "saw someone adjusting the station’s orbit on the command module’s screens",
            "es": "vi a alguien ajustando la órbita de la estación en las pantallas del módulo de comando (🕹️)",
            "ru": "увидел(а), как кто-то корректирует орбиту станции на экранах командного модуля (🕹️)",
        },
        {"en": "heard a voice coming from the command module (🕹️)", "es": "escuché una voz que venía desde el módulo de comando (🕹️)", "ru": "услышал(а) голос из командного модуля (🕹️)"},
    ],
    "LAB": [
        {
            "en": "saw someone mixing glowing chemicals in the lab module (🔬)",
            "es": "vi a alguien mezclando químicos brillantes en el módulo de laboratorio (🔬)",
            "ru": "увидел(а), как кто-то смешивает светящиеся химикаты в лабораторном модуле (🔬)",
        },
        {"en": "heard a voice coming from the lab module (🔬)", "es": "escuché una voz que venía desde el módulo de laboratorio (🔬)", "ru": "услышал(а) голос из лабораторного модуля (🔬)"},
    ],
    "AIRLOCK": [
        {
            "en": "heard a hiss of depressurization from the airlock module (🔒)",
            "es": "escuché un silbido de despresurización desde el módulo de esclusa (🔒)",
            "ru": "услышал(а) шипение декомпрессии из шлюзового модуля (🔒)",
        },
        {"en": "heard a voice coming from the airlock module (🔒)", "es": "escuché una voz que venía desde el módulo de esclusa (🔒)", "ru": "услышал(а) голос из шлюзового модуля (🔒)"},
    ],
    "SLEEPING": [
        {
            "en": "heard someone snoring in the sleeping module (🛌)",
            "es": "escuché a alguien roncando en el módulo de descanso (🛌)",
            "ru": "услышал(а) чей-то храп в жилом модуле (🛌)",
        },
        {
            "en": "heard a metallic clank from the sleeping module’s lockers (🛌)",
            "es": "escuché un golpe metálico proveniente de los armarios del módulo de descanso (🛌)",
            "ru": "услышал(а) металлический лязг из шкафчиков жилого модуля (🛌)",
        },
        {"en": "heard a voice coming from the sleeping module (🛌)", "es": "escuché una voz que venía desde el módulo de descanso (🛌)", "ru": "услышал(а) голос из жилого модуля (🛌)"},
    ],
    "GARDEN": [
        {
            "en": "saw someone harvesting potatoes",
            "es": "vi a alguien cosechando patatas",
            "ru": "увидел(а), как кто-то собирает картофель",
        },
        {
            "en": "saw someone watering the hydroponic vines in the garden module (🥔)",
            "es": "vi a alguien regando las enredaderas hidropónicas en el módulo de jardín (🥔)",
            "ru": "увидел(а), как кто-то поливает гидропонные растения в садовом модуле (🥔)",
        },
        {"en": "heard a voice coming from the garden module (🥔)", "es": "escuché una voz que venía desde el módulo de jardín (🥔)", "ru": "услышал(а) голос из садового модуля (🥔)"},
    ]
}

zoo_intro = {}
zoo_intro["en"] = " are transported into <b>an abandoned zoo</b> at night!"
zoo_intro["es"] = " han sido transportados a <b>un zoológico abandonado</b> por la noche!"
zoo_intro["ru"] = " перенеслись в <b>заброшенный зоопарк</b> ночью!"

zoo_labels = {}
zoo_labels["en"] = {
    "LION ENCLOSURE": "lion enclosure",
    "REPTILE HOUSE": "reptile house",
    "AVIARY": "aviary",
    "MONKEY ISLAND": "monkey island",
    "AQUARIUM": "aquarium",
}

zoo_labels["es"] = {
    "LION ENCLOSURE": "el recinto de leones",
    "REPTILE HOUSE": "la casa de reptiles",
    "AVIARY": "el aviario",
    "MONKEY ISLAND": "la isla de monos",
    "AQUARIUM": "el acuario",
}

zoo_labels["ru"] = {
    "LION ENCLOSURE": "вольер львов",
    "REPTILE HOUSE": "террариум",
    "AVIARY": "вольер птиц",
    "MONKEY ISLAND": "остров обезьян",
    "AQUARIUM": "аквариум",
}

zoo_labels["ru_loc"] = {
    "LION ENCLOSURE": "вольере львов",
    "REPTILE HOUSE": "террариуме",
    "AVIARY": "вольере птиц",
    "MONKEY ISLAND": "острове обезьян",
    "AQUARIUM": "аквариуме",
}

zoo_labels["ru_gen"] = {
    "LION ENCLOSURE": "вольера львов",
    "REPTILE HOUSE": "террариума",
    "AVIARY": "вольера птиц",
    "MONKEY ISLAND": "острова обезьян",
    "AQUARIUM": "аквариума",
}

zoo_representations = {
    "LION ENCLOSURE": "🦁",
    "REPTILE HOUSE": "🦎",
    "AVIARY": "🦜",
    "MONKEY ISLAND": "🐒",
    "AQUARIUM": "🐠",
}

zoo_activities = {}

hospital_intro = {}
hospital_intro["en"] = " are transported into <b>a deserted hospital</b> at night!"
hospital_intro["es"] = " han sido transportados a <b>un hospital desierto</b> por la noche!"
hospital_intro["ru"] = " перенеслись в <b>пустую больницу</b> ночью!"

hospital_labels = {}
hospital_labels["en"] = {
    "ER": "emergency room",
    "ICU": "intensive care unit",
    "OPERATING THEATER": "operating theater",
    "PHARMACY": "pharmacy",
    "LOBBY": "lobby",
}

hospital_labels["es"] = {
    "ER": "la sala de urgencias",
    "ICU": "la unidad de cuidados intensivos",
    "OPERATING THEATER": "el quirófano",
    "PHARMACY": "la farmacia",
    "LOBBY": "el vestíbulo",
}

hospital_labels["ru"] = {
    "ER": "приёмное отделение",
    "ICU": "реанимация",
    "OPERATING THEATER": "операционная",
    "PHARMACY": "аптека",
    "LOBBY": "вестибюль",
}

hospital_labels["ru_loc"] = {
    "ER": "приёмном отделении",
    "ICU": "реанимации",
    "OPERATING THEATER": "операционной",
    "PHARMACY": "аптеке",
    "LOBBY": "вестибюле",
}

hospital_labels["ru_gen"] = {
    "ER": "приёмного отделения",
    "ICU": "реанимации",
    "OPERATING THEATER": "операционной",
    "PHARMACY": "аптеки",
    "LOBBY": "вестибюля",
}

hospital_representations = {
    "ER": "🚑",
    "ICU": "🛏️",
    "OPERATING THEATER": "🔪",
    "PHARMACY": "💊",
    "LOBBY": "💺",
}

hospital_activities = {
    "ER": [
        {"en": "heard a voice coming from the emergency room (🚑)", "es": "escuché una voz que venía desde la sala de urgencias (🚑)", "ru": "услышал(а) голос из приёмного отделения (🚑)"}
    ],
    "ICU": [
        {"en": "heard a voice coming from the intensive care unit (🛏️)", "es": "escuché una voz que venía desde la unidad de cuidados intensivos (🛏️)", "ru": "услышал(а) голос из реанимации (🛏️)"},
    ],
    "OPERATING THEATER": [
        {"en": "heard a voice coming from the operating theater (🔪)", "es": "escuché una voz que venía desde el quirófano (🔪)", "ru": "услышал(а) голос из операционной (🔪)"}
    ],
    "PHARMACY": [
        {"en": "heard a voice coming from the pharmacy (💊)", "es": "escuché una voz que venía desde la farmacia (💊)", "ru": "услышал(а) голос из аптеки (💊)"},
        {"en": "saw someone checking the medicine shelves in the pharmacy (💊)", "es": "vi a alguien revisando las estanterías de medicamentos en la farmacia (💊)", "ru": "увидел(а), как кто-то проверяет полки с лекарствами в аптеке (💊)"}
    ],
    "LOBBY": [
        {"en": "heard a voice coming from the lobby (💺)", "es": "escuché una voz que venía desde el vestíbulo (💺)", "ru": "услышал(а) голос из вестибюля (💺)"}
    ]
}

sport_club_intro = {}
sport_club_intro["en"] = " are transported into <b>an empty sport club</b> at night!"
sport_club_intro["es"] = " han sido transportados a <b>un club deportivo desierto</b> por la noche!"
sport_club_intro["ru"] = " перенеслись в <b>пустой спортивный клуб</b> ночью!"

sport_club_labels = {}
sport_club_labels["en"] = {
    "GYM": "gym",
    "POOL": "swimming pool",
    "SAUNA": "sauna",
    "COURT": "sports court",
    "LOUNGE": "lounge",
}
sport_club_labels["es"] = {
    "GYM": "el gimnasio",
    "POOL": "la piscina",
    "SAUNA": "la sauna",
    "COURT": "la cancha deportiva",
    "LOUNGE": "el salón",
}
sport_club_labels["ru"] = {
    "GYM": "тренажёрный зал",
    "POOL": "бассейн",
    "SAUNA": "сауна",
    "COURT": "спортивная площадка",
    "LOUNGE": "зал отдыха",
}

sport_club_labels["ru_loc"] = {
    "GYM": "тренажёрном зале",
    "POOL": "бассейне",
    "SAUNA": "сауне",
    "COURT": "спортивной площадке",
    "LOUNGE": "зале отдыха",
}

sport_club_labels["ru_gen"] = {
    "GYM": "тренажёрного зала",
    "POOL": "бассейна",
    "SAUNA": "сауны",
    "COURT": "спортивной площадки",
    "LOUNGE": "зала отдыха",
}

sport_club_representations = {
    "GYM": "💪",
    "POOL": "🏊",
    "SAUNA": "🧖",
    "COURT": "🏀",
    "LOUNGE": "🛋️",
}

sport_club_activities = {
    "GYM": [
        {"en": "heard a voice coming from the gym (💪)", "es": "escuché una voz que venía desde el gimnasio (💪)", "ru": "услышал(а) голос из тренажёрного зала (💪)"}
    ],
    "POOL": [
        {"en": "heard a voice coming from the swimming pool (🏊)", "es": "escuché una voz que venía desde la piscina (🏊)", "ru": "услышал(а) голос из бассейна (🏊)"}
    ],
    "SAUNA": [
        {"en": "heard a voice coming from the sauna (🧖)", "es": "escuché una voz que venía desde la sauna (🧖)", "ru": "услышал(а) голос из сауны (🧖)"}
    ],
    "COURT": [
        {"en": "heard a voice coming from the sports court (🏀)", "es": "escuché una voz que venía desde la cancha deportiva (🏀)", "ru": "услышал(а) голос со спортивной площадки (🏀)"}
    ],
    "LOUNGE": [
        {"en": "heard a voice coming from the lounge (🛋️)", "es": "escuché una voz que venía desde el salón (🛋️)", "ru": "услышал(а) голос из зала отдыха (🛋️)"}
    ]
}


abandoned_school_intro = {}
abandoned_school_intro["en"] = " are transported into <b>an abandoned school</b> at night!"
abandoned_school_intro["es"] = " han sido transportados a <b>una escuela abandonada</b> por la noche!"
abandoned_school_intro["ru"] = " перенеслись в <b>заброшенную школу</b> ночью!"

abandoned_school_labels = {}
abandoned_school_labels["en"] = {
    "ART CLASSROOM": "art classroom",
    "SCIENCE LAB": "science lab",
    "GYM": "gym",
    "LIBRARY": "library",
    "CAFETERIA": "cafeteria",
}

abandoned_school_labels["es"] = {
    "ART CLASSROOM": "el aula de arte",
    "SCIENCE LAB": "el laboratorio de ciencias",
    "GYM": "el gimnasio",
    "LIBRARY": "la biblioteca",
    "CAFETERIA": "la cafetería",
}

abandoned_school_labels["ru"] = {
    "ART CLASSROOM": "класс рисования",
    "SCIENCE LAB": "лаборатория",
    "GYM": "спортзал",
    "LIBRARY": "библиотека",
    "CAFETERIA": "столовая",
}

abandoned_school_labels["ru_loc"] = {
    "ART CLASSROOM": "классе рисования",
    "SCIENCE LAB": "лаборатории",
    "GYM": "спортзале",
    "LIBRARY": "библиотеке",
    "CAFETERIA": "столовой",
}

abandoned_school_labels["ru_gen"] = {
    "ART CLASSROOM": "класса рисования",
    "SCIENCE LAB": "лаборатории",
    "GYM": "спортзала",
    "LIBRARY": "библиотеки",
    "CAFETERIA": "столовой",
}

abandoned_school_representations = {
    "ART CLASSROOM": "🎨",
    "SCIENCE LAB": "🔬",
    "GYM": "💪",
    "LIBRARY": "📚",
    "CAFETERIA": "🍽️",
}

abandoned_school_activities = {
    "ART CLASSROOM": [
        {"en": "heard a voice coming from the art classroom (🎨)", "es": "escuché una voz que venía desde el aula de arte (🎨)", "ru": "услышал(а) голос из класса рисования (🎨)"}
    ],
    "SCIENCE LAB": [
        {"en": "heard a voice coming from the science lab (🔬)", "es": "escuché una voz que venía desde el laboratorio de ciencias (🔬)", "ru": "услышал(а) голос из лаборатории (🔬)"}
    ],
    "GYM": [
        {"en": "heard a voice coming from the gym (💪)", "es": "escuché una voz que venía desde el gimnasio (💪)", "ru": "услышал(а) голос из спортзала (💪)"}
    ],
    "LIBRARY": [
        {"en": "heard a voice coming from the library (📚)", "es": "escuché una voz que venía desde la biblioteca (📚)", "ru": "услышал(а) голос из библиотеки (📚)"}
    ],
    "CAFETERIA": [
        {"en": "heard a voice coming from the cafeteria (🍽️)", "es": "escuché una voz que venía desde la cafetería (🍽️)", "ru": "услышал(а) голос из столовой (🍽️)"}
    ],
}

def get_location_data(selected_location, mode):
    if selected_location is None:
        if mode == "latex":
            locations.remove("train")

        location_name = choice(locations)
    else:
        location_name = selected_location
    location_data = None

    if location_name == "mansion":
        location_data = (
            mansion_intro,
            mansions_labels,
            mansion_representations,
            mansion_activities,
        )
    elif location_name == "ship":
        location_data = (
            ship_intro,
            ship_labels,
            ship_representations,
            ship_activities,
        )
    elif location_name == "egypt":
        location_data = (
            egypt_intro,
            egypt_labels,
            egypt_representations,
            egypt_activities,
        )
    elif location_name == "castle":
        location_data = (
            medieval_castle_intro,
            medieval_castle_labels,
            medieval_castle_representations,
            medieval_castle_activities,
        )
    elif location_name == "train":
        location_data = (
            train_intro,
            train_labels,
            train_representations,
            train_activities,
        )
    elif location_name == "space station":
        location_data = (
            space_station_intro,
            space_station_labels,
            space_station_representations,
            space_station_activities,
        )
    elif location_name == "museum":
        location_data = (
            museum_intro,
            museum_labels,
            museum_representations,
            museum_activities,
        )
    elif location_name == "island":
        location_data = (
            island_intro,
            island_labels,
            island_representations,
            island_activities,
        )
    elif location_name == "zoo":
        location_data = (
            zoo_intro,
            zoo_labels,
            zoo_representations,
            zoo_activities,
        )
    elif location_name == "hospital":
        location_data = (
            hospital_intro,
            hospital_labels,
            hospital_representations,
            hospital_activities,
        )
    elif location_name == "sport club":
        location_data = (
            sport_club_intro,
            sport_club_labels,
            sport_club_representations,
            sport_club_activities,
        )
    elif location_name == "abandoned school":
        location_data = (
            abandoned_school_intro,
            abandoned_school_labels,
            abandoned_school_representations,
            abandoned_school_activities,
        )
    else:
        raise ValueError("Unknown location name: " + location_name)

    return (location_name, location_data)


class Locations:
    """
    A class representing locations in a mystery game.

    Attributes:
    - graph: The graph representing the connections between locations.
    - map: A dictionary mapping generic node names to concrete location names.
    - indices: A dictionary mapping generic node names to concrete location indices.
    - names: A dictionary mapping generic node names to concrete location names.
    - representations: A dictionary mapping generic node names to concrete location representations.
    - weapons: A list of weapons available in the game.
    - weapon_locations: A dictionary mapping location names to weapons.
    """

    def __init__(self, mode, location_name, number_places, location_data, weapons):
        """
        Initializes a Locations object.

        Parameters:
        - number_places: The number of locations in the game.
        - location_data: A tuple containing:
            + intro: A short sentence to introduce the location.
            + names: A dictionary mapping concrete location names to generic node names.
            + representations: A dictionary mapping concrete location names to their representations.
        - weapons: A list of weapons available in the game.
        """
        self.mode = mode
        self.name = location_name
        intro, names, representations, activities = location_data
        self.intro = intro
        self.activities = activities
        self.number_places = number_places
        nodes = {}
        for n in range(number_places):
            nodes[n] = "ROOM" + str(n)

        self.map = nodes
        self.number_places = len(nodes)

        nodes_list = list(nodes.values())
        shuffle(nodes_list)
        names_list = list(names["en"].keys())

        self.names = names
        self.indices = {}
        # self.names = {}
        self.representations = {}

        if location_name == "train":
            self.indices["ROOM0"] = "LOCOMOTIVE"
            # self.names["ROOM0"] = names["LOCOMOTIVE"]
            self.representations["ROOM0"] = representations["LOCOMOTIVE"]

            names_list = [x for x in names_list if x != "LOCOMOTIVE"]
            nodes_list = [x for x in nodes_list if x != "ROOM0"]

        for generic, concrete in zip(nodes_list, names_list):
            self.indices[generic] = concrete
            # self.names[generic] = names[concrete]
            self.representations[generic] = representations[concrete]

        self.rindices = {v: k for k, v in self.indices.items()}
        self.weapons = weapons
        self.graph = self.create_locations_graph(nodes)
        self.weapon_locations = self.create_locations_weapons(weapons)

    def create_locations_graph(self, nodes):
        """
        Creates a graph representing the connections between locations.

        Parameters:
        - nodes: A dictionary mapping node indices to location names.

        Returns:
        - graph: The created graph.
        """
        keepGenerating = True

        while keepGenerating:
            if self.name == "train":
                graph = Graph()
                for n in range(self.number_places - 1):
                    graph.add_edge("ROOM" + str(n), "ROOM" + str(n + 1))
            else:
                graph = gnp_random_graph(self.number_places, 0.5)

            keepGenerating = not (is_planar(graph) and is_connected(graph))

        graph = relabel_nodes(graph, nodes)
        return graph

    def create_locations_weapons(self, weapons):
        """
        Creates a dictionary mapping location names to weapons.

        Parameters:
        - weapons: A list of weapons available in the game.

        Returns:
        - weapon_locations: The created dictionary.
        """
        weapon_locations = {}
        shuffled_weapons = list(weapons)
        shuffle(shuffled_weapons)

        for loc, weapon in zip(self.map.values(), shuffled_weapons):
            weapon_locations[loc] = weapon

        return weapon_locations

    def render_locations(self, outdir):
        for language in ["en", "es", "ru"]:
            if language in self.names:
                self.render_locations_language(language, outdir)

    def render_locations_language(self, language, outdir):
        """
        Renders the locations graph and saves it as images.

        Parameters:
        - outdir: The directory where the images will be saved.
        """
        names = {}
        for index, place in self.indices.items():
            names[index] = self.names[language][place]

        labels = {}
        for place, name in names.items():
            labels[place] = name + " " + self.representations[place]

        relabeled_graph = relabel_nodes(self.graph, labels)
        g = to_agraph(relabeled_graph)

        if g.number_of_nodes() > 3:
            pos = planar_layout(g)

            # Apply the planar layout to the PyGraphviz graph
            for node, (x, y) in pos.items():
                n = g.get_node(node)
                n.attr["pos"] = f"{x},{y}"

        g.graph_attr.update(bgcolor="transparent")
        g.node_attr.update(
            fontname="Raleway", color="lightblue2", style="filled", shape="Mrecord"
        )
        g.layout(prog="dot")
        g.edge_attr.update(color="gray")
        g.draw(outdir + f"/{language}/locations_big.svg")

        if self.mode == "latex":
            g.draw(outdir + f"/{language}/locations_big.pdf")

        g.graph_attr.update(dpi="200")
        if self.mode != "latex":
            g.draw(outdir + f"/{language}/locations_big.png")

        labels = {}
        for place, name in names.items():
            labels[place] = self.representations[place]

        relabeled_graph = relabel_nodes(self.graph, labels)
        g = to_agraph(relabeled_graph)

        if g.number_of_nodes() > 3:
            pos = planar_layout(g)

            # Apply the planar layout to the PyGraphviz graph
            for node, (x, y) in pos.items():
                n = g.get_node(node)
                n.attr["pos"] = f"{x},{y}"

        g.graph_attr.update(
            bgcolor="transparent", nodesep="0.1", ranksep="0.1", margin="0"
        )
        g.edge_attr.update(color="dimgrey", labeldistance="0.05")

        g.node_attr.update(
            fontname="Raleway", shape="plaintext", width="0.2", fixedsize="true"
        )

        if (self.mode == "latex"):
            if g.number_of_nodes() == 3:
                g.node_attr.update(fontsize="12")
            elif g.number_of_nodes() == 4:
                g.node_attr.update(fontsize="14")
            elif g.number_of_nodes() >= 5:
                g.node_attr.update(fontsize="16")

        g.layout(prog="dot")
        g.draw(outdir + f"/{language}/locations_small.svg")

        if self.mode == "latex":
            g.draw(outdir + f"/{language}/locations_small.pdf")

        g.graph_attr.update(dpi="200")

        if self.mode != "latex":
            g.draw(outdir + f"/{language}/locations_small.png")

    def get_activities(self):
        """
        Returns the activities associated with each location.

        Returns:
        - activities: A dictionary mapping location names to activities.
        """
        activities = {}
        for generic, concrete in self.indices.items():
            if concrete in self.activities:
                activities[generic] = self.activities[concrete]

        return activities

    def sort_locations(self):
        """
        Returns a list of generic labels sorted according to where they show in the graph.
        Sorting is by highest x (descending), then lowest y (ascending).
        """
        g = to_agraph(self.graph)
        g.layout(prog="dot")
        pos = {}
        for node in self.graph.nodes():
            gv_node = g.get_node(node)
            pos_str = gv_node.attr.get("pos")
            if pos_str:
                x, y = map(float, pos_str.split(","))
                pos[node] = (x, y)
        if not pos:
            return list(self.graph.nodes())
        sorted_locations = sorted(pos.items(), key=lambda item: (-item[1][1], item[1][0]))
        sorted_labels = [loc[0].lower() for loc in sorted_locations]
        return sorted_labels

class TutorialLocations(Locations):
    def __init__(self, location_data):
        self.name = "tutorial"
        _, names, representations, _ = location_data
        self.number_places = 4
        nodes = {}
        for n in range(self.number_places):
            nodes[n] = "ROOM" + str(n)

        self.map = nodes
        self.number_places = len(nodes)

        nodes_list = list(nodes.values())
        shuffle(nodes_list)

        self.names = names
        self.indices = {}
        # self.names = {}
        self.representations = {}

        self.indices["ROOM0"] = "KITCHEN"
        self.representations["ROOM0"] = representations["KITCHEN"]

        self.indices["ROOM1"] = "DINING"
        self.representations["ROOM1"] = representations["DINING"]

        self.indices["ROOM2"] = "BEDROOM"
        self.representations["ROOM2"] = representations["BEDROOM"]

        self.indices["ROOM3"] = "BATHROOM"
        self.representations["ROOM3"] = representations["BATHROOM"]

        self.rindices = {v: k for k, v in self.indices.items()}
        self.graph = self.create_locations_graph(nodes)

    def create_locations_graph(self, nodes):
        """
        Creates a graph representing the connections between locations.

        Parameters:
        - nodes: A dictionary mapping node indices to location names.

        Returns:
        - graph: The created graph.
        """
        graph = Graph()
        graph.add_edge("ROOM0", "ROOM1")
        graph.add_edge("ROOM0", "ROOM2")
        graph.add_edge("ROOM2", "ROOM3")
        graph = relabel_nodes(graph, nodes)
        return graph

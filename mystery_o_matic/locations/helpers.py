def make_ambient_activities(labels, representations):
    """
    Generate a generic, action-agnostic Heard-clue activity pool for every
    room in a location.

    Each room gets three entries (voice / footsteps / movement). Every entry
    names the room and its emoji so the witness's clue still conveys where
    the noise came from, but none of them commit to a specific action — that
    way they never contradict whatever the actor reports in their own
    StayedClue activity.
    """
    out = {}
    for key in labels["en"]:
        rep = representations[key]
        en_room = labels["en"][key]
        es_room = labels["es"][key]
        ru_loc = labels["ru_loc"][key]
        ru_gen = labels["ru_gen"][key]
        out[key] = [
            {"en": f"heard a voice coming from the {en_room} ({rep})",
             "es": f"escuché una voz que venía desde {es_room} ({rep})",
             "ru": f"услышал(а) голос из {ru_gen} ({rep})"},
            {"en": f"heard footsteps in the {en_room} ({rep})",
             "es": f"escuché pasos en {es_room} ({rep})",
             "ru": f"услышал(а) шаги в {ru_loc} ({rep})"},
            {"en": f"heard movement in the {en_room} ({rep})",
             "es": f"escuché movimiento en {es_room} ({rep})",
             "ru": f"услышал(а) движение в {ru_loc} ({rep})"},
            {"en": f"heard someone in the {en_room} ({rep})",
             "es": f"escuché a alguien en {es_room} ({rep})",
             "ru": f"услышал(а) кого-то в {ru_loc} ({rep})"},
        ]
    return out

from abc import ABC, abstractmethod


class LanguageRenderer(ABC):
    @property
    @abstractmethod
    def lang_code(self):
        pass

    # --- Statements ---

    @abstractmethod
    def render_murder_was_alone(self):
        pass

    @abstractmethod
    def render_murder_was_not_found_with_body(self):
        pass

    @abstractmethod
    def render_weapon_location(self, weapon, vplace):
        pass

    @abstractmethod
    def render_character_location(self, subject, place, victim):
        pass

    @abstractmethod
    def render_no_one_else(self):
        pass

    @abstractmethod
    def render_weapon_locations_intro(self):
        pass

    @abstractmethod
    def render_weapon_locations_outro(self):
        pass

    @abstractmethod
    def render_final_locations_intro(self, time):
        pass

    # --- Clues ---

    @abstractmethod
    def render_saw_when_arriving(self, subject, object, object_is_alive, place, time, foggy):
        pass

    @abstractmethod
    def render_not_saw(self, subject, object, place, time):
        pass

    @abstractmethod
    def render_saw_victim_when_arriving(self, subject, object, object_is_alive, place, time):
        pass

    @abstractmethod
    def render_saw_victim_when_leaving(self, subject, object, object_is_alive, place, time):
        pass

    @abstractmethod
    def render_saw_when_leaving(self, subject, object, object_is_alive, place, time, foggy):
        pass

    @abstractmethod
    def render_was_murdered_initial(self, subject, place, time_start, time_end):
        pass

    @abstractmethod
    def render_was_murdered_body_two_options(self, time1, time2):
        pass

    @abstractmethod
    def render_was_victim_dead_at(self, time, alternative):
        pass

    @abstractmethod
    def render_was_victim_alive_at(self, time, alternative):
        pass

    @abstractmethod
    def render_was_murdered_after(self, time, interval_size, positive, alternative):
        pass

    @abstractmethod
    def render_was_murdered_before(self, time, interval_size, positive, alternative):
        pass

    @abstractmethod
    def render_was_murdered_scream(self, time1, time2):
        pass

    @abstractmethod
    def render_evidence(self, subject, place):
        pass

    @abstractmethod
    def render_stayed(self, subject, place, time_start, time_end):
        pass

    @abstractmethod
    def render_interacted(self, subject0, subject1, place):
        pass

    @abstractmethod
    def render_heard(self, subject, activity_text, time):
        pass

    @abstractmethod
    def render_weapon_not_used(self, weapon):
        pass

    # --- Solution steps (shown via "Peek under the curtain") ---

    @abstractmethod
    def render_solution_initial_header(self, time):
        pass

    @abstractmethod
    def render_solution_events_header(self):
        pass

    @abstractmethod
    def render_solution_initial_item(self, subject, place):
        pass

    @abstractmethod
    def render_solution_takes_weapon(self, subject, weapon, place):
        pass

    @abstractmethod
    def render_solution_move(self, subject, from_place, to_place):
        pass

    @abstractmethod
    def render_solution_kills(self, killer, victim, weapon, place):
        pass


_RENDERERS = {}


def register_renderer(renderer):
    _RENDERERS[renderer.lang_code] = renderer


def get_renderer(lang_code):
    return _RENDERERS[lang_code]


def get_all_renderers():
    return _RENDERERS

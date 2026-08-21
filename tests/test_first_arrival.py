from unittest.mock import patch

import pytest

from mystery_o_matic.clues import FirstArrivalClue, create_clue
from mystery_o_matic.lang.en import EnglishRenderer
from mystery_o_matic.lang.es import SpanishRenderer
from mystery_o_matic.lang.ru import RussianRenderer
from mystery_o_matic.time import Time


@pytest.mark.parametrize(
    ("renderer", "randint_path", "expected"),
    [
        (
            EnglishRenderer(),
            "mystery_o_matic.lang.en.randint",
            [
                '$CHAR1: "I didn\'t arrive at the $ROOM2 until 3:00"',
                '$CHAR1: "The first time I entered the $ROOM2 was at 3:00"',
            ],
        ),
        (
            SpanishRenderer(),
            "mystery_o_matic.lang.es.randint",
            [
                '$CHAR1: "No llegué a estar en $ROOM2 hasta las 3:00"',
                '$CHAR1: "La primera vez que entré en $ROOM2 fue a las 3:00"',
            ],
        ),
        (
            RussianRenderer(),
            "mystery_o_matic.lang.ru.randint",
            [
                '$CHAR1: "Я добрался(ась) до $ROOM2_GEN только в 3:00"',
                '$CHAR1: "Впервые я оказался(ась) в $ROOM2_LOC в 3:00"',
            ],
        ),
    ],
)
def test_first_arrival_has_two_rendering_alternatives(
    renderer, randint_path, expected
):
    clue = FirstArrivalClue("$CHAR1", "$ROOM2", Time("3:00"))

    for alternative, text in enumerate(expected):
        with patch(randint_path, return_value=alternative):
            assert clue.render(renderer) == text


def test_create_first_arrival_clue():
    clue = create_clue(
        ["FirstArrival", "$CHAR1", "$ROOM2", Time("3:00")]
    )

    assert isinstance(clue, FirstArrivalClue)
    assert clue.subject == "$CHAR1"
    assert clue.place == "$ROOM2"
    assert clue.time.seconds == Time("3:00").seconds


def test_first_arrival_is_incriminating_at_crime_scene_before_murder():
    clue = FirstArrivalClue("$CHAR1", "$ROOM2", Time("3:00"))

    assert clue.is_incriminating(
        "$CHAR1", "$CHAR2", "$ROOM2", Time("3:15")
    )
    assert not clue.is_incriminating(
        "$CHAR1", "$CHAR2", "$ROOM2", Time("2:45")
    )
    assert not clue.is_incriminating(
        "$CHAR1", "$CHAR2", "$ROOM3", Time("3:15")
    )


def test_first_arrival_lie_moves_arrival_to_alibi():
    clue = FirstArrivalClue("$CHAR1", "$ROOM2", Time("3:00"))

    assert clue.manipulate(
        "$CHAR1", "$CHAR2", "$ROOM3"
    ) is clue
    assert clue.place == "$ROOM3"

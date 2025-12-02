import uuid

import pytest

from models.game import Coordinate, Game


def test_game_state_updates_correctly():
    game = Game(player_id=str(uuid.uuid4()))
    game.add_move(Coordinate(x=1, y=1))  # X
    game.add_move(Coordinate(x=0, y=2))  # O

    assert game.game_state == [
        [".", ".", "."],
        [".", "X", "."],
        ["O", ".", "."],
    ]


def test_add_move_rejects_occupied_spot():
    game = Game(player_id=str(uuid.uuid4()))
    game.add_move(Coordinate(x=1, y=1))

    with pytest.raises(Exception):
        game.add_move(Coordinate(x=1, y=1))  # same spot again


def test_available_spots_decreases_after_moves():
    game = Game(player_id=str(uuid.uuid4()))
    before = len(game.available_spots)

    game.add_move(Coordinate(x=0, y=0))
    after = len(game.available_spots)

    assert after == before - 1
    assert Coordinate(x=0, y=0) not in game.available_spots


def test_add_random_move_places_something(monkeypatch):
    # force deterministic random spot
    # honestly just kinda looking for an excuse to monkey-patch some stuff so I can showcase I understand the concept, lol
    monkeypatch.setattr("models.game.random.choice", lambda spots: Coordinate(x=2, y=2))

    game = Game(player_id="p1")
    game.add_random_move()

    assert game.game_state[2][2] != "."

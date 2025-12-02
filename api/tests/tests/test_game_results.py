import uuid

from models.game import Coordinate, Game


def test_game_result_ongoing_empty_board():
    game = Game(player_id=str(uuid.uuid4()), human_plays_as="X", moves=[])
    assert game.game_result == "ongoing"


def test_game_result_ongoing_partial_board():
    # X at (0,0), O at (1,0), X at (2,2)
    game = Game(
        player_id=str(uuid.uuid4()),
        human_plays_as="O",
        moves=[
            Coordinate(x=0, y=0),  # X
            Coordinate(x=1, y=0),  # O
            Coordinate(x=2, y=2),  # X
        ],
    )
    assert game.game_result == "ongoing"


# Drawn final board:
# X O X
# X O O
# O X X
DRAW_MOVES = [
    Coordinate(x=0, y=0),  # X
    Coordinate(x=1, y=0),  # O
    Coordinate(x=2, y=0),  # X
    Coordinate(x=1, y=1),  # O
    Coordinate(x=0, y=1),  # X
    Coordinate(x=2, y=1),  # O
    Coordinate(x=1, y=2),  # X
    Coordinate(x=0, y=2),  # O
    Coordinate(x=2, y=2),  # X
]


def test_game_result_draw_human_as_x():
    game = Game(player_id=str(uuid.uuid4()), human_plays_as="X", moves=DRAW_MOVES)
    assert game.game_result == "draw"


def test_game_result_draw_human_as_o():
    game = Game(player_id=str(uuid.uuid4()), human_plays_as="O", moves=DRAW_MOVES)
    assert game.game_result == "draw"


# Row win for X (top row):
# X X X
# O . .
# . O .
ROW_X_WIN_MOVES = [
    Coordinate(x=0, y=0),  # X
    Coordinate(x=0, y=1),  # O
    Coordinate(x=1, y=0),  # X
    Coordinate(x=1, y=1),  # O
    Coordinate(x=2, y=0),  # X
]


def test_game_result_cpu_wins_row_with_x():
    game = Game(player_id=str(uuid.uuid4()), human_plays_as="O", moves=ROW_X_WIN_MOVES)
    assert game.game_result == "CPU won"


def test_game_result_human_wins_row_with_x():
    game = Game(player_id=str(uuid.uuid4()), human_plays_as="X", moves=ROW_X_WIN_MOVES)
    assert game.game_result == "human won"


# Column win for O (middle column):
# X O .
# X O .
# . O X
COLUMN_O_WIN_MOVES = [
    Coordinate(x=0, y=0),  # X
    Coordinate(x=1, y=0),  # O
    Coordinate(x=0, y=1),  # X
    Coordinate(x=1, y=1),  # O
    Coordinate(x=2, y=2),  # X
    Coordinate(x=1, y=2),  # O
]


def test_game_result_cpu_wins_column_with_o():
    game = Game(
        player_id=str(uuid.uuid4()), human_plays_as="X", moves=COLUMN_O_WIN_MOVES
    )
    assert game.game_result == "CPU won"


def test_game_result_human_wins_column_with_o():
    game = Game(
        player_id=str(uuid.uuid4()), human_plays_as="O", moves=COLUMN_O_WIN_MOVES
    )
    assert game.game_result == "human won"


# Diagonal 1 win for X:
# X . .
# . X .
# . . X
DIAG_MAIN_X_WIN_MOVES = [
    Coordinate(x=0, y=0),  # X
    Coordinate(x=0, y=1),  # O
    Coordinate(x=1, y=1),  # X
    Coordinate(x=1, y=0),  # O
    Coordinate(x=2, y=2),  # X
]


def test_game_result_cpu_wins_main_diagonal_with_x():
    game = Game(
        player_id=str(uuid.uuid4()), human_plays_as="O", moves=DIAG_MAIN_X_WIN_MOVES
    )
    assert game.game_result == "CPU won"


def test_game_result_human_wins_main_diagonal_with_x():
    game = Game(
        player_id=str(uuid.uuid4()), human_plays_as="X", moves=DIAG_MAIN_X_WIN_MOVES
    )
    assert game.game_result == "human won"


# Diagonal 2 win for O:
# X . O
# . O .
# O . X
DIAG_ANTI_O_WIN_MOVES = [
    Coordinate(x=0, y=0),  # X
    Coordinate(x=2, y=0),  # O
    Coordinate(x=0, y=1),  # X
    Coordinate(x=1, y=1),  # O
    Coordinate(x=2, y=2),  # X
    Coordinate(x=0, y=2),  # O
]


def test_game_result_cpu_wins_anti_diagonal_with_o():
    game = Game(
        player_id=str(uuid.uuid4()), human_plays_as="X", moves=DIAG_ANTI_O_WIN_MOVES
    )
    assert game.game_result == "CPU won"


def test_game_result_human_wins_anti_diagonal_with_o():
    game = Game(
        player_id=str(uuid.uuid4()), human_plays_as="O", moves=DIAG_ANTI_O_WIN_MOVES
    )
    assert game.game_result == "human won"

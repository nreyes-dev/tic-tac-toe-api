import copy
import random
import uuid
from typing import List, Literal, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field, computed_field

DEFAULT_GAME_STATE = [
    [".", ".", "."],
    [".", ".", "."],
    [".", ".", "."],
]


class Coordinate(BaseModel):
    """
    Represents a single spot in the tic tac toe board.
    Uses 0-based indexing as suggested by the original challenge's description.
    """

    x: int = Field(ge=0, le=2)
    y: int = Field(ge=0, le=2)


class Game(BaseModel):
    """
    A Game of tic tac toe, represented by "X"s, "O"s and "."s,
    as suggested by the original challenge's description.
    The dots represent empty spots, while "X"s are crosses and "O"s are circles.
    Crosses always play first, circles second.
    The current game state can be constructed from the list of moves that were made.
    """

    game_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    player_id: str
    human_plays_as: Literal["X", "O"] = Field(
        default_factory=lambda: random.choice(["X", "O"])
    )
    moves: List[Coordinate] = Field(
        default=[]
    )  # because the first move is always a cross, this is enough to fully understand the game state

    @computed_field
    @property
    def game_state(self) -> List[List[str]]:
        """
        Return the current game state.

        Because crosses ("X") always go first, move parity determines the symbol:
        - Even index (0, 2, 4, ...): "X"
        - Odd index  (1, 3, 5, ...): "O"
        """
        game_state = copy.deepcopy(
            DEFAULT_GAME_STATE
        )  # need to deepcopy because of the nested lists

        for i, move in enumerate(self.moves):
            symbol = "X" if i % 2 == 0 else "O"
            game_state[move.y][move.x] = symbol

        return game_state

    @computed_field
    @property
    def available_spots(self) -> List[Coordinate]:
        game_state = self.game_state
        return [
            Coordinate(x=x, y=y)
            for y in range(3)
            for x in range(3)
            if game_state[y][x] == "."
        ]

    @computed_field
    @property
    def game_result(self) -> Literal["ongoing", "human won", "CPU won", "draw"]:
        game_state = self.game_state

        winner_symbol: Optional[str] = None

        # is there a winning row?
        for row in game_state:
            if row == ["X", "X", "X"]:
                winner_symbol = "X"
                break
            if row == ["O", "O", "O"]:
                winner_symbol = "O"
                break

        # is there a winning column?
        if winner_symbol is None:
            columns = [
                [game_state[0][0], game_state[1][0], game_state[2][0]],
                [game_state[0][1], game_state[1][1], game_state[2][1]],
                [game_state[0][2], game_state[1][2], game_state[2][2]],
            ]
            for col in columns:
                if col == ["X", "X", "X"]:
                    winner_symbol = "X"
                    break
                if col == ["O", "O", "O"]:
                    winner_symbol = "O"
                    break

        # is there a winning diagonal?
        if winner_symbol is None:
            diagonals = [
                [game_state[0][0], game_state[1][1], game_state[2][2]],
                [game_state[0][2], game_state[1][1], game_state[2][0]],
            ]
            for diag in diagonals:
                if diag == ["X", "X", "X"]:
                    winner_symbol = "X"
                    break
                if diag == ["O", "O", "O"]:
                    winner_symbol = "O"
                    break

        if winner_symbol is not None:
            if winner_symbol == self.human_plays_as:
                return "human won"
            return "CPU won"

        if len(self.available_spots) > 0:
            return "ongoing"

        return "draw"

    def add_move(self, move: Coordinate) -> None:
        if move in self.moves:
            raise HTTPException(
                status_code=400, detail=f"Spot ({move.x}, {move.y}) is already taken."
            )
        self.moves.append(move)

    def add_random_move(self) -> None:
        """
        Used for the random CPU moves
        """
        available_spots = self.available_spots
        if not available_spots:
            raise HTTPException(
                status_code=500,
                detail="Can't choose a random move because the game is over",
            )

        random_move = random.choice(available_spots)
        self.add_move(random_move)

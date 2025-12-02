import logging
import uuid

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse, Response

import redis_client
from models.game import Coordinate, Game

router = APIRouter()


def get_player_id(
    response: Response,
    x_player_id: str | None = Header(default=None, alias="X-Player-Id"),
) -> str:
    if x_player_id is None:
        x_player_id = str(uuid.uuid4())
        # Let the client know what to use from now on
        response.headers["X-Player-Id"] = x_player_id
    return x_player_id


@router.post("/game")
async def new_game(player_id: str = Depends(get_player_id)):
    try:
        game = Game(
            player_id=player_id,
        )
        if game.human_plays_as == "O":
            # the cpu makes the first move
            game.add_random_move()

        # store game
        await redis_client.write(
            key=f"game:{game.game_id}",
            value=game.model_dump(
                # don't store computed fields
                exclude={"game_state", "available_spots", "game_result"}
            ),
        )
        # store pointer to game in player history
        await redis_client.zadd(f"player:{player_id}:games", game.game_id)

        return JSONResponse(
            content=game.model_dump(),
            status_code=status.HTTP_201_CREATED,
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Internal Server Error: {e}", exc_info=True)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/game/{game_id}/move")
async def make_a_move(
    game_id: str, body: Coordinate, player_id: str = Depends(get_player_id)
):
    try:
        # retrieve game and validate that the caller owns it and that the game didn't end yet
        stored_game = await redis_client.read(f"game:{game_id}")
        if stored_game is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found.",
            )
        game = Game(**stored_game)
        if game.player_id != player_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This game belongs to a different player.",
            )
        if game.game_result != "ongoing":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This game has already ended.",
            )

        # make the move
        game.add_move(body)

        # if the game is still ongoing, the CPU responds
        if game.game_result != "ongoing":
            game.add_random_move()

        # update game store
        await redis_client.write(
            key=f"game:{game.game_id}",
            value=game.model_dump(
                # don't store computed fields
                exclude={"game_state", "available_spots", "game_result"}
            ),
        )

        return JSONResponse(
            content=game.model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Internal Server Error: {e}", exc_info=True)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/game/{game_id}/history")
async def get_game_history(game_id: str):
    # TODO
    try:
        return Response(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Internal Server Error: {e}", exc_info=True)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/game/history")
async def get_all_games_history():
    # TODO
    try:
        return Response(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Internal Server Error: {e}", exc_info=True)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

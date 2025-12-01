import logging
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, Response

router = APIRouter()

@router.get("/hello")
async def get_hello():
    try:
        return JSONResponse(
            content={"message": "hello world"},
            status_code=status.HTTP_200_OK,
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Internal Server Error: {e}", exc_info=True)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

from fastapi import APIRouter

from src.services.decorators import time_of_function, error_handler
from src.services.logger import get_logger

logger = get_logger()

router = APIRouter()


@router.get(path="/")
@error_handler
@time_of_function
async def get_main():
    logger.info("Get main")
    return {"status": 200}

import functools
import inspect
import logging
import sys
import time

from fastapi import HTTPException

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream=sys.stdout, format=Log_Format, level=logging.INFO)
logger = logging.getLogger()


def time_of_function(function):
    if inspect.iscoroutinefunction(function):

        @functools.wraps(function)
        async def wrap_func(*args, **kwargs):
            start_time = time.time()
            res = await function(*args, **kwargs)
            logger.info(
                f"Func {function.__name__} lead time {round(time.time() - start_time, 2)} seconds"
            )
            return res

    else:

        @functools.wraps(function)
        def wrap_func(*args, **kwargs):
            start_time = time.time()
            res = function(*args, **kwargs)
            logger.info(
                f"Func {function.__name__} lead time {round(time.time() - start_time, 2)} seconds"
            )
            return res

    return wrap_func


def error_handler(function):
    @functools.wraps(function)
    async def wrap_func(*args, **kwargs):
        try:
            res = await function(*args, **kwargs)
        except HTTPException as e:
            raise HTTPException(
                status_code=e.__dict__.get("status_code"),
                detail=e.__dict__.get("detail"),
            )
        except Exception as e:
            logger.error(f"Func {function.__name__} error: {e}")
            raise HTTPException(status_code=400, detail=f"Session error, Error: {e}")
        return res

    return wrap_func


import logging

import coloredlogs
import uvicorn

from config import settings

is_dev_env = settings.python_env == "development"

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

logging_level = LOG_LEVELS.get(settings.logging_lvl.lower(), logging.INFO)
if settings.logging_lvl.lower() not in LOG_LEVELS:
    logging.warning(
        'Unrecognized LOGGING_LVL "%s", defaulting to INFO',
        settings.logging_lvl,
    )

logging.basicConfig(
    level=logging_level,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
coloredlogs.install(level=logging_level)


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=is_dev_env,
        log_level=settings.logging_lvl.lower(),
    )

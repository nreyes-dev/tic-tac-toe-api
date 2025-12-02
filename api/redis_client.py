import json
import logging
import time
from typing import Any, List, Optional

import redis.asyncio as redis

DEFAULT_TTL = 86400  # 24hs

client = redis.Redis(host="redis", port=6379, db=0)


async def read(key: str) -> Optional[Any]:
    """Get a JSON-decoded value from Redis, or None."""
    try:
        value = await client.get(key)
        if value is None:
            return None
        return json.loads(value)
    except Exception as e:
        logging.error(f"Redis get error for key '{key}': {e}", exc_info=True)
        return None


async def write(key: str, value: Any, ttl: int = DEFAULT_TTL) -> None:
    """Set a JSON-encoded value in Redis with a TTL."""
    try:
        await client.setex(key, ttl, json.dumps(value))
    except Exception as e:
        logging.error(f"Redis set error for key '{key}': {e}", exc_info=True)


async def zadd(key: str, member: str, score: Optional[int] = None) -> None:
    """
    Add a member to a sorted set with an optional score.
    If no score is given, use the current Unix timestamp.
    """
    try:
        if score is None:
            score = int(time.time())
        await client.zadd(key, {member: score})
    except Exception as e:
        logging.error(f"Redis ZADD error for key '{key}': {e}", exc_info=True)


async def zrange(key: str, start: int = 0, end: int = -1) -> List[str]:
    """
    Return all members from a sorted set, in ascending order.
    """
    try:
        result = await client.zrange(key, start, end)
        return [member.decode("utf-8") for member in result]
    except Exception as e:
        logging.error(f"Redis ZRANGE error for key '{key}': {e}", exc_info=True)
        return []

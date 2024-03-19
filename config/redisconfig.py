import os

from redis import Redis

redis = Redis(
    host=os.environ.get("REDIS_HOST") or "localhost",
    port=6379,
    db=0,
    decode_responses=True
)



from uuid import uuid4
from datetime import datetime, timedelta
import redis
from redis.client import Redis
client = Redis(connection_pool=redis.BlockingConnectionPool())


ACCESS_TOKEN_EXPIRE_MINUTES = 30
r = redis.Redis(host='localhost', port=6379)


def create_session(user_id: str):
    session_id = str(uuid4())
    expiry_time = ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000
    r.hmset(session_id, {"user_id": user_id})
    r.pexpire(session_id, expiry_time)
    return session_id


def delete_session(session_id: str):
    r.delete(session_id)


def update_session_expiry(session_id: str) -> bool:
    """Returns True if session exists and is 
    sucessfully updated False if session isn't found."""

    expiry_time = ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000

    if r.exists(session_id) == 1:
        r.pexpire(session_id, expiry_time)
        return True
    return False

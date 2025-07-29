"""
Memory state implementation
"""

from datetime import datetime, timezone
from inspect import _empty

from mr.states.interface import IState


class MemoryState(IState):
    """
    State that use hash table to save cached returns
    """

    _state: dict[str, any]
    _kwargs: dict[str, any]

    __slots__ = ("_state", "_kwargs")

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._state = {}

    def sync_get(self, key: str):
        now_timestamp = datetime.now(timezone.utc).timestamp()
        if register := self._state.get(key):
            _ttl = register.get("ttl")
            if _ttl == _empty or ((register.get("created_at") + _ttl) >= now_timestamp):
                return register.get("value")
        return None

    def sync_set(self, key: str, value: any, ttl: int = _empty):
        value = {
            "created_at": datetime.now(timezone.utc).timestamp(),
            "ttl": ttl,
            "value": value,
        }
        self._state.update({key: value})

    def sync_unset(self, key: str):
        if key in self._state:
            del self._state[key]
        return None

    async def async_get(self, key: str):
        return self.sync_get(key)

    async def async_set(self, key: str, value: any, ttl: int = _empty):
        return self.sync_set(key=key, value=value, ttl=ttl)

    async def async_unset(self, key: str):
        return self.sync_unset(key)

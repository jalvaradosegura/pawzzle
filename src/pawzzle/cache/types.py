from typing import Any, Protocol


class Cache(Protocol):
    def __contains__(self, item: str) -> bool: ...

    def get(self, key: str) -> Any: ...

    def set(self, key: str, value: Any, expiration: int) -> None: ...

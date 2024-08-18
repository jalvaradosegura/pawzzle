from typing import Any

import valkey


class ValkeyCache:
    def __init__(self, url: str):
        self.valkey = valkey.from_url(url)  # type: ignore

    @classmethod
    def from_url(cls, url: str) -> "ValkeyCache":
        return cls(url)

    def __contains__(self, item: str) -> bool:
        return item in self.valkey

    def get(self, key: str) -> Any:
        return self.valkey.get(key)

    def set(self, key: str, value: Any, expiration: int) -> None:
        self.valkey.set(key, value, expiration)

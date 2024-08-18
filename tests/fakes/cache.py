from typing import Any


class CacheFake:
    def __init__(self):
        self.data: dict[str, Any] = {}

    def __contains__(self, item: str) -> bool:
        return item in self.data

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def set(self, key: str, value: Any, expiration: int) -> None:
        self.data[key] = value

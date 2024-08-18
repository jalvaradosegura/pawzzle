from typing import Any
from unittest.mock import MagicMock, patch


from pawzzle.cache.valkey_cache import ValkeyCache


@patch("pawzzle.cache.valkey_cache.valkey.from_url")
def test_valkey_cache_init(mocked_valkey_from_url: MagicMock):
    mocked_valkey_from_url.return_value = {}
    valkey_cache = ValkeyCache.from_url("dummy-url")
    assert isinstance(valkey_cache, ValkeyCache)


@patch("pawzzle.cache.valkey_cache.valkey.from_url")
def test_valkey_cache_contains(mocked_valkey_from_url: MagicMock):
    mocked_valkey_from_url.return_value = {}
    valkey_cache = ValkeyCache.from_url("dummy-url")

    valkey_cache.valkey["name"] = "Jon"

    assert ("data" in valkey_cache) is False
    assert ("name" in valkey_cache) is True


@patch("pawzzle.cache.valkey_cache.valkey.from_url")
def test_valkey_cache_set(mocked_valkey_from_url: MagicMock):
    class FakeValkeyCache:
        def __init__(self):
            self.data: dict[str, Any] = {}

        def __contains__(self, item: str) -> bool:
            return item in self.data

        def set(self, key: str, value: Any, expiration: int) -> None:
            self.data[key] = value

    mocked_valkey_from_url.return_value = FakeValkeyCache()
    valkey_cache = ValkeyCache.from_url("dummy-url")

    valkey_cache.set("name", "Jon", 60)

    assert ("name" in valkey_cache) is True


@patch("pawzzle.cache.valkey_cache.valkey.from_url")
def test_valkey_cache_get(mocked_valkey_from_url: MagicMock):
    class FakeValkeyCache:
        def __init__(self):
            self.data: dict[str, Any] = {}

        def __contains__(self, item: str) -> bool:
            return item in self.data

        def set(self, key: str, value: Any, expiration: int) -> None:
            self.data[key] = value

        def get(self, key: str) -> Any:
            return self.data[key]

    mocked_valkey_from_url.return_value = FakeValkeyCache()
    valkey_cache = ValkeyCache.from_url("dummy-url")
    valkey_cache.set("name", "Jon", 60)

    result = valkey_cache.get("name")

    assert result == "Jon"

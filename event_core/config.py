import os
from typing import (
    Any,
    Callable,
    Dict,
    TypeAlias,
    TypeVar,
    overload,
)

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


T = TypeVar("T")
ConfigT: TypeAlias = Dict[str, Any]


@overload
def _get_env_var(key: str) -> str: ...


@overload
def _get_env_var(key: str, converter: Callable[[str], T]) -> T: ...


def _get_env_var(key, converter=None):
    if val := os.environ.get(key):
        return converter(val) if converter else val
    raise KeyError(f"Env variable {key} required")


def _get_redis_connection_params() -> ConfigT:
    return {
        "host": _get_env_var("REDIS_HOST"),
        "port": _get_env_var("REDIS_PORT"),
        "username": _get_env_var("REDIS_USERNAME"),
        "password": _get_env_var("REDIS_PASSWORD"),
        "decode_responses": True,
    }


def get_redis_pubsub_connection_params() -> ConfigT:
    return _get_redis_connection_params()


def get_redis_mapping_connection_params() -> ConfigT:
    return _get_redis_connection_params()


def _get_api_url(key: str) -> str:
    return _get_env_var(key).rstrip("/") + "/"


def get_embedding_service_api_url() -> str:
    return _get_api_url("EMBEDDING_SERVICE_API_URL")


def get_storage_service_api_url() -> str:
    return _get_api_url("STORAGE_SERVICE_API_URL")

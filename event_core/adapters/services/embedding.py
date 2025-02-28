import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Union
from urllib.parse import urljoin

import requests

from event_core.config import get_embedding_service_api_url

logger = logging.getLogger(__name__)


class EmbeddingClient(ABC):

    @abstractmethod
    def query_text(
        self, user: str, text: str, n_cands: int, n_rank: int
    ) -> List[str]:
        raise NotImplementedError


class EmbeddingAPIClient(EmbeddingClient):

    def __init__(self):
        self._api_url = get_embedding_service_api_url()

    def query_text(
        self, user: str, text: str, n_cands: int, n_rank: int
    ) -> List[str]:
        logger.info(f'Querying text="{text}" in {user} namespace')
        params: Dict[str, Union[str, int]] = {
            "user": user,
            "text": text,
            "n_cands": n_cands,
            "n_rank": n_rank,
        }
        res = requests.get(urljoin(self._api_url, "query/text"), params)
        keys: List[str] = res.json()
        return keys

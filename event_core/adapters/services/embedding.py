import logging
from abc import ABC, abstractmethod
from typing import Dict, List, TypeAlias, Union
from urllib.parse import urljoin

import requests

from ...config import get_embedding_service_api_url
from .types import JsonT

logger = logging.getLogger(__name__)

DocT: TypeAlias = Dict[str, JsonT]
ModalT: TypeAlias = str


class EmbeddingClient(ABC):
    """
    ABC for interacting with Embedding Service via a client.
    This class defines the interface for Embedding Service 
    clients. Currently, only API client is implemented.

    Only the `query_text()` method is required to be implemented.
    Client has no knowledge of the retrieval procedure, which is
    determined internally within the Embedding Service.
    """

    @abstractmethod
    def query_text(
        self, user: str, text: str, top_n: int, **kwargs
    ) -> Dict[ModalT, List[DocT]]:
        """
        Given a text query made by a user, fetch the top_n most 
        relevant documents.

        Args:
            user (str):
                User making the request. Used in generating the
                corresponding namesapce for vector database queries
            text (str):
                Query text
            top_n (int):
                Specify number of top most relevant documents
            **kwargs:
                Additional optional query params

        Returns:
            Dict[str, List[DocT]]:
                Dict where keys are `event_core.domain.types.Modal`
                enum values, and values are list of document objects 
                for the corresponding modal.
        """
        raise NotImplementedError


class EmbeddingAPIClient(EmbeddingClient):
    """API client for interacting with Embedding Service"""

    def __init__(self):
        self._api_url = get_embedding_service_api_url()

    def _get_endpoint(self, endpoint: str) -> str:
        endpoint = endpoint.strip("/")
        return urljoin(self._api_url, endpoint)

    def query_text(
        self, user: str, text: str, top_n: int, **kwargs
    ) -> Dict[ModalT, List[DocT]]:
        logger.info(f"Query {text=} by {user=}")
        params: Dict[str, Union[str, int]] = {
            "user": user,
            "text": text,
            "top_n": top_n,
            **kwargs,
        }
        get_endpoint = self._get_endpoint("query/text")
        res = requests.get(get_endpoint, params)
        keys: Dict[ModalT, List[DocT]] = res.json()
        return keys

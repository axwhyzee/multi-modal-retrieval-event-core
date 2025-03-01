import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, TypeAlias, Union
from urllib.parse import urljoin

import requests
from pydantic import BaseModel, StrictStr, field_validator

from ...config import get_embedding_service_api_url
from ...domain.types import FileExt, Modal

logger = logging.getLogger(__name__)

ModalT: TypeAlias = StrictStr
DocKeysT: TypeAlias = List[str]


class QueryResponse(BaseModel):
    modals: Dict[ModalT, DocKeysT]

    @field_validator("modals")
    def validate_modals(
        cls, v: Dict[ModalT, DocKeysT]
    ) -> Dict[ModalT, DocKeysT]:
        for modal in Modal:
            # validate modals
            if modal.value not in v:
                raise ValueError(
                    f"Missing {modal=} All modals must be "
                    f"provided even if there are no docs"
                )
            # validate object keys
            for key in v[modal.value]:
                suffix = Path(key).suffix
                if suffix == "":
                    raise ValueError(f"doc_key {key} has no file ext")
                if suffix not in FileExt._value2member_map_:
                    raise ValueError(
                        f"Unsupported file ext {suffix}. Consider: "
                        f"{list(FileExt._value2member_map_.keys())}"
                    )
        return v


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
    ) -> QueryResponse:
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

    def _build_endpoint(self, endpoint: str) -> str:
        endpoint = endpoint.strip("/")
        return urljoin(self._api_url, endpoint)

    def query_text(
        self, user: str, text: str, top_n: int, **kwargs
    ) -> QueryResponse:
        logger.info(f"Query {text=} by {user=}")
        params: Dict[str, Union[str, int]] = {
            "user": user,
            "text": text,
            "top_n": top_n,
            **kwargs,
        }
        get_endpoint = self._build_endpoint("query/text")
        res = requests.get(get_endpoint, params)
        return QueryResponse(modals=res.json())

import logging
from typing import Dict, List, Union
from urllib.parse import urljoin

import requests

from event_core.config import get_embedding_service_api_url

logger = logging.getLogger(__name__)

API_URL = get_embedding_service_api_url()


def query_text(user: str, text: str, n_cands: int, n_rank: int) -> List[str]:
    logger.info(f'Querying text="{text}" in {user} namespace')
    params: Dict[str, Union[int, str]] = {
        "user": user,
        "text": text,
        "n_cands": n_cands,
        "n_rank": n_rank,
    }
    res = requests.get(urljoin(API_URL, "query/text"), params=params)
    keys: List[str] = res.json()
    return keys

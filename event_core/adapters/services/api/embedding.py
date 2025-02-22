import logging
from typing import Dict, List
from urllib.parse import urljoin

import requests

from event_core.config import get_embedding_service_api_url

logger = logging.getLogger(__name__)

API_URL = get_embedding_service_api_url()


def query_text(user: str, text: str) -> Dict[str, List[str]]:
    logger.info(f'Querying text="{text}" in {user} namespace')
    res = requests.get(
        urljoin(API_URL, "query/text"), params={"user": user, "text": text}
    )
    return res.json()

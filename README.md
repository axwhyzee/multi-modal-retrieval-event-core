# Event Core
The multi-modal retrieval system is event driven, and at its core, there is the <b>Storage Service</b>, <b>Event Broker</b> and <b>Meta Service</b>
Since all services are coupled with the global event schemas, `event-core` package serves to coordinate changes made to the core event schemas, pubsub clients, as well as storage and embedding service clients, reducing boilerplate code.

## Installation
pip install git+https://github.com/axwhyzee/multi-modal-retrieval-event-core.git

## Setup
If event pubsub will be used, ensure the following env vars are defined:
```
REDIS_HOST=...
REDIS_PORT=...
REDIS_USERNAME=...
REDIS_PASSWORD=...
```

If storage service will be used, ensure the following env var is defined:
```
STORAGE_SERVICE_API_URL=...
```

If embedded service will be used, ensure the following env var is defined:
```
EMBEDDING_SERVICE_API_URL=...
```

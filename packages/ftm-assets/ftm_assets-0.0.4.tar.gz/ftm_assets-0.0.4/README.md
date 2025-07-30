[![ftm-assets on pypi](https://img.shields.io/pypi/v/ftm-assets)](https://pypi.org/project/ftm-assets/)
[![Python test and package](https://github.com/dataresearchcenter/ftm-assets/actions/workflows/python.yml/badge.svg)](https://github.com/dataresearchcenter/ftm-assets/actions/workflows/python.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Coverage Status](https://coveralls.io/repos/github/dataresearchcenter/ftm-assets/badge.svg?branch=main)](https://coveralls.io/github/dataresearchcenter/ftm-assets?branch=main)
[![AGPLv3+ License](https://img.shields.io/pypi/l/ftm-assets)](./LICENSE)

# ftm-assets

Resolve assets (currently images) related to [FollowTheMoney](https://followthemoney.tech) entities.

## Get images based on qid

```bash
cat entities.ftm.json | ftm-assets load-entities
```

## Run api server

```bash
uvicorn --port 8000 ftm_assets.api:app --workers 4
```

## Get asset metadata

For images:

```bash
curl https://localhost:8000/img/<entity_id>
```

```json
{
    "id": "<entity_id>",
    "url": "...",
    "alt": "...",
    "attribution": {
        "author": "...",
        "license": "...",
    }
}
```

## Run as an OpenAleph worker service

    pip install ftm-assets[openaleph]

To ingreate `ftm-assets` into the [OpenAleph](https://openaleph.org) ecosystem as a worker that processes entities, start the worker queue like this:

    PROCRASTINATE_APP=ftm_assets.tasks.app procrastinate worker -q ftm-assets

To defer tasks from other places, use `ftm-assets` as queue name and `ftm_assets.tasks.resolve_image` as the task identifier.

### Docker

Run the queue worker with changing the entrypoint to `procrastinate`:

    docker run ghcr.io/dataresearchcenter/ftm-asstets --entrypoint procrastinate worker -q ftm-assets

## License and Copyright

`ftm-assets`, (C) 2025 [Data and Research Center – DARC](https://dataresearchcenter.org)

`ftm-assets` is licensed under the AGPLv3 or later license.

see [NOTICE](./NOTICE) and [LICENSE](./LICENSE)

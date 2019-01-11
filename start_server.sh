#!/usr/bin/env bash
alembic upgrade head
gunicorn --pid gunicorn.pid -w 3 -b 0.0.0.0:8090 mogiminsk.server:init_async --worker-class aiohttp.GunicornUVLoopWebWorker
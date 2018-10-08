#!/usr/bin/env bash

gunicorn -w 3 -b 0.0.0.0:8020 --worker-class aiohttp.GunicornUVLoopWebWorker mogiminsk.server:async_init
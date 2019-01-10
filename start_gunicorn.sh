#!/usr/bin/env bash
gunicorn --pid gunicorn.pid -w 3 -b 0.0.0.0:8090 mogiminsk.server:init --worker-class aiohttp.GunicornUVLoopWebWorker
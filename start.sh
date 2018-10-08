#!/usr/bin/env bash

gunicorn --daemon --pid server.pid -w 3 -b 0.0.0.0:8020 --worker-class aiohttp.GunicornUVLoopWebWorker mogiminsk.server:init
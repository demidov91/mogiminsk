import argparse

from aiohttp import web

from mogiminsk.utils import init_client, destroy_client
from mogiminsk.middleware import (
    block_ip,
    initilize_session,
    suppress_error,
    clear_tasklocal,
)
from mogiminsk.settings import TELEGRAM_API_KEY


def init():
    app = web.Application(middlewares=[
        suppress_error.middleware,
        clear_tasklocal.middleware,
        block_ip.KeyShield(TELEGRAM_API_KEY).middleware,
        initilize_session.middleware,
    ])

    from bot_telegram.server import TgServer
    app.router.add_post("/mogiminsk/tg/", TgServer.webhook)

    app.on_startup.append(init_client)
    app.on_cleanup.append(destroy_client)
    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path')
    parser.add_argument('--port')

    args = parser.parse_args()
    port = args.port

    if port:
        port = int(port)

    elif not args.path:
        port = 8090

    if port:
        web.run_app(init(), host='0.0.0.0', port=port)

    else:
        web.run_app(init(), path=args.path, port=None)
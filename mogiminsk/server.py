import argparse

from aiohttp import web

from api.views import providers, trips
from mogiminsk.middleware import (
    initilize_session,
    suppress_error,
    clear_tasklocal,
)
from mogiminsk.utils import (
    init_client,
    destroy_client,
)


def init():
    app = web.Application()
    app.add_subapp('/mogiminsk/', init_messagers())
    app.add_subapp('/api/', init_api())
    return app


def init_messagers():
    from bot_telegram.tg_server import TgServer
    from bot_viber.viber_server import ViberServer

    app = web.Application(middlewares=[
        suppress_error.middleware,
        clear_tasklocal.middleware,
        initilize_session.middleware,
    ])

    app.router.add_post("/tg/", TgServer.webhook)
    app.router.add_post("/viber/{token}/", ViberServer.webhook)

    app.on_startup.append(init_client)
    app.on_cleanup.append(destroy_client)

    return app
    

def init_api():
    app = web.Application()
    app.router.add_get("/trips/", trips)
    app.router.add_get("/providers/", providers)

    app.on_startup.append(init_client)
    app.on_cleanup.append(destroy_client)

    return app


async def init_async():
    return init()


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
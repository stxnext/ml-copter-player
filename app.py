import asyncio
import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from db import setup_db
from routes import setup_routes


def make_app(loop=None):
    app = web.Application(loop=loop)

    app['static_root_url'] = '/static'
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')
        )
    )

    setup_routes(app)
    setup_db(app, loop)

    return app


def main():
    app = make_app(asyncio.get_event_loop())
    port = int(os.environ.get('PORT', '8080'))
    web.run_app(app, port=port)


if __name__ == '__main__':
    main()

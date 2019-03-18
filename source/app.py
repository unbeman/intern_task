import sys

from aiohttp import web
from middlewares import error_middleware
import initial
from request_handler.request_handler import RequestHandler
from controller.controller import Controller
from database_connector.postgres_connector import AsyncPostgresqlConnector
import logging

logger = logging.getLogger(__name__)


async def on_start_tasks(app: web.Application) -> None:
    db_connector = AsyncPostgresqlConnector(**app['database_settings'])
    await db_connector.init()
    app['db_connector'] = db_connector
    controller = Controller(db_connector)
    app['controller'] = controller
    request_handler = RequestHandler(app, controller)
    app['request_handler'] = request_handler
    logger.info('Server started')


async def on_shutdown_tasks(app: web.Application) -> None:
    await app['db_connector'].close()
    logger.info('Server stopped')


def init_app(argv):
    app = web.Application(middlewares=[error_middleware])
    initial.init_app_settings(app, argv)
    app.on_startup.append(on_start_tasks)
    app.on_shutdown.append(on_shutdown_tasks)
    return app


def main(argv):
    app = init_app(argv)
    web.run_app(app, host=app['host'], port=app['port'])


if __name__ == '__main__':
    main(sys.argv[1:])

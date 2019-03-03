from aiohttp import web
from middlewares import error_middleware
import initial


def on_start_tasks(app: web.Application) -> None:
    pass


def on_shutdown_tasks(app: web.Application) -> None:
    pass


app = web.Application(middlewares=[error_middleware])
initial.init_app_settings(app)
app.on_startup.append(on_start_tasks)
app.on_shutdown.append(on_shutdown_tasks)
web.run_app(app, host=app['host'], port=app['port'])

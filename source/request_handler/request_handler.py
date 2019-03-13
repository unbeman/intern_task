from aiohttp import web
import jsonschema
import utils
import logging
from controller.controller import Controller

logger = logging.getLogger(__name__)


class RequestHandler:
    def __init__(self, app: web.Application, controller: Controller):
        self.__add_routes(app)
        self.controller = controller

    def __add_routes(self, app: web.Application) -> None:
        app.router.add_post('/company', self.create_company)
        app.router.add_post('/company/{company_id}', self.update_company)
        app.router.add_get('/company/{company_id}', self.get_company)
        app.router.add_post('/worker', self.create_worker)
        app.router.add_post('/worker/{worker_id}', self.update_worker)
        app.router.add_get('/worker/{worker_id}', self.get_worker)
        app.router.add_post('/worker/bind', self.bind_worker_to_company)
        app.router.add_post('/worker/{worker_id}/goods', self.assign_worker_to_goods)
        app.router.add_post('/storefront/filling', self.fill_storefront)

    async def create_company(self, request: web.Request) -> web.Response:
        data = await request.json()
        try:
            jsonschema.validate(data, utils.create_company_schema)
        except jsonschema.ValidationError as e:
            logger.error(e)
            raise web.HTTPUnprocessableEntity()
        answer = await self.controller.create_company(data)
        return web.json_response(answer)

    async def update_company(self, request: web.Request) -> web.Response:
        company_id = request.match_info['company_id']
        data = await request.json()
        try:
            jsonschema.validate(data, utils.update_company_schema)
        except jsonschema.ValidationError as e:
            logger.error(e)
            raise web.HTTPUnprocessableEntity()
        await self.controller.update_company(company_id, data)
        return web.Response()

    async def get_company(self, request: web.Request) -> web.Response:
        company_id = request.match_info['company_id']
        answer = await self.controller.get_company(company_id)
        return web.json_response(answer)

    async def create_worker(self, request: web.Request) -> web.Response:
        data = await request.json()
        try:
            jsonschema.validate(data, utils.create_worker_schema)
        except jsonschema.ValidationError as e:
            logger.error(e)
            raise web.HTTPUnprocessableEntity()
        answer = await self.controller.create_worker(data)
        return web.json_response(answer)

    async def update_worker(self, request: web.Request) -> web.Response:
        worker_id = request.match_info['worker_id']
        data = await request.json()
        try:
            jsonschema.validate(data, utils.update_worker_schema)
        except jsonschema.ValidationError as e:
            logger.error(e)
            raise web.HTTPUnprocessableEntity()
        await self.controller.update_worker(worker_id, data)
        return web.Response()

    async def get_worker(self, request: web.Request):
        worker_id = request.match_info['worker_id']
        answer = await self.controller.get_worker(worker_id)
        return web.json_response(answer)

    # not implemented yet
    async def bind_worker_to_company(self, request: web.Request) -> web.Response:
        pass

    async def fill_storefront(self, request: web.Request) -> web.Response:
        pass

    async def assign_worker_to_goods(self, request: web.Request) -> web.Response:
        pass

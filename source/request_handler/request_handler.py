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
        app.router.add_get('/company', self.get_companies)
        app.router.add_get('/company/{company_id}', self.get_company)
        app.router.add_get('/company/{company_id}/goods', self.get_goods_of_company)
        app.router.add_get('/company/{company_id}/workers', self.get_workers_of_company)
        app.router.add_post('/worker', self.create_worker)
        app.router.add_post('/worker/{worker_id}', self.update_worker)
        app.router.add_get('/worker/{worker_id}', self.get_worker)
        app.router.add_post('/goods/{goods_id}/assign', self.assign_worker_to_goods)
        app.router.add_post('/goods/{goods_id}', self.update_goods)
        app.router.add_post('/storefront', self.fill_storefront)
        app.router.add_get('/storefront', self.get_goods_in_storefront)

    async def create_company(self, request: web.Request) -> web.Response:
        data = await request.json()
        jsonschema.validate(data, utils.create_company_schema)
        answer = await self.controller.create_company(data)
        return web.json_response(answer)

    async def update_company(self, request: web.Request) -> web.Response:
        company_id = request.match_info['company_id']
        data = await request.json()
        jsonschema.validate(data, utils.update_company_schema)
        await self.controller.update_company(company_id, data)
        return web.Response()

    async def get_company(self, request: web.Request) -> web.Response:
        company_id = request.match_info['company_id']
        answer = await self.controller.get_company(company_id)
        return web.json_response(answer)

    async def create_worker(self, request: web.Request) -> web.Response:
        data = await request.json()
        jsonschema.validate(data, utils.create_worker_schema)
        answer = await self.controller.create_worker(data)
        return web.json_response(answer)

    async def update_worker(self, request: web.Request) -> web.Response:
        worker_id = request.match_info['worker_id']
        data = await request.json()
        jsonschema.validate(data, utils.update_worker_schema)
        await self.controller.update_worker(worker_id, data)
        return web.Response()

    async def get_worker(self, request: web.Request):
        worker_id = request.match_info['worker_id']
        answer = await self.controller.get_worker(worker_id)
        return web.json_response(answer)

    async def fill_storefront(self, request: web.Request) -> web.Response:
        data = await request.json()
        jsonschema.validate(data, utils.goods_schema)
        answer = await self.controller.add_goods(data)
        return web.json_response(answer)

    async def get_goods_in_storefront(self, request: web.Request) -> web.Response:
        answer = await self.controller.get_goods_list()
        return web.json_response(answer)

    async def assign_worker_to_goods(self, request: web.Request) -> web.Response:
        goods_id = request.match_info['goods_id']
        data = await request.json()
        jsonschema.validate(data, utils.assign_worker_to_goods_schema)
        await self.controller.assign_worker_to_goods(goods_id, data)
        return web.Response()

    async def update_goods(self, request: web.Request) -> web.Response:
        goods_id = request.match_info['goods_id']
        data = await request.json()
        jsonschema.validate(data, utils.update_goods_schema)
        await self.controller.update_goods(goods_id, data)
        return web.Response()

    async def get_workers_of_company(self, request: web.Request):
        company_id = request.match_info['company_id']
        answer = await self.controller.get_workers_by_company_id(company_id)
        return web.json_response(answer)

    async def get_goods_of_company(self, request: web.Request):
        company_id = request.match_info['company_id']
        answer = await self.controller.get_goods_of_company_id(company_id)
        return web.json_response(answer)

    async def get_companies(self, request: web.Request):
        pass

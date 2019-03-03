import logging
from aiohttp import web

logger = logging.getLogger(__name__)


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPException as e:
        logger.debug("http exception, e:%s" % e)
        resp = web.json_response({'error': e.reason}, status=e.status)
        return resp
    except Exception as e:
        logger.exception(e)
        resp = web.json_response({'error': 'Internal Server Error'}, status=500)
        return resp

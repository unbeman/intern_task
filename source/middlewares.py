import logging
from json import JSONDecodeError

import jsonschema
from aiohttp import web
import utils

logger = logging.getLogger(__name__)

# TODO: add 404 and other errors
@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPException as e:
        logger.debug("http exception, e:%s" % e)
        resp = web.json_response({'error': e.reason}, status=e.status)
        return resp
    except JSONDecodeError as e:
        logger.exception(e)
        return web.json_response({'error': 'Unprocessable entity'}, status=422)
    except (ValueError, TypeError, jsonschema.ValidationError) as e:
        logger.exception(e)
        resp = web.json_response({'error': 'Invalid json payload'}, status=400)
        return resp
    except utils.RecordNotFound as e:
        resp = web.json_response({'error': str(e)}, status=404)
        return resp
    except utils.TransactionFailed:
        return web.Response(status=400)
    except Exception as e:
        logger.exception(e)
        resp = web.json_response({'error': 'Internal Server Error'}, status=500)
        return resp

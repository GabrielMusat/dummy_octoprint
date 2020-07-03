from aiohttp import web
from printer import get_printer


async def get_job(req: web.Request) -> web.Response:
    return web.json_response(get_printer().job.state)

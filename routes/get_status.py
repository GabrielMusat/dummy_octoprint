from aiohttp import web
from printer import get_printer


async def get_status(req: web.Request) -> web.Response:
    return web.json_response(get_printer().status.state)

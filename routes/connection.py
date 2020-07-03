from aiohttp import web
from printer import get_printer


async def connection(req: web.Request) -> web.Response:
    try:
        body = await req.json()
    except Exception as e:
        print("could not decode json:", str(e))
        return web.Response(status=400)

    if "command" not in body:
        print("command not in body")
        return web.Response(status=400)

    if body["command"] != "connect":
        print("command parameter does not say connect")
        return web.Response(status=400)

    code = get_printer().connect()
    return web.Response(status=code)

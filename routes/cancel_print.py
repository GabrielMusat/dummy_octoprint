from aiohttp import web
from printer import get_printer


async def cancel_print(req: web.Request) -> web.Response:
    try:
        body = await req.json()
    except Exception as e:
        print("could not decode json:", str(e))
        return web.Response(status=400)

    if "command" not in body:
        print("command not in body")
        return web.Response(status=400)

    if body["command"] != "cancel":
        print("command parameter is not cancel")
        return web.Response(status=400)

    code = get_printer().cancel_print()
    return web.Response(status=code)

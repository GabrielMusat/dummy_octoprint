from aiohttp import web
from printer import get_printer


async def print_file(req: web.Request) -> web.Response:
    try:
        body = await req.json()
    except Exception as e:
        print("could not decode json:", str(e))
        return web.Response(status=400)

    if "command" not in body:
        print("command not in body")
        return web.Response(status=400)

    if "print" not in body:
        print("print not in body")
        return web.Response(status=400)

    if body["command"] != "select":
        print("command parameter is not select")
        return web.Response(status=400)

    if not body["print"]:
        print("print parameter is not True")
        return web.Response(status=400)

    if "file" not in req.match_info:
        print("file not specified")
        return web.Response(status=400)

    file = req.match_info["file"]
    code = get_printer().print_file(file)
    return web.Response(status=code)

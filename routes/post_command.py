from aiohttp import web
from printer import get_printer


async def post_command(req: web.Request) -> web.Response:
    try:
        body = await req.json()
    except Exception as e:
        print("could not decode json:", str(e))
        return web.Response(status=400)

    if "commands" not in body:
        print("commands not in body")
        return web.Response(status=400)

    if type(body["commands"]) != list:
        print("commands is not a list")
        return web.Response(status=400)

    for cmd in body["commands"]:
        if type(cmd) != str:
            print("one command is not str")
            return web.Response(status=400)

    code = get_printer().post_command()
    return web.Response(status=code)

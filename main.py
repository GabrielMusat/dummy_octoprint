import asyncio
from aiohttp import web
from args import Args
from printer import get_printer
import routes.cancel_print
import routes.print_file
import routes.post_command
import routes.connection
import routes.get_job
import routes.get_status


def main():
    args = Args()
    app = web.Application()
    app.add_routes([
        web.post("/connection", routes.connection.connection),
        web.get("/printer", routes.get_status.get_status),
        web.get("/job", routes.get_job.get_job),
        web.post("/printer/command", routes.post_command.post_command),
        web.post("/files/local/{file}", routes.print_file.print_file),
        web.post("/job", routes.cancel_print.cancel_print)
    ])
    get_printer(args.path)
    web.run_app(app, host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()

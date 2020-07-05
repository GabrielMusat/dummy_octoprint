import random
import asyncio
import typing as T
import os
from StatefullClass import StatefulClass


status = {
    "sd": {
        "ready": False
    },
    "state": {
        "flags": {
            "cancelling": False,
            "closedOrError": False,
            "error": False,
            "finishing": False,
            "operational": False,
            "printing": False,
            "paused": False,
            "pausing": False,
            "ready": False,
            "resuming": False,
            "sdReady": False
        },
        "text": "Closed"
    },
    "temperature": {
        "bed": {
            "actual": 20,
            "offset": 0,
            "target": 0
        },
        "tool0": {
            "actual": 20,
            "offset": 0,
            "target": 0
        }
    }
}

job = {
    "job": {
        "estimatedPrintTime": None,
        "filament": {
            "length": None,
            "volume": None
        },
        "file": {
            "date": None,
            "name": None,
            "origin": None,
            "path": None,
            "size": None
        },
        "lastPrintTime": None,
        "user": None
    },
    "progress": {
        "completion": None,
        "filepos": None,
        "printTime": None,
        "printTimeLeft": None,
        "printTimeOrigin": None,
    },
    "state": "Closed"
}


class Printer:
    def __init__(self, path: str):
        self.path = path
        self.status = StatefulClass(status)
        self.job = StatefulClass(job)
        self.temperature_loop()

    def get_job(self) -> dict:
        return self.job.state

    def get_status(self) -> dict:
        return self.status.state

    def temperature_loop(self) -> None:
        async def nested():
            while True:
                self.status.set(["temperature", "bed", "actual"], 20+3*random.random())
                self.status.set(["temperature", "tool0", "actual"], 20+3*random.random())
                await asyncio.sleep(0.2)
        asyncio.get_event_loop().create_task(nested())

    def connect(self) -> int:
        async def nested():
            await asyncio.sleep(5)
            self.status.set(["state", "text"], "Operational")
            self.status.set(["state", "flags", "operational"], True)
            self.job.set(["state"], "Operational")
        asyncio.get_event_loop().create_task(nested())
        return 200

    def post_command(self) -> int:
        if self.status.get(["state", "text"]) == "Closed":
            return 409
        return 204

    def print_file(self, file: str) -> int:
        if self.status.get(["state", "text"]) == "Closed":
            return 409
        if not os.path.isfile(os.path.join(self.path, "uploads", file)):
            return 404

        self.job.set(["job", "file", "name"], file)
        self.job.set(["progress", "completion"], 0)
        self.job.set(["state"], "Printing")
        self.status.set(["state", "flags", "printing"], True)
        self.status.set(["state", "text"], "Printing")
        self.status.set(["state", "flags", "operational"], False)

        async def nested():
            while True:
                if self.status.get(["state", "text"]) == "Cancelling" or self.job.get(["progress", "completion"]) >= 100:
                    if self.status.get(["state", "text"]) == "Cancelling":
                        await asyncio.sleep(5)
                    self.job.set(["job", "file", "name"], None)
                    self.job.set(["progress", "completion"], None)
                    self.status.set(["state", "flags", "printing"], False)
                    self.job.set(["state"], "Operational")
                    self.status.set(["state", "text"], "Operational")
                    self.status.set(["state", "flags", "operational"], True)
                    break
                self.job.set(["progress", "completion"], self.job.get(["progress", "completion"])+1)
                await asyncio.sleep(0.1)

        asyncio.get_event_loop().create_task(nested())
        return 204

    def cancel_print(self):
        if self.status.get(["state", "text"]) != "Printing":
            return 400
        self.status.set(["state", "text"], "Cancelling")
        return 204


printer: T.Union[Printer, None] = None


def get_printer(path: str = None) -> Printer:
    global printer
    if printer is None:
        assert path is not None
        printer = Printer(path)
    return printer

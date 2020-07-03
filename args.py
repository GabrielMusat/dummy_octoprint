import argparse


class Args:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--port", type=int)
        parser.add_argument("--path", type=str, default="/home/pi/.octoprint")
        args = parser.parse_args()
        self.port: int = args.port
        self.path: str = args.path

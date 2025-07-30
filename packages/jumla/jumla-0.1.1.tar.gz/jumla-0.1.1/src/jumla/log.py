import time
from colorama import Fore, Style


class Logger:
    def __init__(self):
        self.start_time = time.time()

    def info(self, msg: str):
        print(f"{msg}")

    def success(self, msg: str):
        print(f"{msg}")

    def warn(self, msg: str):
        print(f"⚠️  {Fore.LIGHTYELLOW_EX}{msg}")

    def error(self, msg: str):
        print(f"{msg}")

    def bullet(self, msg: str):
        print(f"  • {msg}")

    def step(self, msg: str):
        print(f"→  {msg}")

    def finish(self, msg="Done"):
        elapsed = time.time() - self.start_time
        print(f"{Style.BRIGHT}{Fore.GREEN}{msg} in {elapsed:.2f}s")


logger = Logger()

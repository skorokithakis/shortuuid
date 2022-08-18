import argparse
import sys
from typing import Any

from .main import uuid


def cli(*args: Any) -> None:
    parser = argparse.ArgumentParser(description='Print a random shortuuid')
    parser.parse_args(*args)

    print(uuid())


def main() -> None:
    cli(sys.argv[1:])

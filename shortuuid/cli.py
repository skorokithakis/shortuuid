import argparse
import sys
from typing import Any
from uuid import UUID

from .main import decode
from .main import encode
from .main import uuid


def encode_cli(args:argparse.Namespace):
    print(encode(args.uuid))


def decode_cli(args:argparse.Namespace):
    print(str(decode(args.shortuuid, legacy=args.legacy)))


def cli(*args: Any) -> None:
    parser = argparse.ArgumentParser(description='Print a random shortuuid')

    subparsers = parser.add_subparsers(help='sub-command help')

    encode_parser = subparsers.add_parser('encode', help='encode help')
    encode_parser.add_argument('uuid', type=UUID, help='A uuid to encode')
    encode_parser.set_defaults(func=encode_cli)

    decode_parser = subparsers.add_parser('decode', help='decode help')
    decode_parser.add_argument('shortuuid', type=str, help='A shortuuid to decode to a uuid')
    decode_parser.add_argument('--legacy', action='store_true')
    decode_parser.set_defaults(func=decode_cli)

    passed_args = parser.parse_args(*args)

    if hasattr(passed_args, 'func'):
        passed_args.func(passed_args)
    else:
        # Maintain legacy behaviour
        print(uuid())


def main() -> None:
    cli(sys.argv[1:])

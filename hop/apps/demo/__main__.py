#!/usr/bin/env python

import argparse
import signal

from . import __version__
from . import example


def append_subparser(subparser, cmd, func):

    assert func.__doc__, "empty docstring: {}".format(func)
    help_ = func.__doc__.split("\n")[0].lower().strip(".")
    desc = func.__doc__.strip()

    parser = subparser.add_parser(
        cmd,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help=help_,
        description=desc,
    )

    parser.set_defaults(func=func)
    return parser

def _set_up_parser():
    """Set up parser for scimma app entry point.

    """
    parser = argparse.ArgumentParser(prog="hop-demo")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s version {__version__}",
    )

    # my arguments here
    subparser = parser.add_subparsers(
    title="Commands",
    metavar="subscribe -F <CONFIGURATION_FILE> -E <EMAIL>",
    dest="cmd",
    )
    subparser.required = True

    # registering your app
    p = append_subparser(subparser, "subscribe", example._main)
    example._add_parser_args(p)

    return parser


def _set_up_cli():
    """Set up CLI boilerplate for scimma app entry point.

    """
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    parser = _set_up_parser()
    return parser.parse_args()


# ------------------------------------------------
# -- main

def main():
    args = _set_up_cli()
    args.func(args)
    # do stuff here


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from config.config import Config

from log.logger import Logger

from con.handler import Handler

from web.proxy import HttpProxy

from argparse import ArgumentParser

import os

VERSION = "1.0"

def args():
    parser = ArgumentParser(
        description="Web Security " + VERSION
    )

    parser.add_argument(
        dest="RHOST",
        type=str,
        help="Remote web server host"
    )

    parser.add_argument(
        dest="RPORT",
        type=int,
        help="Remote web server port"
    )

    parser.add_argument(
        "-p",
        "--port",
        dest="PORT",
        type=int,
        default=80,
        help="Port number"
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        type=str,
        default="waf-config.yml",
        help="Config file"
    )

    parser.add_argument(
        "-l",
        "--log",
        dest="log",
        type=str,
        default="waf-log.json",
        help="Log file"
    )

    return parser.parse_args()

def main():
    argv = args()

    config = Config(argv.file)

    if os.path.isfile(argv.log):
        with open(argv.log, "wt") as f:
            f.write("[\n\n]")

    def output(data):
        with open(argv.log, "at") as f:
            f.seek(f.tell() -2)
            f.write(data)

    logger = Logger(output)
    
    handler = Handler(
        config.ruleset,
        config.allow,
        config.size,
        config.action,
        logger
    )

    proxy = Proxy(handler, config.block, argv.RHOST, argv.RPORT)
    
    proxy.run("0.0.0.0", argv.port)

if __name__ == "__main__":
    main()
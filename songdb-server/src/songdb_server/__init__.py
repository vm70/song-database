"""Song Database server."""

import argparse
from importlib.metadata import metadata

import uvicorn

from songdb_server.api.app import app, export_openapi_json

__version__ = metadata("songdb-server")["Version"]


def main() -> None:
    """Main command-line entrypoint."""
    parser = argparse.ArgumentParser(
        prog="songdb-server",
        description="Song Database Server",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="show the version number of this program and exit",
    )
    parser.add_argument(
        "-e",
        "--export-openapi",
        type=str,
        help="export OpenAPI specification to the given file path and exit",
        metavar="JSONFILE",
        dest="export",
    )
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.export is not None:
        export_openapi_json(args.export)
        return

    uvicorn.run(app, host="127.0.0.1")

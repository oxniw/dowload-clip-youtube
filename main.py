# ==============================================================================
# File: .//Description-of-file/main.md
# Overview: Application entry point parsing CLI arguments and launching server.
# ==============================================================================

import argparse
from config import DEFAULT_HOST, DEFAULT_PORT
from start_server import start_server


def main():
    parser = argparse.ArgumentParser(description="YouTube Downloader & Clipper Web App")
    parser.add_argument(
        "--host",
        type=str,
        default=DEFAULT_HOST,
        help=f"Host address to bind (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port number to bind (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Disable automatic browser opening on launch",
    )

    args = parser.parse_args()
    start_server(
        host=args.host,
        port=args.port,
        auto_open=not args.no_browser,
    )


if __name__ == "__main__":
    main()

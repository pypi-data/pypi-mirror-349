"""Command-line interface for running the MCP server."""

import argparse
import os
import sys


def main() -> None:
    """Parse command line arguments and start the server."""
    parser = argparse.ArgumentParser(
        description="Dev-Kit MCP Server",
        epilog="Provides tools for file operations and running makefile commands",
    )
    parser.add_argument(
        "--root-dir", type=str, help="Root directory for file operations (defaults to current directory)"
    )

    args = parser.parse_args()

    # Set default root directory if not provided
    if args.root_dir is None:
        args.root_dir = os.getcwd()
        print(f"No root directory specified, using current directory: {args.root_dir}")

    # Validate root directory
    if not os.path.isdir(args.root_dir):
        print(f"Error: Root directory '{args.root_dir}' does not exist or is not a directory")
        sys.exit(1)

    print("Starting Dev-Kit MCP Server")
    print(f"Root directory: {args.root_dir}")

    try:
        # Override sys.argv to pass the root_dir to start_server
        # This is needed because start_server uses argparse internally
        sys.argv = [sys.argv[0]]
        if args.root_dir:
            sys.argv.extend(["--root-dir", args.root_dir])

        from .fastmcp_server import start_server

        # Get the server instance
        fastmcp = start_server()

        # Run the server
        fastmcp.run()
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create an ASCII .netrc file for SDSS authentication."""

from __future__ import annotations

import argparse
import getpass
import os
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a .netrc-style ASCII file with secure permissions."
    )
    parser.add_argument(
        "--machine",
        default="data.sdss5.org",
        help="Remote machine name (default: data.sdss5.org)",
    )
    parser.add_argument(
        "--login",
        default="sdss5",
        help="Login name (default: sdss5)",
    )
    parser.add_argument(
        "--password",
        help="Password. If omitted, it is requested without echoing it.",
    )
    parser.add_argument(
        "--output",
        default="~/.netrc",
        help="Output path (default: ~/.netrc)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = Path(args.output).expanduser()

    if output.exists() and not args.force:
        raise SystemExit(
            f"Refusing to overwrite existing file: {output}\n"
            "Use --force to replace it."
        )

    password = args.password or getpass.getpass("Password: ")
    if not password:
        raise SystemExit("Password cannot be empty.")

    content = (
        f"machine {args.machine}\n"
        f"login {args.login}\n"
        f"password {password}\n"
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="ascii")
    os.chmod(output, 0o600)

    print(f"Created {output} with permissions 600.")


if __name__ == "__main__":
    main()

from __future__ import annotations

from dotenv import load_dotenv

from cli_app import execute_command
from cli_parser import build_parser


def main() -> int:
    load_dotenv()
    args = build_parser().parse_args()
    return execute_command(args)


if __name__ == "__main__":
    raise SystemExit(main())

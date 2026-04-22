from __future__ import annotations

from dotenv import load_dotenv

from chromy.cli import app


def main() -> None:
    load_dotenv()
    app()


if __name__ == "__main__":
    main()

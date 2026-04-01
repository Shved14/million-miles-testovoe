import argparse
import asyncio

from parser.scheduler import run_once, run_scheduler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    if args.once:
        created = asyncio.run(run_once())
        print(f"Created: {created}")
        return

    asyncio.run(run_scheduler())


if __name__ == "__main__":
    main()

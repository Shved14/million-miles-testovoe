import argparse

from parser.scheduler import run_once, run_scheduler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    if args.once:
        created = run_once()
        print(f"Created: {created}")
        return

    run_scheduler()


if __name__ == "__main__":
    main()

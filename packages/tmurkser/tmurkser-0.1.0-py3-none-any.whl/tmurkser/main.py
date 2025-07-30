import sys
from argparse import ArgumentParser

from tmurkser.session_loader import SessionLoader
from tmurkser.session_saver import SessionSaver


def main():
    """Run the tmurkser script."""
    parser = ArgumentParser(
        prog="tmurkser",
        description="A tmux session manager",
        epilog="Licensed under the MIT license. (c) 2025 Simon Barth",
    )
    subparsers = parser.add_subparsers(help="commands help", dest="command")

    save_parser = subparsers.add_parser("save", help="Save the current sessions")
    save_parser.add_argument("NAME", nargs="?", help="Name of the session file to save")

    target_group = save_parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument(
        "--all", "-a", action="store_true", help="Save all current sessions"
    )
    target_group.add_argument(
        "--session", nargs="*", help="Name of the session(s) to save"
    )
    target_group.add_argument(
        "--exclude",
        nargs="*",
        help="Name of the session(s) to exclude. All others will be saved",
    )

    load_parser = subparsers.add_parser("load", help="Load saved sessions")
    load_parser.add_argument("NAME", nargs="?", help="Name of the session file to load")

    args = parser.parse_args()

    config_name = args.NAME if args.NAME else "default"

    if args.command == "load":
        loader = SessionLoader(config_name)
        loader.load()

    if args.command == "save":
        saver = SessionSaver(config_name)
        if args.all:
            print("Saving all sessions...")
            saver.save_sessions(True)
        elif args.session:
            print(f"Saving sessions: {args.session}")
            saver.save_sessions(session_names=args.session)
        elif args.exclude:
            print(f"Excluding sessions: {args.exclude}")
            saver.save_sessions(exclude_names=args.exclude)

    sys.exit(0)

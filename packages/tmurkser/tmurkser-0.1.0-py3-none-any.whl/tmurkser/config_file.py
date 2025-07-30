from pathlib import Path
from typing import TypedDict, cast

from tomlkit import parse

from tmurkser.dataclasses import TmuxConfig


class ParsedTmuxWindow(TypedDict):
    name: str
    path: Path


class ParsedTmuxSession(TypedDict):
    name: str
    windows: list[ParsedTmuxWindow]


class ParsedTmuxConfig(TypedDict):
    sessions: list[ParsedTmuxSession]


def load_config(path: Path) -> TmuxConfig:
    """Load the tmux configuration.

    Args:
        path (Path): The path to the configuration file.

    Returns:
        TmuxConfig: A list of standard sessions.
    """
    config: ParsedTmuxConfig = {"sessions": []}
    with open(path, "rb") as f:
        data = parse(f.read())
        parsed_config = cast(ParsedTmuxConfig, data)

        for session in parsed_config["sessions"]:
            session_name = session["name"]
            windows = [
                ParsedTmuxWindow(name=window["name"], path=Path(window["path"]))
                for window in session["windows"]
            ]
            config["sessions"].append(
                ParsedTmuxSession(name=session_name, windows=windows)
            )

    return TmuxConfig.from_parsed(config)


def get_config_dir() -> Path:
    """Get the configuration directory.

    Creates the directory if it does not exist.

    Returns:
        The configuration directory path.
    """
    config_dir = Path.home() / ".config" / "tmurkser"
    config_dir.mkdir(parents=True, exist_ok=True)

    return config_dir

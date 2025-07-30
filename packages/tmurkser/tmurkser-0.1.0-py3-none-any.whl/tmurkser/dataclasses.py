from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from tmurkser.config_file import ParsedTmuxConfig


@dataclass
class TmuxWindow:
    name: str
    path: Path


@dataclass
class TmuxSession:
    name: str
    windows: list[TmuxWindow]


@dataclass
class TmuxConfig:
    sessions: list[TmuxSession]

    @classmethod
    def from_parsed(
        cls: Type["TmuxConfig"], parsed_config: "ParsedTmuxConfig"
    ) -> "TmuxConfig":
        """Create a TmuxConfig instance from a parsed configuration."""
        sessions = [
            TmuxSession(
                name=session["name"],
                windows=[
                    TmuxWindow(name=window["name"], path=Path(window["path"]))
                    for window in session["windows"]
                ],
            )
            for session in parsed_config["sessions"]
        ]
        return cls(sessions=sessions)

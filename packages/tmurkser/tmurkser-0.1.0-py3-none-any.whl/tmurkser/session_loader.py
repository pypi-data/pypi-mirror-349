from pathlib import Path

from libtmux import Server

from tmurkser.config_file import get_config_dir, load_config


class SessionLoader:
    """Class to load tmux sessions."""

    path: Path

    def __init__(self, name):
        self.path = get_config_dir() / f"{name}.toml"

    def load(self):
        if not self.path.exists():
            print(f"Session file {self.path} does not exist.")
            return

        server = Server()
        for session in load_config(self.path).sessions:
            # Check if the session already exists
            existing_session = server.sessions.filter(session_name=session.name)
            if existing_session:
                print(f"Session {session.name} already exists.")
                continue

            # Create a new session
            window = session.windows.pop(0)
            new_session = server.new_session(
                session_name=session.name,
                attach=False,
                window_name=window.name,
            )

            active_pane = new_session.windows[0].active_pane
            if active_pane:
                active_pane.send_keys(f" cd {window.path} && clear", enter=True)

            for window in session.windows:
                new_session.new_window(
                    window_name=window.name,
                    start_directory=str(window.path),  # noqa
                )

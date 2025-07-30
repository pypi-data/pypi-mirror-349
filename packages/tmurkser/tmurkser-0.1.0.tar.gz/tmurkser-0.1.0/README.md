# Tmurkser

> A simple tmux session manager

## Installation

```shell
pipx install tmurkser
```

## Features

### Currently implemented

- Save different tmux configurations with the `save` command. Save sessions and windows, saves the current working path of the active pane of each window.
  - Save all session
  - Only save specific sessions
  - Exclue specific sessions
- Restore tmux configurations

## Planned features

- Pane handling (currently only the active pane is handled)
- Session templates

## Development

Dependencies are managed with [uv](https://docs.astral.sh/uv/)

Run the program with:

```shell
uv run tmurkser
```


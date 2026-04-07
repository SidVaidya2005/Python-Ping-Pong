# Python Ping Pong

A beginner-friendly Ping Pong game built with Python's `turtle` module.

## Setup

1. Make sure Python 3.10+ is installed.
2. Clone this repository.
3. Run:

```bash
python main.py
```

## Features

- Game states: **start**, **playing**, **paused**, **game over**
- Two modes:
  - **Player vs Player**
  - **Player vs CPU**
- Difficulty presets (**easy**, **medium**, **hard**) that tune:
  - Ball base speed
  - Ball acceleration on paddle hit
  - Paddle move speed
  - Max points needed per round
  - CPU reaction + accuracy
- Match format toggle: **Best of 1 / 3 / 5**
- In-session match stats:
  - Round wins per side
  - Session longest win streak
- Persistent stats in `stats.json`:
  - Total matches played
  - Match wins per side
  - All-time longest streak
- UI improvements:
  - Start screen and controls hint
  - Pause/resume
  - Restart
  - Winner banner
  - Arena boundary + center line

## Controls

- `W` / `S`: Left paddle up/down
- `↑` / `↓`: Right paddle up/down (PVP mode)
- `1`: Start Player vs Player
- `2`: Start Player vs CPU
- `Space`: Pause / Resume
- `R`: Restart current match
- `D`: Cycle difficulty (when not actively playing)
- `B`: Cycle Best-of format (when not actively playing)
- `Q`: Quit game

## Key remapping

All key bindings are centralized in:

`/home/runner/work/Python-Ping-Pong/Python-Ping-Pong/game_config.py`

Update `CONTROL_BINDINGS` to remap controls.

## Testing

Run non-graphics unit tests with:

```bash
python -m unittest discover
```

## Screenshots / GIF

You can add gameplay screenshots or a GIF to this README to showcase the modes and UI flow.

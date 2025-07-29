# snsr

A playful Python-based "screensaver" that randomly moves your mouse and simulates key presses to keep your screen active.

## Features

- Moves the mouse to random screen positions.
- Simulates random key presses.
- Keeps your system from going idle.
- Lightweight and easy to use.

## Installation

You can install `snsr` using `pip` or `uv` once it’s published to PyPI:

```bash
pip install snsr
# or
uv pip install snsr
````

## Usage

Once installed, run the screensaver from any terminal with:

```bash
snsr
```

It will:

* Move your mouse to random points on the screen
* Press a random key (`a`, `s`, `d`, `f`, `j`, `k`, `l`)
* Repeat this process every few seconds

### To Stop

Press `Ctrl+C` in the terminal to exit.

## Requirements

* Python 3.7+
* [`pyautogui`](https://pypi.org/project/pyautogui/)

## Notes

* Ensure your OS allows simulated input events from Python scripts.
* Useful for keeping your machine awake during long tasks (e.g., rendering, builds, meetings).

## Disclaimer

This project is intended for educational or personal use only. Use responsibly and respect your organization's policies regarding input automation.

---

MIT License © 2025

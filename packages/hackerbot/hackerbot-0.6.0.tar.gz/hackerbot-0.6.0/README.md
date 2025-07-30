![HackerBot](images/transparent_hb_horizontal_industries_.png)
# Hackerbot Python Package

The `hackerbot` Python package provides modules for controlling and managing the Hackerbot robotics system.

## Installation

You can now install the package directly from PyPI:

```bash
pip install hackerbot
```

This will automatically install all required dependencies and make the `hackerbot` package available in your Python environment.

### (Optional) Installing from Source

If you prefer to install from source for development purposes:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/hackerbotindustries/hackerbot-python-package.git
   cd hackerbot-python-package/
   ```

2. **Install Locally**

   ```bash
   pip install .
   ```

## Quick Start

SSH into the Raspberry Pi or open a VNC viewer, then install the official Python package:

```bash
pip install hackerbot
```

Or upgrade the existing package:

```bash
pip install --upgrade hackerbot
```

Then, run `python3` to open up the Python interactive shell and copy and paste the following:

```python
from hackerbot import Hackerbot

bot = Hackerbot()

bot.base.drive(0, 65)
bot.base.drive(200, 0)
```

You should see your Hackerbot leave the charger and move in the opposite direction.

```python
bot.head.look(180, 250, 70)
```

Now your robot should move its head and look up at you!

```python
bot.arm.move_joints(0, 0, 0, 0, 0, 0, 10)
```

You should see your elephant arm moving to a straight-up position.

```python
bot.base.destroy(auto_dock=True)
```

Safely clean up, and your Hackerbot will return to the charger. Once `destroy` is called, you need to create a new Hackerbot instance to perform new actions.

## Usage

After installation, you can import and use the package in your Python scripts:

```python
import hackerbot
```

## Testing

To run the unit tests:

```bash
cd tests/unit_tests
pytest
```

## Troubleshooting

If you run into issues during installation or usage, try the following:

* Use a virtual environment:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

* Upgrade `pip`:

  ```bash
  pip install --upgrade pip
  ```

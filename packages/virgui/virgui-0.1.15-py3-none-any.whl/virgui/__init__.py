import importlib.resources
from pathlib import Path

from finesse import Model

import virgui
from virgui.version import __version__ as __version__

GLOBAL_MODEL = Model()
LAYOUTS = Path(str(importlib.resources.files(virgui))) / "layouts"
ASSETS = Path(str(importlib.resources.files(virgui))) / "assets"

"""Load the HA-free humidifier logic by file path.

Loading by path avoids importing the package ``__init__``, which imports the
Home Assistant runtime.
"""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

_LOGIC_PATH = (
    Path(__file__).resolve().parent.parent
    / "custom_components"
    / "syncleo"
    / "humidifier_logic.py"
)


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("humidifier_logic", _LOGIC_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["humidifier_logic"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def logic() -> ModuleType:
    return _load()


@pytest.fixture
def model(logic: ModuleType):
    return logic.HumidifierModel(
        modes_map={
            "manual": 1,
            "auto": 2,
            "night": 3,
            "baby": 4,
            "health": 5,
            "fitness": 6,
            "yoga": 7,
            "meditation": 8,
            "prana_manual": 9,
            "prana_auto": 10,
            "aroma": 11,
        },
        manual_mode="manual",
        off_mode=0,
        continuous_mode="continuous",
        continuous_target=85,
        program_modes=("prana_manual", "prana_auto", "aroma"),
        min_humidity=30,
        max_humidity=80,
        humidity_step=5,
    )

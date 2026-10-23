"""Tests for the pysyncleo backlight compat shim (loaded by file path, no HA)."""

import importlib.util
from pathlib import Path

from pysyncleo.commands import CmdBacklight, UdpCommand

_PATH = (
    Path(__file__).resolve().parent.parent
    / "custom_components"
    / "syncleo"
    / "compat.py"
)


def _load():
    spec = importlib.util.spec_from_file_location("syncleo_compat", _PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_backlight_keeps_raw() -> None:
    compat = _load()
    compat.ensure_backlight_raw_payload()
    compat.ensure_backlight_raw_payload()
    raw = bytes.fromhex("030300ff0000ff00")
    cmd = UdpCommand.from_bytes(bytes([28]) + raw)
    assert cmd.value is True
    assert cmd.raw == raw


def test_backlight_bool_semantics_unchanged() -> None:
    compat = _load()
    compat.ensure_backlight_raw_payload()
    cmd = UdpCommand.from_bytes(bytes([28, 0]))
    assert cmd.value is False
    assert cmd.raw == b"\x00"
    assert CmdBacklight(True).serialize() == b"\x01"

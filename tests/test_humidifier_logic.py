"""Tests for the HA-free humidifier logic."""

import pytest


def test_resolve_mode_manual_vs_continuous(logic, model):
    assert logic.resolve_mode(model, 1, 50) == "manual"
    assert logic.resolve_mode(model, 1, 85) == "continuous"
    assert logic.resolve_mode(model, 2, 40) == "auto"
    assert logic.resolve_mode(model, 0, 0) is None
    assert logic.resolve_mode(model, None, None) is None
    assert logic.resolve_mode(model, 99, 0) is None


def test_available_modes_order(logic, model):
    modes = logic.available_modes(model)
    assert modes[:3] == ["manual", "continuous", "auto"]
    assert len(modes) == 12


def test_visible_target(logic, model):
    assert logic.visible_target(model, 1, 50) == 50
    assert logic.visible_target(model, 1, 85) is None
    assert logic.visible_target(model, 9, 0) is None
    assert logic.visible_target(model, 2, 40) == 40
    assert logic.visible_target(model, 0, 0) is None


@pytest.mark.parametrize("device_mode", [6, 7, 8])
def test_visible_target_program_modes_hide_co_target(logic, model, device_mode):
    assert logic.visible_target(model, device_mode, 85) is None


@pytest.mark.parametrize("device_mode", [1, 2])
def test_visible_target_hides_zero_target_on_water_shortage(logic, model, device_mode):
    assert logic.visible_target(model, device_mode, 0) is None


def test_plan_set_humidity_does_not_power_on(logic, model):
    assert logic.plan_set_humidity(model, 55, 0) == []
    assert logic.plan_set_humidity(model, 55, None) == []


def test_normalize_humidity(logic, model):
    assert logic.normalize_humidity(model, 42) == 40
    assert logic.normalize_humidity(model, 95) == 80
    assert logic.normalize_humidity(model, 10) == 30


def test_encode_backlight_raw_preserves_default_colour(logic):
    assert logic.encode_backlight_raw(2, bytes(3)) == bytes.fromhex("0202000000000000")
    assert logic.encode_backlight_raw(1, bytes([255, 0, 0])) == bytes.fromhex(
        "0101ff0000ff0000"
    )


def test_decode_backlight_clamps_level(logic):
    assert logic.decode_backlight(bytes.fromhex("0909ff0000ff0000")).level == 3


def test_plan_set_mode(logic, model):
    assert logic.plan_set_mode(model, "continuous", 50, 55) == [
        ("mode", 1),
        ("target", 85),
    ]
    assert logic.plan_set_mode(model, "manual", 85, 55) == [
        ("mode", 1),
        ("target", 55),
    ]
    assert logic.plan_set_mode(model, "manual", 50, 55) == [("mode", 1)]
    assert logic.plan_set_mode(model, "yoga", 50, 55) == [("mode", 7)]
    with pytest.raises(ValueError):
        logic.plan_set_mode(model, "bogus", 50, 55)


def test_plan_set_humidity_rounds_and_clamps(logic, model):
    assert logic.plan_set_humidity(model, 42, 1) == [("target", 40)]
    assert logic.plan_set_humidity(model, 43, 1) == [("target", 45)]
    assert logic.plan_set_humidity(model, 95, 1) == [("target", 80)]
    assert logic.plan_set_humidity(model, 10, 1) == [("target", 30)]
    assert logic.plan_set_humidity(model, 60, 2) == [("mode", 1), ("target", 60)]


def test_plan_turn_on(logic, model):
    assert logic.plan_turn_on(model, 7, None) == [("mode", 7)]
    assert logic.plan_turn_on(model, 1, 85) == [("mode", 1), ("target", 85)]
    assert logic.plan_turn_on(model, 1, 50) == [("mode", 1)]


def test_water_shortage(logic, model):
    assert logic.is_water_shortage(model, 1, 0, 0) is True
    assert logic.is_water_shortage(model, 1, 50, 2) is False
    assert logic.is_water_shortage(model, 0, 0, 0) is False
    assert logic.is_water_shortage(model, 9, 0, 0) is False
    assert logic.is_water_shortage(model, 11, 0, 0) is False
    assert logic.is_water_shortage(model, 1, None, 0) is None


def test_backlight_roundtrip(logic):
    assert logic.decode_backlight(bytes.fromhex("030300ff0000ff00")) == (
        logic.BacklightState(3, (0, 255, 0))
    )
    default = logic.decode_backlight(bytes.fromhex("0000000000000000"))
    assert default.level == 0
    assert default.rgb == (255, 255, 255)
    assert logic.decode_backlight(b"\x01") is None
    assert logic.encode_backlight(2, (255, 0, 0)) == bytes.fromhex("0202ff0000ff0000")


def test_brightness_mapping(logic):
    assert logic.level_to_brightness(1) == 85
    assert logic.level_to_brightness(3) == 255
    assert logic.brightness_to_level(1) == 1
    assert logic.brightness_to_level(128) == 2
    assert logic.brightness_to_level(255) == 3

"""Home Assistant independent logic for Syncleo humidifiers (stdlib only)."""

from dataclasses import dataclass
from typing import Literal

Command = tuple[Literal["mode", "target"], int]


@dataclass(frozen=True)
class HumidifierModel:
    """Static description of a humidifier model."""

    modes_map: dict[str, int]
    manual_mode: str
    off_mode: int = 0
    continuous_mode: str | None = None
    continuous_target: int | None = None
    program_modes: tuple[str, ...] = ()
    min_humidity: int = 30
    max_humidity: int = 80
    humidity_step: int = 5


def _is_continuous(
    model: HumidifierModel, device_mode: int, target: int | None
) -> bool:
    return (
        model.continuous_mode is not None
        and target is not None
        and target == model.continuous_target
        and device_mode == model.modes_map[model.manual_mode]
    )


def resolve_mode(
    model: HumidifierModel, device_mode: int | None, target: int | None
) -> str | None:
    """Return the HA mode name for the device mode register and target."""
    if device_mode is None:
        return None
    if _is_continuous(model, device_mode, target):
        return model.continuous_mode
    for name, value in model.modes_map.items():
        if value == device_mode:
            return name
    return None


def available_modes(model: HumidifierModel) -> list[str]:
    """Return mode names: manual, continuous, then the rest in register order."""
    modes = [model.manual_mode]
    if model.continuous_mode is not None:
        modes.append(model.continuous_mode)
    modes.extend(name for name in model.modes_map if name != model.manual_mode)
    return modes


def visible_target(
    model: HumidifierModel, device_mode: int | None, target: int | None
) -> int | None:
    """Return the target humidity to show, or None when it is not meaningful."""
    mode = resolve_mode(model, device_mode, target)
    if mode is None or mode == model.continuous_mode or mode in model.program_modes:
        return None
    if target is None or not model.min_humidity <= target <= model.max_humidity:
        return None
    return target


def plan_set_mode(
    model: HumidifierModel,
    mode: str,
    current_target: int | None,
    last_manual_target: int,
) -> list[Command]:
    """Return register writes needed to switch to the given HA mode."""
    manual_value = model.modes_map[model.manual_mode]
    if mode == model.continuous_mode and model.continuous_target is not None:
        return [("mode", manual_value), ("target", model.continuous_target)]
    if mode not in model.modes_map:
        raise ValueError(f"Unknown mode: {mode}")
    commands: list[Command] = [("mode", model.modes_map[mode])]
    if (
        mode == model.manual_mode
        and model.continuous_target is not None
        and current_target == model.continuous_target
    ):
        commands.append(("target", last_manual_target))
    return commands


def normalize_humidity(model: HumidifierModel, humidity: float) -> int:
    """Round humidity to the model step and clamp it to the supported range."""
    step = model.humidity_step
    target = round(humidity / step) * step
    return int(max(model.min_humidity, min(model.max_humidity, target)))


def plan_set_humidity(
    model: HumidifierModel, humidity: float, device_mode: int | None
) -> list[Command]:
    """Return register writes needed to set the target humidity.

    Returns no writes while the device is off (or its state is unknown): setting
    the humidity must not power the device on.
    """
    if device_mode is None or device_mode == model.off_mode:
        return []
    target = normalize_humidity(model, humidity)
    manual_value = model.modes_map[model.manual_mode]
    if device_mode == manual_value:
        return [("target", target)]
    return [("mode", manual_value), ("target", target)]


def plan_turn_on(
    model: HumidifierModel,
    last_on_mode: int,
    last_on_target: int | None,
    pending_target: int | None = None,
) -> list[Command]:
    """Return register writes needed to turn on, restoring the last mode.

    A pending (already normalized) target set while the device was off wins:
    the device is switched to manual mode with that target.
    """
    if pending_target is not None:
        return [
            ("mode", model.modes_map[model.manual_mode]),
            ("target", pending_target),
        ]
    commands: list[Command] = [("mode", last_on_mode)]
    if (
        last_on_mode == model.modes_map[model.manual_mode]
        and model.continuous_target is not None
        and last_on_target == model.continuous_target
    ):
        commands.append(("target", model.continuous_target))
    return commands


def is_water_shortage(
    model: HumidifierModel,
    device_mode: int | None,
    target: int | None,
    speed: int | None,
) -> bool | None:
    """Infer water shortage: the device runs a humidity mode with target and speed 0."""
    if device_mode is None or target is None or speed is None:
        return None
    if device_mode == model.off_mode:
        return False
    if any(model.modes_map[name] == device_mode for name in model.program_modes):
        return False
    return target == 0 and speed == 0


@dataclass(frozen=True)
class BacklightState:
    """Decoded backlight register."""

    level: int
    rgb: tuple[int, int, int]


def decode_backlight(raw: bytes, levels: int = 3) -> BacklightState | None:
    """Decode the 8-byte backlight register; zero colour means default (white).

    The level is clamped to 0..levels.
    """
    if len(raw) < 8:
        return None
    rgb = (raw[2], raw[3], raw[4])
    if rgb == (0, 0, 0):
        rgb = (255, 255, 255)
    return BacklightState(level=min(levels, max(raw[0], raw[1])), rgb=rgb)


def encode_backlight_raw(level: int, color_bytes: bytes) -> bytes:
    """Encode level and the raw 3 colour bytes (written back unchanged)."""
    color = bytes(color_bytes[:3])
    return bytes([level, level]) + color + color


def level_to_brightness(level: int, levels: int = 3) -> int:
    """Convert a device level (0..levels) to HA brightness (0..255)."""
    return round(level * 255 / levels)


def brightness_to_level(brightness: int, levels: int = 3) -> int:
    """Convert HA brightness (0..255) to a device level; any nonzero value is >= 1."""
    if brightness <= 0:
        return 0
    return max(1, min(levels, round(brightness * levels / 255)))

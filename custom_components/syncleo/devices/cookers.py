"""Polaris multicookers on the Syncleo platform.

Verified against a real PMC-0528WIFI (mDNS devtype 48, firmware 2.17, protocol 2):
the device pushes current temperature, error, keep-warm and child-lock on connect and
echoes child-lock writes back immediately.

Programs were reverse-engineered by recording 10 program starts in the vendor app: the
device announces the running program in a MULTI_STEP frame (program code, target
temperature, duration), and the same frame starts it — verified by starting and stopping
"варка на пару" from this integration's protocol stack.
"""

from collections.abc import Callable
from functools import partial
from typing import Any, cast

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature, UnitOfTime
from pysyncleo.commands import UdpCommand

from ..const import (
    FEATURE_CHILD_LOCK,
    FEATURE_COOKER_CURRENT_TEMPERATURE,
    FEATURE_COOKER_DELAY_START,
    FEATURE_COOKER_PROGRAM,
    FEATURE_COOKER_START,
    FEATURE_COOKER_STOP,
    FEATURE_COOKER_TARGET_TEMPERATURE,
    FEATURE_ERROR,
    FEATURE_KEEP_WARM,
    FEATURE_TIMER,
    VENDOR_POLARIS,
)
from ..cooker_commands import CookerProgramCommand, CookerStopCommand
from .profiles import (
    ButtonConfig,
    CookerProfile,
    NumberConfig,
    SelectConfig,
    SensorConfig,
)

_COOKER_NUMBER_CONFIGS = {
    FEATURE_COOKER_TARGET_TEMPERATURE: NumberConfig(
        min_value=30,
        max_value=160,
        step=5,
        unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    FEATURE_TIMER: NumberConfig(
        min_value=1,
        max_value=720,
        step=1,
        unit_of_measurement=UnitOfTime.MINUTES,
    ),
    FEATURE_COOKER_DELAY_START: NumberConfig(
        min_value=0,
        max_value=1440,
        step=10,
        unit_of_measurement=UnitOfTime.MINUTES,
    ),
}

# name -> (program code, default temperature °C, default duration in seconds);
# recorded from the device while starting each program in the Polaris IQ Home app
POLARIS_COOKER_PROGRAMS = {
    "Суп": (0x12, 97, 3600),
    "Молочная каша": (0x11, 95, 3600),
    "Холодец": (0x18, 93, 21600),
    "Плов": (0x09, 115, 3600),
    "Варка на пару": (0x0F, 100, 300),
    "Жарка": (0x07, 160, 1800),
    "Крупа": (0x04, 115, 2400),
    "Тушение": (0x06, 93, 7200),
    "Варенье": (0x0E, 102, 3600),
    "Выпечка": (0x03, 130, 3600),
}


def _start_command(profile: CookerProfile) -> CookerProgramCommand:
    """Build the start frame for the program currently selected in HA."""
    name = profile.selected_program
    if not name or name not in profile.programs:
        raise ValueError(
            "No cooking program selected: choose one in the program select first"
        )
    code, temperature, seconds = profile.programs[name]
    return CookerProgramCommand(code=code, temperature=temperature, seconds=seconds)


def _create_polaris_cooker(device_type: int, **kwargs: Any) -> CookerProfile:
    profile = CookerProfile(
        vendor=VENDOR_POLARIS,
        device_type=device_type,
        binary_sensors=[FEATURE_ERROR],
        sensors={
            FEATURE_COOKER_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
        },
        switches=[FEATURE_CHILD_LOCK, FEATURE_KEEP_WARM],
        numbers=[
            FEATURE_COOKER_TARGET_TEMPERATURE,
            FEATURE_TIMER,
            FEATURE_COOKER_DELAY_START,
        ],
        number_configs=dict(_COOKER_NUMBER_CONFIGS),
        selects={
            FEATURE_COOKER_PROGRAM: SelectConfig(
                options_map={
                    name: code for name, (code, _, _) in POLARIS_COOKER_PROGRAMS.items()
                }
            )
        },
        programs=dict(POLARIS_COOKER_PROGRAMS),
        **kwargs,
    )
    # cooker commands are duck-typed on purpose (see cooker_commands.py), hence the casts
    profile.buttons = {
        FEATURE_COOKER_START: ButtonConfig(
            command_factory=cast(
                Callable[[], UdpCommand], partial(_start_command, profile)
            )
        ),
        FEATURE_COOKER_STOP: ButtonConfig(
            command_factory=cast(Callable[[], UdpCommand], CookerStopCommand)
        ),
    }
    return profile


PROFILES = [
    # Polaris PMC-0528WIFI (devtype 48) — verified on hardware
    _create_polaris_cooker(device_type=48),
    # same hardware family reported with another devtype in the Polaris app
    _create_polaris_cooker(device_type=268),
]

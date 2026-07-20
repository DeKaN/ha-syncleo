from typing import Dict, Tuple

from .profiles import (
    DeviceBaseProfile,
    BreezerProfile,
    ClimateProfile,
    BinarySensorMixin,
    NumberConfig,
    NumberMixin,
    SelectConfig,
    SelectMixin,
    SensorConfig,
    SensorMixin,
    SwitchMixin,
    WaterHeaterProfile,
)

from .air_conditioners import PROFILES as CONDITIONER_PROFILES
from .boilers import PROFILES as BOILER_PROFILES
from .breezers import PROFILES as BREEZER_PROFILES
from .heaters import PROFILES as HEATER_PROFILES
from .kettles import PROFILES as KETTLE_PROFILES

_ALL_PROFILES = (
    CONDITIONER_PROFILES
    + BOILER_PROFILES
    + BREEZER_PROFILES
    + HEATER_PROFILES
    + KETTLE_PROFILES
)

DEVICE_PROFILES: Dict[Tuple[str, int], DeviceBaseProfile] = {
    profile.lookup_key: profile for profile in _ALL_PROFILES
}

__all__ = [
    "DEVICE_PROFILES",
    "DeviceBaseProfile",
    "BreezerProfile",
    "ClimateProfile",
    "BinarySensorMixin",
    "NumberConfig",
    "NumberMixin",
    "SelectConfig",
    "SelectMixin",
    "SensorConfig",
    "SensorMixin",
    "SwitchMixin",
    "WaterHeaterProfile",
]

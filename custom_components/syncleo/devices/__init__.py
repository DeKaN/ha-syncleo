from typing import Dict, Tuple

from .profiles import (
    DeviceBaseProfile,
    ClimateProfile,
    BinarySensorMixin,
    NumberMixin,
    SensorMixin,
    SwitchMixin,
)

from .air_conditioners import PROFILES as CONDITIONER_PROFILES
from .heaters import PROFILES as HEATER_PROFILES

_ALL_PROFILES = CONDITIONER_PROFILES + HEATER_PROFILES

DEVICE_PROFILES: Dict[Tuple[str, int], DeviceBaseProfile] = {
    profile.lookup_key: profile for profile in _ALL_PROFILES
}

__all__ = [
    "DEVICE_PROFILES",
    "DeviceBaseProfile",
    "ClimateProfile",
    "BinarySensorMixin",
    "NumberMixin",
    "SensorMixin",
    "SwitchMixin",
]

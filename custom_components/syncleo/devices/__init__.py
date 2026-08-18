from .air_conditioners import PROFILES as CONDITIONER_PROFILES
from .boilers import PROFILES as BOILER_PROFILES
from .breezers import PROFILES as BREEZER_PROFILES
from .heaters import PROFILES as HEATER_PROFILES
from .kettles import PROFILES as KETTLE_PROFILES
from .profiles import (
    BinarySensorMixin,
    BreezerProfile,
    ClimateProfile,
    DeviceBaseProfile,
    LightMixin,
    NumberConfig,
    NumberMixin,
    SelectConfig,
    SelectMixin,
    SensorConfig,
    SensorMixin,
    SwitchMixin,
    WaterHeaterProfile,
)

_ALL_PROFILES = (
    CONDITIONER_PROFILES
    + BOILER_PROFILES
    + BREEZER_PROFILES
    + HEATER_PROFILES
    + KETTLE_PROFILES
)

DEVICE_PROFILES: dict[tuple[str, int], DeviceBaseProfile] = {
    profile.lookup_key: profile for profile in _ALL_PROFILES
}

__all__ = [
    "DEVICE_PROFILES",
    "BinarySensorMixin",
    "BreezerProfile",
    "ClimateProfile",
    "DeviceBaseProfile",
    "LightMixin",
    "NumberConfig",
    "NumberMixin",
    "SelectConfig",
    "SelectMixin",
    "SensorConfig",
    "SensorMixin",
    "SwitchMixin",
    "WaterHeaterProfile",
]

from .air_cleaners import PROFILES as AIR_CLEANER_PROFILES
from .air_conditioners import PROFILES as CONDITIONER_PROFILES
from .boilers import PROFILES as BOILER_PROFILES
from .breezers import PROFILES as BREEZER_PROFILES
from .heaters import PROFILES as HEATER_PROFILES
from .kettles import PROFILES as KETTLE_PROFILES
from .profiles import (
    AirCleanerProfile,
    BinarySensorMixin,
    BreezerProfile,
    ButtonConfig,
    ButtonMixin,
    ClimateProfile,
    DeviceBaseProfile,
    LightMixin,
    NumberConfig,
    NumberMixin,
    PresetConfig,
    SelectConfig,
    SelectMixin,
    SensorConfig,
    SensorMixin,
    SwitchConfig,
    SwitchMixin,
    VentilationProfile,
    WaterHeaterProfile,
)

_ALL_PROFILES = (
    AIR_CLEANER_PROFILES
    + CONDITIONER_PROFILES
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
    "AirCleanerProfile",
    "BinarySensorMixin",
    "BreezerProfile",
    "ButtonConfig",
    "ButtonMixin",
    "ClimateProfile",
    "DeviceBaseProfile",
    "LightMixin",
    "NumberConfig",
    "NumberMixin",
    "PresetConfig",
    "SelectConfig",
    "SelectMixin",
    "SensorConfig",
    "SensorMixin",
    "SwitchConfig",
    "SwitchMixin",
    "VentilationProfile",
    "WaterHeaterProfile",
]

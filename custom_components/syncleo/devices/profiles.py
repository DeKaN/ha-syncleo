from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import time
from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
from homeassistant.components.fan import FanEntityFeature
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.water_heater import WaterHeaterEntityFeature
from homeassistant.components.humidifier import HumidifierDeviceClass, HumidifierEntityFeature
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.time import TimeEntity
from homeassistant.const import (
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    Platform,
)

from pysyncleo.enums import UdpCommandType
from pysyncleo.models import DiagnosticStatus

from ..const import (
    FEATURE_RSSI,
    FEATURE_ERROR,
    PROFILE_TYPE_AC,
    PROFILE_TYPE_BOILER,
    PROFILE_TYPE_HEATER,
    PROFILE_TYPE_HUMIDIFIER,
    PROFILE_TYPE_KETTLE,
    PROFILE_TYPE_AIRCLEANER,
)


@dataclass(kw_only=True)
class NumberBounds:
    """Base integer bounds for any number entity."""

    min_value: int = 0
    max_value: int = 1
    step: int = 1


@dataclass(kw_only=True)
class NumberConfig(NumberBounds):
    """Configuration for dedicated command numbers."""

    pass


@dataclass(kw_only=True)
class ProgramDataField(NumberBounds):
    """Configuration for numbers packed into CmdProgramData."""

    mode: int
    offset: int = 0
    size: int = 1


@dataclass
class LightConfig:
    red_key: str
    green_key: str
    blue_key: str
    brightness_key: Optional[str] = None              # не нужнен
    brightness_levels: int = 255


@dataclass(kw_only=True)
class SelectConfig:
    options_map: Dict[str, int]

    @property
    def options(self) -> List[str]:
        return list(self.options_map.keys())


@dataclass(kw_only=True)
class SensorConfig:
    device_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = None
    unit_of_measurement: str | None = None
    entity_category: EntityCategory | None = None
    value_fn: Callable[[Any], Any] = lambda x: x
    translation_key: str | None = None


RSSI_SENSOR_CONFIG = SensorConfig(
    device_class=SensorDeviceClass.SIGNAL_STRENGTH,
    unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT, # SIGNAL_STRENGTH_DECIBELS
    state_class=SensorStateClass.MEASUREMENT,
    entity_category=EntityCategory.DIAGNOSTIC,
    value_fn=lambda status: (
        status.rssi - 256
        if status.rssi > 127
        else status.rssi
        if isinstance(status, DiagnosticStatus)
        else None
    )
)
ERROR_SENSOR_CONFIG = SensorConfig(
        device_class=None,
        unit_of_measurement=None,
        state_class=None,
        translation_key="error_text",
)


@dataclass(kw_only=True)
class SwitchConfig:
    translation_key: str | None = None


@dataclass(kw_only=True)
class BinarySensorConfig:
    translation_key: str | None = None


@dataclass(kw_only=True)
class TimeConfig:
    min_time: int | None = None
    max_time: int | None = None
    default_time: int | None = None
    translation_key: str | None = None


@dataclass(kw_only=True)
class PlatformProviderBase:
    @property
    def supported_platforms(self) -> List[Platform]:
        return [Platform.UPDATE]


@dataclass(kw_only=True)
class BinarySensorMixin(PlatformProviderBase):
    binary_sensors: list[str] = field(default_factory=list)
    binary_sensor_configs: dict[str, BinarySensorConfig] = field(default_factory=dict)

    @property
    def supported_platforms(self) -> List[Platform]:
        platforms = super().supported_platforms
        return (
            platforms + [Platform.BINARY_SENSOR] if self.binary_sensors else platforms
        )


@dataclass(kw_only=True)
class TimeMixin(PlatformProviderBase):
    times: list[str] = field(default_factory=list)
    time_configs: dict[str, TimeConfig] = field(default_factory=dict)

    @property
    def supported_platforms(self) -> List[Platform]:
        platforms = super().supported_platforms
        return (
            platforms + [Platform.TIME] if self.times else platforms
        )


@dataclass(kw_only=True)
class LightMixin(PlatformProviderBase):
    lights: Dict[str, LightConfig] = field(default_factory=dict)

    @property
    def supported_platforms(self) -> List[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.LIGHT] if self.lights else platforms


@dataclass(kw_only=True)
class NumberMixin(PlatformProviderBase):
    numbers: List[str] = field(default_factory=list)
    number_configs: dict[str, NumberConfig] = field(default_factory=dict)

    @property
    def supported_platforms(self) -> List[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.NUMBER] if self.numbers else platforms


@dataclass(kw_only=True)
class SelectMixin(PlatformProviderBase):
    selects: Dict[str, SelectConfig] = field(default_factory=dict)

    @property
    def supported_platforms(self) -> List[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.SELECT] if self.selects else platforms


@dataclass(kw_only=True)
class SensorMixin(PlatformProviderBase):
    sensors: Dict[str, SensorConfig] = field(default_factory=dict)

    def __post_init__(self):
        if self.sensors is None:
            self.sensors = {}
        if FEATURE_RSSI not in self.sensors:
            self.sensors[FEATURE_RSSI] = RSSI_SENSOR_CONFIG
        if FEATURE_ERROR not in self.sensors:
            self.sensors[FEATURE_ERROR] = ERROR_SENSOR_CONFIG

    @property
    def supported_platforms(self) -> List[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.SENSOR] if self.sensors else platforms


@dataclass(kw_only=True)
class SwitchMixin(PlatformProviderBase):
    switches: List[str] = field(default_factory=list)
    switch_configs: dict[str, SwitchConfig] = field(default_factory=dict)
    
    @property
    def supported_platforms(self) -> List[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.SWITCH] if self.switches else platforms


@dataclass(kw_only=True)
class DeviceBaseProfile(PlatformProviderBase):
    """Base generic profile for all devices."""

    vendor: str
    device_type: int
    profile_type: str
    program_data_fields: Dict[str, ProgramDataField] = field(default_factory=dict)

    @property
    def lookup_key(self) -> Tuple[str, int]:
        return (self.vendor, self.device_type)


@dataclass(kw_only=True)
class BreezerProfile(
    DeviceBaseProfile,
    BinarySensorMixin,
    NumberMixin,
    SelectMixin,
    SensorMixin,
    SwitchMixin,
):
    """Profile for Breezers and Ventilation systems."""

    supported_features: FanEntityFeature
    speed_count: int
#    speed_list: Tuple[str, ...] = field(default=("off", "one", "two", "three", "four", "five", "six", "seven", "eight"))
    preset_modes_map: Dict[str, int] = field(default_factory=dict)
    default_preset_mode: str

    hvac_modes: List[HVACMode] = field(
        default_factory=lambda: [HVACMode.OFF, HVACMode.FAN_ONLY]
    )
    hvac_mode: HVACMode = field(default=HVACMode.OFF)

    @property
    def supported_platforms(self) -> List[Platform]:
        return super().supported_platforms + [Platform.FAN]


@dataclass(kw_only=True)
class AirCleanerProfile(
    DeviceBaseProfile,
    NumberMixin,
    SelectMixin,
    SensorMixin,
    SwitchMixin,
    TimeMixin,
):
    """Profile for AirCleaner systems."""
    profile_type: str = PROFILE_TYPE_AIRCLEANER
    supported_features: FanEntityFeature = (
        FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON
    )
    speed_count: int = 3
    preset_modes_map: Dict[str, int] = field(default_factory=dict)
    default_preset_mode: str
#    speed_list: Tuple[str, ...] = field(default=("auto", "one", "two", "three"))

    @property
    def supported_platforms(self) -> List[Platform]:
        return super().supported_platforms + [Platform.FAN]


@dataclass(kw_only=True)
class ClimateProfile(
    DeviceBaseProfile,
    BinarySensorMixin,
    NumberMixin,
    SelectMixin,
    SensorMixin,
    SwitchMixin,
):
    """Profile for Heaters and Air Conditioners."""

    min_temp: int
    max_temp: int
    target_temp_step: float
    supported_features: ClimateEntityFeature

    hvac_modes_map: Dict[HVACMode, int]
    default_hvac_mode: HVACMode

    cmd_current_humidity: Optional[UdpCommandType] = None

    preset_modes_map: Dict[str, int] = field(default_factory=dict)

    cmd_fan_mode: Optional[UdpCommandType] = None
    fan_modes_map: Dict[str, int] = field(default_factory=dict)

    supported_swing_modes: List[str] = field(default_factory=list)

    @property
    def supported_platforms(self) -> List[Platform]:
        return super().supported_platforms + [Platform.CLIMATE]


@dataclass(kw_only=True)
class WaterHeaterProfile(
    DeviceBaseProfile,
    BinarySensorMixin,
    LightMixin,
    NumberMixin,
    SensorMixin,
    SwitchMixin,
    SelectMixin,
):
    """Profile for Water Heaters (Boilers) and Kettles."""

    min_temp: int
    max_temp: int
    target_temp_step: float
    supported_features: WaterHeaterEntityFeature

    operation_modes_map: Dict[str, int]
    default_operation_mode: str

    @property
    def supported_platforms(self) -> List[Platform]:
        return super().supported_platforms + [Platform.WATER_HEATER]


@dataclass(kw_only=True)
class BoilerProfile(WaterHeaterProfile):
    profile_type: str = PROFILE_TYPE_BOILER
    target_temp_step: float = 1.0
    supported_features: WaterHeaterEntityFeature = (
        WaterHeaterEntityFeature.TARGET_TEMPERATURE
        | WaterHeaterEntityFeature.OPERATION_MODE
        | WaterHeaterEntityFeature.ON_OFF
    )


@dataclass(kw_only=True)
class AirConditionerProfile(ClimateProfile):
    profile_type: str = PROFILE_TYPE_AC
    target_temp_step: float = 1.0
    supported_features: ClimateEntityFeature = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.SWING_MODE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )
    cmd_fan_mode: Optional[UdpCommandType] = UdpCommandType.SPEED


@dataclass(kw_only=True)
class HeaterProfile(ClimateProfile):
    profile_type: str = PROFILE_TYPE_HEATER
    target_temp_step: float = 1.0
    supported_features: ClimateEntityFeature = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.PRESET_MODE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )


@dataclass(kw_only=True)
class KettleProfile(WaterHeaterProfile):
    profile_type: str = PROFILE_TYPE_KETTLE
    min_temp: int = 30
    max_temp: int = 100
    target_temp_step: float = 1.0
    supported_features: int = (
        WaterHeaterEntityFeature.TARGET_TEMPERATURE
        | WaterHeaterEntityFeature.OPERATION_MODE
        | WaterHeaterEntityFeature.ON_OFF
    )




@dataclass(kw_only=True)
class HumidifierProfile(
    DeviceBaseProfile,
    NumberMixin,
    SensorMixin,
    SwitchMixin,
    TimeMixin,
    LightMixin,
):
    """Profile for Humidifiers."""
    profile_type: str = PROFILE_TYPE_HUMIDIFIER
    min_humidity: int = 30
    max_humidity: int = 80
    device_class: HumidifierDeviceClass = HumidifierDeviceClass.HUMIDIFIER,
    supported_features: HumidifierEntityFeature = HumidifierEntityFeature.MODES
    preset_modes_map: Dict[str, int] = field(default_factory=dict)
    default_preset_mode: str
    cmd_current_humidity: Optional[UdpCommandType] = None
    cmd_humidifier_mode: Optional[UdpCommandType] = None

    @property
    def supported_platforms(self) -> List[Platform]:
        return super().supported_platforms + [Platform.HUMIDIFIER]

# ==========================================
#     TEMPLATES FOR FUTURE DEVICE PROFILES
# ==========================================

# @dataclass(kw_only=True)
# class FanProfile(DeviceBaseProfile):
#     """Profile for Air Cleaners and Ventilation Systems."""

#     supported_features: FanEntityFeature
#     cmd_power: UdpCommandType
#     preset_modes: List[str] = field(default_factory=list)

#     @property
#     def supported_platforms(self) -> List[Platform]:
#         return [Platform.FAN]

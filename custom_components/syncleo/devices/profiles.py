from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
from homeassistant.components.fan import FanEntityFeature
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.water_heater import WaterHeaterEntityFeature
from homeassistant.const import (
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    Platform,
)

from pysyncleo.enums import UdpCommandType
from pysyncleo.models import DiagnosticStatus

from ..const import FEATURE_RSSI


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


RSSI_SENSOR_CONFIG = SensorConfig(
    device_class=SensorDeviceClass.SIGNAL_STRENGTH,
    unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    entity_category=EntityCategory.DIAGNOSTIC,
    value_fn=lambda status: (
        status.rssi - 256
        if status.rssi > 127
        else status.rssi
        if isinstance(status, DiagnosticStatus)
        else None
    ),
)


@dataclass(kw_only=True)
class PlatformProviderBase:
    @property
    def supported_platforms(self) -> List[Platform]:
        return []


@dataclass(kw_only=True)
class BinarySensorMixin(PlatformProviderBase):
    binary_sensors: list[str] = field(default_factory=list)

    @property
    def supported_platforms(self) -> List[Platform]:
        platforms = super().supported_platforms
        return (
            platforms + [Platform.BINARY_SENSOR] if self.binary_sensors else platforms
        )


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

    @property
    def supported_platforms(self) -> List[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.SENSOR] if self.sensors else platforms


@dataclass(kw_only=True)
class SwitchMixin(PlatformProviderBase):
    switches: List[str] = field(default_factory=list)

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
    cmd_mode: UdpCommandType
    preset_modes_map: Dict[str, int] = field(default_factory=dict)
    default_preset_mode: str
    cmd_speed: UdpCommandType | None = None

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

    cmd_mode: UdpCommandType
    hvac_modes_map: Dict[HVACMode, int]
    default_hvac_mode: HVACMode

    cmd_target_temp: UdpCommandType
    cmd_current_temp: Optional[UdpCommandType] = None
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

    cmd_mode: UdpCommandType
    operation_modes_map: Dict[str, int]
    default_operation_mode: str

    cmd_target_temp: UdpCommandType
    cmd_current_temp: Optional[UdpCommandType] = None

    @property
    def supported_platforms(self) -> List[Platform]:
        return super().supported_platforms + [Platform.WATER_HEATER]


# ==========================================
#     TEMPLATES FOR FUTURE DEVICE PROFILES
# ==========================================

# @dataclass(kw_only=True)
# class HumidifierProfile(DeviceBaseProfile):
#     """Profile for Humidifiers."""

#     min_humidity: int
#     max_humidity: int
#     supported_features: HumidifierEntityFeature
#     cmd_mode: UdpCommandType
#     modes_map: Dict[str, int]
#     cmd_target_humidity: UdpCommandType
#     cmd_current_humidity: Optional[UdpCommandType] = None
#     switches: List[str] = field(default_factory=list)
#     sensors: List[str] = field(default_factory=list)
#     speed_map: Dict[str, int] = field(default_factory=dict)

#     @property
#     def supported_platforms(self) -> List[Platform]:
#         platforms = [Platform.HUMIDIFIER]

#         if self.switches:
#             platforms.append(Platform.SWITCH)
#         if self.sensors:
#             platforms.append(Platform.SENSOR)
#         if self.speed_map:
#             platforms.append(Platform.SELECT)

#         return platforms


# @dataclass(kw_only=True)
# class FanProfile(DeviceBaseProfile):
#     """Profile for Air Cleaners and Ventilation Systems."""

#     supported_features: FanEntityFeature
#     cmd_power: UdpCommandType
#     preset_modes: List[str] = field(default_factory=list)

#     @property
#     def supported_platforms(self) -> List[Platform]:
#         return [Platform.FAN]

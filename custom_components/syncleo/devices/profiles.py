from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from homeassistant.components.climate.const import ClimateEntityFeature, HVACMode
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

from ..const import (
    FEATURE_RSSI,
    PROFILE_TYPE_AC,
    PROFILE_TYPE_BOILER,
    PROFILE_TYPE_HEATER,
    PROFILE_TYPE_KETTLE,
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
    brightness_key: str | None = None
    brightness_levels: int = 255


@dataclass(kw_only=True)
class SelectConfig:
    options_map: dict[str, int]

    @property
    def options(self) -> list[str]:
        return list(self.options_map.keys())


@dataclass(kw_only=True)
class SensorConfig:
    required_program_data_field: str | None = None
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
    def supported_platforms(self) -> list[Platform]:
        return [Platform.UPDATE]


@dataclass(kw_only=True)
class BinarySensorMixin(PlatformProviderBase):
    binary_sensors: list[str] = field(default_factory=list)

    @property
    def supported_platforms(self) -> list[Platform]:
        platforms = super().supported_platforms
        return (
            platforms + [Platform.BINARY_SENSOR] if self.binary_sensors else platforms
        )


@dataclass(kw_only=True)
class LightMixin(PlatformProviderBase):
    lights: dict[str, LightConfig] = field(default_factory=dict)

    @property
    def supported_platforms(self) -> list[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.LIGHT] if self.lights else platforms


@dataclass(kw_only=True)
class NumberMixin(PlatformProviderBase):
    numbers: list[str] = field(default_factory=list)
    number_configs: dict[str, NumberConfig] = field(default_factory=dict)

    @property
    def supported_platforms(self) -> list[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.NUMBER] if self.numbers else platforms


@dataclass(kw_only=True)
class SelectMixin(PlatformProviderBase):
    selects: dict[str, SelectConfig] = field(default_factory=dict)

    @property
    def supported_platforms(self) -> list[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.SELECT] if self.selects else platforms


@dataclass(kw_only=True)
class SensorMixin(PlatformProviderBase):
    sensors: dict[str, SensorConfig] = field(default_factory=dict)

    def __post_init__(self):
        if self.sensors is None:
            self.sensors = {}
        if FEATURE_RSSI not in self.sensors:
            self.sensors[FEATURE_RSSI] = RSSI_SENSOR_CONFIG

    @property
    def supported_platforms(self) -> list[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.SENSOR] if self.sensors else platforms


@dataclass(kw_only=True)
class SwitchMixin(PlatformProviderBase):
    switches: list[str] = field(default_factory=list)

    @property
    def supported_platforms(self) -> list[Platform]:
        platforms = super().supported_platforms
        return platforms + [Platform.SWITCH] if self.switches else platforms


@dataclass(kw_only=True)
class DeviceBaseProfile(PlatformProviderBase):
    """Base generic profile for all devices."""

    vendor: str
    device_type: int
    profile_type: str
    program_data_fields: dict[str, ProgramDataField] = field(default_factory=dict)
    data_source_features: list[str] = field(default_factory=list)

    @property
    def lookup_key(self) -> tuple[str, int]:
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
    preset_modes_map: dict[str, int] = field(default_factory=dict)
    default_preset_mode: str

    @property
    def supported_platforms(self) -> list[Platform]:
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

    hvac_modes_map: dict[HVACMode, int]
    default_hvac_mode: HVACMode

    cmd_current_humidity: UdpCommandType | None = None

    preset_modes_map: dict[str, int] = field(default_factory=dict)
    preset_mode_requirements: dict[str, str] = field(default_factory=dict)
    target_temperature_requirement: str | None = None

    cmd_fan_mode: UdpCommandType | None = None
    fan_modes_map: dict[str, int] = field(default_factory=dict)

    supported_swing_modes: list[str] = field(default_factory=list)

    @property
    def supported_platforms(self) -> list[Platform]:
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

    operation_modes_map: dict[str, int]
    default_operation_mode: str

    @property
    def supported_platforms(self) -> list[Platform]:
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
    cmd_fan_mode: UdpCommandType | None = UdpCommandType.SPEED


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
    target_temp_step: float = 5.0
    supported_features: WaterHeaterEntityFeature = (
        WaterHeaterEntityFeature.TARGET_TEMPERATURE
        | WaterHeaterEntityFeature.OPERATION_MODE
        | WaterHeaterEntityFeature.ON_OFF
    )


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

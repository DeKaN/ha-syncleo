from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
from homeassistant.const import Platform

from pysyncleo.enums import UdpCommandType


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
    offset: int
    size: int = 1


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
class SensorMixin(PlatformProviderBase):
    sensors: List[str] = field(default_factory=list)

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
    program_data_fields: Dict[str, ProgramDataField] = field(default_factory=dict)

    @property
    def lookup_key(self) -> Tuple[str, int]:
        return (self.vendor, self.device_type)


@dataclass(kw_only=True)
class ClimateProfile(
    DeviceBaseProfile, BinarySensorMixin, NumberMixin, SensorMixin, SwitchMixin
):
    """Profile for Heaters and Air Conditioners."""

    profile_type: str
    min_temp: int
    max_temp: int
    target_temp_step: float
    supported_features: ClimateEntityFeature

    cmd_mode: UdpCommandType
    hvac_modes_map: Dict[HVACMode, int]
    default_hvac_mode: HVACMode

    cmd_target_temp: UdpCommandType
    cmd_current_temp: Optional[UdpCommandType] = None

    preset_modes_map: Dict[str, int] = field(default_factory=dict)

    cmd_fan_mode: Optional[UdpCommandType] = None
    fan_modes_map: Dict[str, int] = field(default_factory=dict)

    supported_swing_modes: List[str] = field(default_factory=list)

    @property
    def supported_platforms(self) -> List[Platform]:
        return super().supported_platforms + [Platform.CLIMATE]


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


# @dataclass(kw_only=True)
# class SwitchProfile(DeviceBaseProfile):
#     """Profile for generic appliances that turn on/off."""

#     cmd_power: UdpCommandType

#     @property
#     def supported_platforms(self) -> List[Platform]:
#         return [Platform.SWITCH]


# @dataclass(kw_only=True)
# class SensorProfile(DeviceBaseProfile):
#     """Profile for passive reporting devices."""
#     pass


# @dataclass(kw_only=True)
# class WaterHeaterProfile(DeviceBaseProfile):
#     """Profile for Boilers and Kettles."""

#     min_temp: int
#     max_temp: int
#     supported_features: WaterHeaterEntityFeature
#     cmd_power: UdpCommandType
#     cmd_target_temp: UdpCommandType
#     cmd_current_temp: Optional[UdpCommandType] = None

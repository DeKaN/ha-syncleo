from homeassistant.components.fan import FanEntityFeature
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    UnitOfTemperature,
)

from pysyncleo.enums import UdpCommandType

from ..const import (
    FEATURE_BACKLIGHT,
    FEATURE_CURRENT_CO2,
    FEATURE_CURRENT_TEMPERATURE,
    FEATURE_EXPENDABLES_FILTER,
    FEATURE_VOLUME,
    PD_CO2_INSTALLED,
    PD_DAMPER,
    PD_HEATER_INSTALLED,
    PD_NIGHT_SPEED,
    PD_TURN_ON,
    PRESET_AUTO,
    PRESET_VENTILATION,
    PRESET_MANUAL,
    PRESET_NIGHT,
    PRESET_TURBO,
    VENDOR_RUSCLIMATE,
)

from .profiles import BreezerProfile, ProgramDataField, SensorConfig

PROFILES = [
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=69,
        profile_type="breezer",
        supported_features=FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON,
        speed_count=7,
        cmd_mode=UdpCommandType.MODE,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
            PRESET_VENTILATION: 5,
        },
        default_preset_mode=PRESET_AUTO,
        cmd_speed=UdpCommandType.SPEED,
        program_data_fields={
            PD_HEATER_INSTALLED: ProgramDataField(mode=0),
            PD_CO2_INSTALLED: ProgramDataField(mode=0, offset=1),
            PD_TURN_ON: ProgramDataField(mode=1, offset=0),
            PD_NIGHT_SPEED: ProgramDataField(
                mode=1, offset=1, min_value=1, max_value=3
            ),
            PD_DAMPER: ProgramDataField(mode=1, offset=2),
        },
        binary_sensors=[PD_HEATER_INSTALLED, PD_CO2_INSTALLED, PD_DAMPER],
        switches=[FEATURE_BACKLIGHT, FEATURE_VOLUME],
        sensors={
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
            FEATURE_CURRENT_CO2: SensorConfig(
                device_class=SensorDeviceClass.CO2,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    )
]

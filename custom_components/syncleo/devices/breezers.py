from homeassistant.components.fan import FanEntityFeature
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    STATE_OFF,
    UnitOfTemperature,
)

from pysyncleo.enums import UdpCommandType

from ..const import (
    FEATURE_BACKLIGHT,
    FEATURE_BREEZER_DAMPER,
    FEATURE_BREEZER_TEMPERATURE,
    FEATURE_CURRENT_CO2,
    FEATURE_CURRENT_TEMPERATURE,
    FEATURE_ERROR,
    FEATURE_EXPENDABLES_FILTER,
    FEATURE_EXPENDABLES_PREFILTER,
    FEATURE_IONIZATION,
    FEATURE_ULTRAVIOLET,
    FEATURE_VOLUME,
    FEATURE_BREEZER_MELODY,
    PD_BREEZER_AUTO_INTENSITY,
    PD_BREEZER_DAMPER,
    PD_CO2_INSTALLED,
    PD_COOLDOWN,
    PD_HEATER_INSTALLED,
    PD_NIGHT_SPEED,
    PD_TURN_ON,
    PD_UV_INSTALLED,
    PRESET_AUTO,
    PRESET_MELODY_BIRDS_SINGING,
    PRESET_MELODY_FIREPLACE_SOUND,
    PRESET_MELODY_FOREST_SOUND,
    PRESET_MELODY_RAIN_SOUND,
    PRESET_MELODY_SEA_SOUND,
    PRESET_VENTILATION,
    PRESET_MANUAL,
    PRESET_NIGHT,
    PRESET_TURBO,
    PROFILE_TYPE_BREEZER,
    VENDOR_RUSCLIMATE,
)

from .profiles import (
    BreezerProfile,
    NumberConfig,
    ProgramDataField,
    SelectConfig,
    SensorConfig,
)

PROFILES = [
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=3,
        profile_type=PROFILE_TYPE_BREEZER,
        supported_features=FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON,
        speed_count=8,
        cmd_mode=UdpCommandType.MODE,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
        },
        default_preset_mode=PRESET_AUTO,
        cmd_speed=UdpCommandType.SPEED,
        program_data_fields={
            PD_NIGHT_SPEED: ProgramDataField(mode=3, min_value=1, max_value=3),
            PD_COOLDOWN: ProgramDataField(mode=4, size=2, max_value=7200),
        },
        binary_sensors=[FEATURE_ERROR],
        numbers=[FEATURE_BREEZER_TEMPERATURE, PD_NIGHT_SPEED],
        number_configs={
            FEATURE_BREEZER_TEMPERATURE: NumberConfig(min_value=5, max_value=25),
        },
        switches=[
            FEATURE_BREEZER_DAMPER,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET,
            FEATURE_VOLUME,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
        },
    ),
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=30,
        profile_type=PROFILE_TYPE_BREEZER,
        supported_features=FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON,
        speed_count=8,
        cmd_mode=UdpCommandType.MODE,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
        },
        default_preset_mode=PRESET_AUTO,
        cmd_speed=UdpCommandType.SPEED,
        program_data_fields={
            PD_HEATER_INSTALLED: ProgramDataField(mode=0),
            PD_UV_INSTALLED: ProgramDataField(mode=0, offset=1),
            PD_TURN_ON: ProgramDataField(mode=1, offset=0),
            PD_NIGHT_SPEED: ProgramDataField(
                mode=1, offset=1, min_value=1, max_value=3
            ),
            PD_BREEZER_DAMPER: ProgramDataField(mode=1, offset=2),
        },
        binary_sensors=[FEATURE_ERROR],
        numbers=[PD_NIGHT_SPEED],
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET,
            FEATURE_VOLUME,
            PD_BREEZER_DAMPER,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_PREFILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
        },
    ),
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=32,
        profile_type=PROFILE_TYPE_BREEZER,
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
            PD_BREEZER_DAMPER: ProgramDataField(mode=1, offset=2),
        },
        binary_sensors=[
            FEATURE_ERROR,
            PD_BREEZER_DAMPER,
            PD_CO2_INSTALLED,
            PD_HEATER_INSTALLED,
        ],
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
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_PREFILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
        },
    ),
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=59,
        profile_type=PROFILE_TYPE_BREEZER,
        supported_features=FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON,
        speed_count=8,
        cmd_mode=UdpCommandType.MODE,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
        },
        default_preset_mode=PRESET_AUTO,
        cmd_speed=UdpCommandType.SPEED,
        program_data_fields={
            PD_HEATER_INSTALLED: ProgramDataField(mode=0),
            PD_UV_INSTALLED: ProgramDataField(mode=0, offset=1),
            PD_TURN_ON: ProgramDataField(mode=1, offset=0),
            PD_NIGHT_SPEED: ProgramDataField(
                mode=1, offset=1, min_value=1, max_value=3
            ),
            PD_BREEZER_DAMPER: ProgramDataField(mode=1, offset=2),
            PD_BREEZER_AUTO_INTENSITY: ProgramDataField(mode=1, offset=3),
        },
        binary_sensors=[FEATURE_ERROR],
        numbers=[PD_NIGHT_SPEED],
        selects={
            FEATURE_BREEZER_MELODY: SelectConfig(
                options_map={
                    STATE_OFF: 0,
                    PRESET_MELODY_RAIN_SOUND: 1,
                    PRESET_MELODY_SEA_SOUND: 2,
                    PRESET_MELODY_FOREST_SOUND: 3,
                    PRESET_MELODY_BIRDS_SINGING: 4,
                    PRESET_MELODY_FIREPLACE_SOUND: 5,
                }
            ),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET,
            FEATURE_VOLUME,
            PD_BREEZER_DAMPER,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_PREFILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
        },
    ),
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=69,
        profile_type=PROFILE_TYPE_BREEZER,
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
            PD_BREEZER_DAMPER: ProgramDataField(mode=1, offset=2),
        },
        binary_sensors=[
            FEATURE_ERROR,
            PD_BREEZER_DAMPER,
            PD_CO2_INSTALLED,
            PD_HEATER_INSTALLED,
        ],
        selects={
            FEATURE_BREEZER_MELODY: SelectConfig(
                options_map={
                    STATE_OFF: 0,
                    PRESET_MELODY_RAIN_SOUND: 1,
                    PRESET_MELODY_SEA_SOUND: 2,
                    PRESET_MELODY_FOREST_SOUND: 3,
                    PRESET_MELODY_BIRDS_SINGING: 4,
                    PRESET_MELODY_FIREPLACE_SOUND: 5,
                }
            ),
        },
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
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
        },
    ),
]

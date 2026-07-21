from homeassistant.components.climate.const import (
    PRESET_ECO,
    PRESET_COMFORT,
    PRESET_NONE,
    HVACMode,
    ClimateEntityFeature,
)
from pysyncleo.enums import UdpCommandType

from ..const import (
    FEATURE_ACCESS_CONTROL,
    FEATURE_AURUS_PF_AUTO_OFF_DISPLAY,
    FEATURE_AURUS_PF_HALF_POWER,
    FEATURE_AURUS_SCREENSAVER_MODE,
    FEATURE_BACKLIGHT,
    FEATURE_CHILD_LOCK,
    FEATURE_DAMPER,
    FEATURE_ERROR,
    FEATURE_POWER_LEVEL,
    FEATURE_VOLUME,
    PD_ANTI_FROST_TEMP,
    PD_AUTO_OFF_DISPLAY,
    PD_CURRENT_PRESET,
    PD_DAMPER,
    PD_ECO_DELTA,
    PD_DISPLAY_HALF_POWER,
    PD_MIN_VOLTAGE,
    PD_POWER,
    PD_TIME_END,
    PD_TIME_START,
    PD_TURN_ON,
    PD_VACATION_TEMPERATURE,
    PRESET_ANTI_FROST,
    PRESET_AURUS_SCREENSAVER_MODE_1,
    PRESET_AURUS_SCREENSAVER_MODE_3,
    PRESET_AURUS_SCREENSAVER_MODE_5,
    PRESET_AURUS_SCREENSAVER_MODE_OFF,
    PRESET_MANUAL,
    PRESET_VACATION,
    PROFILE_TYPE_HEATER,
    VENDOR_RUSCLIMATE,
)
from .profiles import ClimateProfile, NumberConfig, ProgramDataField, SelectConfig

PROFILES = [
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=6,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=10,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=5),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=5),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=9,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=10,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=5),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0, offset=2),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=5),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=11,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=5,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=5),
            PD_CURRENT_PRESET: ProgramDataField(
                mode=0, offset=1, min_value=1, max_value=6
            ),
        },
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_BACKLIGHT,
            FEATURE_ERROR,
            FEATURE_VOLUME,
        ],
        numbers=[FEATURE_POWER_LEVEL, PD_CURRENT_PRESET],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=5),
            PD_CURRENT_PRESET: NumberConfig(min_value=1, max_value=6),
        },
        switches=[
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=14,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=5,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=5),
        },
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
            FEATURE_VOLUME,
        ],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=5),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=17,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=10,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=5),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0, offset=2),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
            PD_TURN_ON: ProgramDataField(mode=4, offset=0),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=5),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=28,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=10,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=10),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0, offset=2),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
            PD_TURN_ON: ProgramDataField(mode=4, offset=0),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=10),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=31,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=10,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=10),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0, offset=2),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
            PD_TURN_ON: ProgramDataField(mode=4, offset=0),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=10),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=42,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=10,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=5),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0, offset=2),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=5),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=46,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=10,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=10),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0, offset=2),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
            PD_TURN_ON: ProgramDataField(mode=4, offset=0),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=10),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=47,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=5,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=5),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0, offset=2),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
            PD_TURN_ON: ProgramDataField(mode=4, offset=0),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=5),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=49,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=5,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=10),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0, offset=2),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
            PD_TURN_ON: ProgramDataField(mode=4, offset=0),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=10),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=71,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=10,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=10),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0, offset=2),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
            PD_TURN_ON: ProgramDataField(mode=4, offset=0),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[FEATURE_POWER_LEVEL, PD_ECO_DELTA, PD_ANTI_FROST_TEMP],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=10),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=89,
        profile_type=PROFILE_TYPE_HEATER,
        min_temp=10,
        max_temp=35,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        preset_modes_map={
            PRESET_NONE: 0,
            PRESET_COMFORT: 1,
            PRESET_ECO: 2,
            PRESET_ANTI_FROST: 3,
            PRESET_MANUAL: 4,
            PRESET_VACATION: 5,
        },
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=10),
            PD_ECO_DELTA: ProgramDataField(mode=2, offset=0, min_value=3, max_value=7),
            PD_ANTI_FROST_TEMP: ProgramDataField(
                mode=3, offset=0, min_value=3, max_value=7
            ),
            PD_TURN_ON: ProgramDataField(mode=4, offset=0),
            PD_VACATION_TEMPERATURE: ProgramDataField(
                mode=8, offset=0, min_value=5, max_value=25
            ),
            PD_DAMPER: ProgramDataField(mode=10, offset=0),
            PD_MIN_VOLTAGE: ProgramDataField(
                mode=11, offset=0, min_value=0, max_value=75
            ),
            PD_TIME_START: ProgramDataField(
                mode=12, offset=0, size=4, min_value=0, max_value=4294967295
            ),
            PD_TIME_END: ProgramDataField(
                mode=12, offset=4, size=4, min_value=0, max_value=4294967295
            ),
        },
        binary_sensors=[FEATURE_ACCESS_CONTROL, FEATURE_ERROR],
        numbers=[
            FEATURE_POWER_LEVEL,
            PD_ECO_DELTA,
            PD_ANTI_FROST_TEMP,
            PD_MIN_VOLTAGE,
            PD_VACATION_TEMPERATURE,
        ],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=10),
        },
        selects={
            FEATURE_AURUS_SCREENSAVER_MODE: SelectConfig(
                options_map={
                    PRESET_AURUS_SCREENSAVER_MODE_OFF: 0,
                    PRESET_AURUS_SCREENSAVER_MODE_1: 1,
                    PRESET_AURUS_SCREENSAVER_MODE_3: 2,
                    PRESET_AURUS_SCREENSAVER_MODE_5: 3,
                },
            ),
        },
        switches=[
            FEATURE_AURUS_PF_AUTO_OFF_DISPLAY,
            FEATURE_AURUS_PF_HALF_POWER,
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_DAMPER,
            FEATURE_VOLUME,
        ],
    ),
]

from homeassistant.components.climate.const import (
    PRESET_ECO,
    PRESET_COMFORT,
    HVACMode,
    ClimateEntityFeature,
)
from pysyncleo.enums import UdpCommandType

from ..const import (
    FEATURE_ACCESS_CONTROL,
    FEATURE_BACKLIGHT,
    FEATURE_CHILD_LOCK,
    FEATURE_DAMPER,
    FEATURE_ERROR,
    FEATURE_POWER_LEVEL,
    FEATURE_VOLUME,
    PD_ANTI_FROST_TEMP,
    PD_AUTO_OFF_DISPLAY,
    PD_ECO_DELTA,
    PD_HALF_POWER,
    PD_POWER,
    PD_TURN_ON,
    PRESET_ANTI_FROST,
    VENDOR_RUSCLIMATE,
)
from .profiles import ClimateProfile, NumberConfig, ProgramDataField

PROFILES = [
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=46,
        profile_type="heater",
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
        preset_modes_map={PRESET_COMFORT: 1, PRESET_ECO: 2, PRESET_ANTI_FROST: 3},
        program_data_fields={
            PD_POWER: ProgramDataField(mode=0, offset=0, min_value=0, max_value=10),
            PD_AUTO_OFF_DISPLAY: ProgramDataField(mode=0, offset=1),
            PD_HALF_POWER: ProgramDataField(mode=0, offset=2),
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
    )
]

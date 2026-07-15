from homeassistant.components.climate.const import (
    HVACMode,
    ClimateEntityFeature,
    FAN_AUTO,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    SWING_OFF,
    SWING_HORIZONTAL,
    SWING_VERTICAL,
    SWING_BOTH,
)
from pysyncleo.enums import UdpCommandType

from ..const import (
    FAN_MAX,
    FAN_MIN,
    FEATURE_ACCESS_CONTROL,
    FEATURE_BACKLIGHT,
    FEATURE_CHILD_LOCK,
    FEATURE_ERROR,
    FEATURE_IONIZATION,
    FEATURE_NIGHT,
    FEATURE_TURBO,
    FEATURE_VOLUME,
    PD_ANGLE_HORIZONTAL,
    PD_ANGLE_VERTICAL,
    PD_BREEZE_AWAY,
    PD_ECO_MODE,
    PD_ENERGY_SAVING,
    PD_FREEZE_PROTECTION,
    PD_FUNGUS_PROOF,
    PD_LAST_PROGRAM,
    PD_SELFCLEAN,
    PD_SILENCE_MODE,
    PD_SWING_MODE,
    VENDOR_RUSCLIMATE,
)
from .profiles import ClimateProfile, ProgramDataField

PROFILES = [
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=8,
        profile_type="ac",
        min_temp=17,
        max_temp=30,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.SWING_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.AUTO: 1,
            HVACMode.COOL: 2,
            HVACMode.DRY: 3,
            HVACMode.HEAT: 4,
            HVACMode.FAN_ONLY: 5,
        },
        default_hvac_mode=HVACMode.AUTO,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        cmd_fan_mode=UdpCommandType.SPEED,
        fan_modes_map={FAN_AUTO: 0, FAN_LOW: 1, FAN_MEDIUM: 2, FAN_HIGH: 3},
        supported_swing_modes=[
            SWING_OFF,
            SWING_VERTICAL,
            SWING_HORIZONTAL,
            SWING_BOTH,
        ],
        program_data_fields={
            PD_SWING_MODE: ProgramDataField(mode=0, size=2),
        },
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_ERROR,
            FEATURE_VOLUME,
        ],
        switches=[FEATURE_NIGHT, FEATURE_TURBO],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=10,
        profile_type="ac",
        min_temp=18,
        max_temp=32,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.SWING_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.COOL: 2,
            HVACMode.DRY: 3,
            HVACMode.HEAT: 4,
            HVACMode.FAN_ONLY: 5,
        },
        default_hvac_mode=HVACMode.FAN_ONLY,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        cmd_fan_mode=UdpCommandType.SPEED,
        fan_modes_map={FAN_AUTO: 0, FAN_LOW: 1, FAN_MEDIUM: 2, FAN_HIGH: 3},
        supported_swing_modes=[
            SWING_OFF,
            SWING_HORIZONTAL,
        ],
        program_data_fields={
            PD_SWING_MODE: ProgramDataField(mode=0),
            PD_LAST_PROGRAM: ProgramDataField(
                mode=0, offset=1, min_value=2, max_value=5
            ),
        },
        binary_sensors=[
            FEATURE_ERROR,
        ],
        switches=[FEATURE_NIGHT],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=13,
        profile_type="ac",
        min_temp=16,
        max_temp=30,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.SWING_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.AUTO: 1,
            HVACMode.COOL: 2,
            HVACMode.DRY: 3,
            HVACMode.HEAT: 4,
            HVACMode.FAN_ONLY: 5,
        },
        default_hvac_mode=HVACMode.AUTO,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        cmd_fan_mode=UdpCommandType.SPEED,
        fan_modes_map={
            FAN_AUTO: 0,
            FAN_MIN: 1,
            FAN_LOW: 2,
            FAN_MEDIUM: 3,
            FAN_HIGH: 4,
            FAN_MAX: 5,
        },
        supported_swing_modes=[
            SWING_OFF,
            SWING_VERTICAL,
            SWING_HORIZONTAL,
            SWING_BOTH,
        ],
        program_data_fields={
            PD_SWING_MODE: ProgramDataField(mode=0, size=2),
            PD_ECO_MODE: ProgramDataField(mode=0, offset=2),
            PD_FREEZE_PROTECTION: ProgramDataField(mode=0, offset=3),
            PD_SELFCLEAN: ProgramDataField(mode=1),
            PD_BREEZE_AWAY: ProgramDataField(mode=2),
            PD_ANGLE_HORIZONTAL: ProgramDataField(mode=3, max_value=5),
            PD_ANGLE_VERTICAL: ProgramDataField(mode=4, max_value=5),
        },
        binary_sensors=[
            FEATURE_ERROR,
        ],
        numbers=[PD_ANGLE_HORIZONTAL, PD_ANGLE_VERTICAL],
        switches=[
            FEATURE_NIGHT,
            FEATURE_TURBO,
            PD_BREEZE_AWAY,
            PD_ECO_MODE,
            PD_FREEZE_PROTECTION,
            PD_SELFCLEAN,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=15,
        profile_type="ac",
        min_temp=16,
        max_temp=30,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.SWING_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.AUTO: 1,
            HVACMode.COOL: 2,
            HVACMode.DRY: 3,
            HVACMode.HEAT: 4,
            HVACMode.FAN_ONLY: 5,
        },
        default_hvac_mode=HVACMode.AUTO,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        cmd_fan_mode=UdpCommandType.SPEED,
        fan_modes_map={
            FAN_AUTO: 0,
            FAN_MIN: 1,
            FAN_LOW: 2,
            FAN_MEDIUM: 3,
            FAN_HIGH: 4,
            FAN_MAX: 5,
        },
        supported_swing_modes=[
            SWING_OFF,
            SWING_VERTICAL,
            SWING_HORIZONTAL,
            SWING_BOTH,
        ],
        program_data_fields={
            PD_SWING_MODE: ProgramDataField(mode=0, size=2),
            PD_ECO_MODE: ProgramDataField(mode=0, offset=2),
            PD_FREEZE_PROTECTION: ProgramDataField(mode=0, offset=3),
            PD_SELFCLEAN: ProgramDataField(mode=1),
        },
        binary_sensors=[
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_IONIZATION,
            FEATURE_NIGHT,
            FEATURE_TURBO,
            PD_ECO_MODE,
            PD_FREEZE_PROTECTION,
            PD_SELFCLEAN,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=20,
        profile_type="ac",
        min_temp=16,
        max_temp=32,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.SWING_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.AUTO: 1,
            HVACMode.COOL: 2,
            HVACMode.DRY: 3,
            HVACMode.HEAT: 4,
            HVACMode.FAN_ONLY: 5,
        },
        default_hvac_mode=HVACMode.AUTO,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        cmd_fan_mode=UdpCommandType.SPEED,
        fan_modes_map={FAN_AUTO: 0, FAN_LOW: 1, FAN_MEDIUM: 2, FAN_HIGH: 3},
        supported_swing_modes=[
            SWING_OFF,
            SWING_VERTICAL,
            SWING_HORIZONTAL,
            SWING_BOTH,
        ],
        program_data_fields={
            PD_SWING_MODE: ProgramDataField(mode=0, size=2),
            PD_ECO_MODE: ProgramDataField(mode=0, offset=2),
            PD_FUNGUS_PROOF: ProgramDataField(mode=0, offset=3),
            PD_SELFCLEAN: ProgramDataField(mode=1),
            PD_SILENCE_MODE: ProgramDataField(mode=1, offset=1),
        },
        binary_sensors=[
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_IONIZATION,
            FEATURE_NIGHT,
            FEATURE_TURBO,
            PD_ECO_MODE,
            PD_FUNGUS_PROOF,
            PD_SELFCLEAN,
            PD_SILENCE_MODE,
        ],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=68,
        profile_type="ac",
        min_temp=18,
        max_temp=32,
        target_temp_step=1.0,
        supported_features=(
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.SWING_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.AUTO: 1,
            HVACMode.COOL: 2,
            HVACMode.DRY: 3,
            HVACMode.HEAT: 4,
            HVACMode.FAN_ONLY: 5,
        },
        default_hvac_mode=HVACMode.AUTO,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        cmd_fan_mode=UdpCommandType.SPEED,
        fan_modes_map={FAN_AUTO: 0, FAN_LOW: 1, FAN_MEDIUM: 2, FAN_HIGH: 3},
        supported_swing_modes=[
            SWING_OFF,
            SWING_VERTICAL,
            SWING_HORIZONTAL,
            SWING_BOTH,
        ],
        program_data_fields={
            PD_SWING_MODE: ProgramDataField(mode=0, size=2),
            PD_ENERGY_SAVING: ProgramDataField(mode=0, offset=2),
            PD_SILENCE_MODE: ProgramDataField(mode=0, offset=3),
        },
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_CHILD_LOCK,
            FEATURE_ERROR,
            FEATURE_VOLUME,
        ],
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_NIGHT,
            FEATURE_TURBO,
            PD_ENERGY_SAVING,
            PD_SILENCE_MODE,
        ],
    ),
]

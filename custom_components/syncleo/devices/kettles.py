from homeassistant.components.water_heater import STATE_OFF, WaterHeaterEntityFeature
from pysyncleo.enums import UdpCommandType

from ..const import (
    FEATURE_BACKLIGHT,
    FEATURE_CHILD_LOCK,
    FEATURE_ERROR,
    FEATURE_KETTLE_TEMPERATURE_PRESET,
    FEATURE_VOLUME,
    KETTLE_MODE_BOILING,
    KETTLE_MODE_IQ_BOILING,
    KETTLE_MODE_TEA_TIME,
    KETTLE_MODE_WARM_UP,
    KETTLE_MODE_WARM_UP_KEEP,
    KETTLE_PRESET_BABY_BOTTLE,
    KETTLE_PRESET_BLACK_TEA,
    KETTLE_PRESET_FLOWER_TEA,
    KETTLE_PRESET_GREEN_TEA,
    KETTLE_PRESET_HERBAL_TEA,
    KETTLE_PRESET_INSTANT_COFFEE,
    KETTLE_PRESET_NONE,
    KETTLE_PRESET_OOLONG_TEA,
    KETTLE_PRESET_PUER,
    KETTLE_PRESET_RED_TEA,
    KETTLE_PRESET_TEA_BAG,
    KETTLE_PRESET_WHITE_TEA,
    VENDOR_POLARIS,
)
from .profiles import SelectConfig, WaterHeaterProfile

PROFILES = [
    WaterHeaterProfile(
        vendor=VENDOR_POLARIS,
        device_type=2,
        profile_type="kettle",
        min_temp=30,
        max_temp=100,
        target_temp_step=5.0,
        supported_features=WaterHeaterEntityFeature.TARGET_TEMPERATURE
        | WaterHeaterEntityFeature.OPERATION_MODE
        | WaterHeaterEntityFeature.ON_OFF,
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        default_operation_mode=KETTLE_MODE_BOILING,
        operation_modes_map={
            STATE_OFF: 0,
            KETTLE_MODE_BOILING: 1,
            KETTLE_MODE_WARM_UP: 3,
            KETTLE_MODE_WARM_UP_KEEP: 4,
            KETTLE_MODE_IQ_BOILING: 5,
            KETTLE_MODE_TEA_TIME: 6,
        },
        binary_sensors=[FEATURE_ERROR],
        selects={
            FEATURE_KETTLE_TEMPERATURE_PRESET: SelectConfig(
                options_map={
                    KETTLE_PRESET_NONE: 0,
                    KETTLE_PRESET_BLACK_TEA: 100,
                    KETTLE_PRESET_BABY_BOTTLE: 40,
                    KETTLE_PRESET_INSTANT_COFFEE: 95,
                    KETTLE_PRESET_GREEN_TEA: 80,
                    KETTLE_PRESET_FLOWER_TEA: 80,
                    KETTLE_PRESET_TEA_BAG: 100,
                    KETTLE_PRESET_RED_TEA: 90,
                    KETTLE_PRESET_PUER: 95,
                    KETTLE_PRESET_OOLONG_TEA: 90,
                    KETTLE_PRESET_WHITE_TEA: 65,
                    KETTLE_PRESET_HERBAL_TEA: 90,
                }
            ),
        },
        switches=[FEATURE_CHILD_LOCK],
    ),
    WaterHeaterProfile(
        vendor=VENDOR_POLARIS,
        device_type=98,
        profile_type="kettle",
        min_temp=30,
        max_temp=100,
        target_temp_step=5.0,
        supported_features=WaterHeaterEntityFeature.TARGET_TEMPERATURE
        | WaterHeaterEntityFeature.OPERATION_MODE
        | WaterHeaterEntityFeature.ON_OFF,
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        default_operation_mode=KETTLE_MODE_BOILING,
        operation_modes_map={
            STATE_OFF: 0,
            KETTLE_MODE_BOILING: 1,
            KETTLE_MODE_WARM_UP: 3,
            KETTLE_MODE_WARM_UP_KEEP: 4,
            KETTLE_MODE_IQ_BOILING: 5,
            KETTLE_MODE_TEA_TIME: 6,
        },
        binary_sensors=[FEATURE_ERROR],
        selects={
            FEATURE_KETTLE_TEMPERATURE_PRESET: SelectConfig(
                options_map={
                    KETTLE_PRESET_NONE: 0,
                    KETTLE_PRESET_BLACK_TEA: 100,
                    KETTLE_PRESET_BABY_BOTTLE: 40,
                    KETTLE_PRESET_INSTANT_COFFEE: 95,
                    KETTLE_PRESET_GREEN_TEA: 80,
                    KETTLE_PRESET_FLOWER_TEA: 80,
                    KETTLE_PRESET_TEA_BAG: 100,
                    KETTLE_PRESET_RED_TEA: 90,
                    KETTLE_PRESET_PUER: 95,
                    KETTLE_PRESET_OOLONG_TEA: 90,
                    KETTLE_PRESET_WHITE_TEA: 65,
                    KETTLE_PRESET_HERBAL_TEA: 90,
                }
            ),
        },
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
]

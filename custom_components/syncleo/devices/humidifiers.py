from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfTemperature

from ..const import (
    FEATURE_CURRENT_HUMIDITY,
    FEATURE_HUMIDIFIER_SPEED,
    FEATURE_HUMIDIFIER_TEMPERATURE,
    FEATURE_IONIZATION,
    FEATURE_ULTRAVIOLET,
    FEATURE_VOLUME,
    FEATURE_WARM_STREAM,
    HUMIDIFIER_MODE_AROMA,
    HUMIDIFIER_MODE_AUTO,
    HUMIDIFIER_MODE_BABY,
    HUMIDIFIER_MODE_CONTINUOUS,
    HUMIDIFIER_MODE_FITNESS,
    HUMIDIFIER_MODE_HEALTH,
    HUMIDIFIER_MODE_MANUAL,
    HUMIDIFIER_MODE_MEDITATION,
    HUMIDIFIER_MODE_NIGHT,
    HUMIDIFIER_MODE_PRANA_AUTO,
    HUMIDIFIER_MODE_PRANA_MANUAL,
    HUMIDIFIER_MODE_YOGA,
    PD_HUMIDIFIER_FITNESS_DURATION,
    PD_HUMIDIFIER_MEDITATION_DURATION,
    PD_HUMIDIFIER_MEDITATION_HOUR,
    PD_HUMIDIFIER_MEDITATION_MINUTE,
    PD_HUMIDIFIER_MEDITATION_REPEAT,
    PD_HUMIDIFIER_PRANA_CYCLES,
    PD_HUMIDIFIER_PRANA_DURATION,
    PD_HUMIDIFIER_PRANA_EXERCISE,
    PD_HUMIDIFIER_PRANA_EXHALE,
    PD_HUMIDIFIER_PRANA_HOLD_IN,
    PD_HUMIDIFIER_PRANA_HOLD_OUT,
    PD_HUMIDIFIER_PRANA_INHALE,
    PD_HUMIDIFIER_YOGA_ASANAS,
    PD_HUMIDIFIER_YOGA_DURATION,
    VENDOR_RUSCLIMATE,
)
from ..humidifier_logic import HumidifierModel
from .profiles import HumidifierProfile, ProgramDataField, SelectConfig, SensorConfig

PROFILES = [
    HumidifierProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=35,
        model=HumidifierModel(
            modes_map={
                HUMIDIFIER_MODE_MANUAL: 1,
                HUMIDIFIER_MODE_AUTO: 2,
                HUMIDIFIER_MODE_NIGHT: 3,
                HUMIDIFIER_MODE_BABY: 4,
                HUMIDIFIER_MODE_HEALTH: 5,
                HUMIDIFIER_MODE_FITNESS: 6,
                HUMIDIFIER_MODE_YOGA: 7,
                HUMIDIFIER_MODE_MEDITATION: 8,
                HUMIDIFIER_MODE_PRANA_MANUAL: 9,
                HUMIDIFIER_MODE_PRANA_AUTO: 10,
                HUMIDIFIER_MODE_AROMA: 11,
            },
            manual_mode=HUMIDIFIER_MODE_MANUAL,
            off_mode=0,
            continuous_mode=HUMIDIFIER_MODE_CONTINUOUS,
            continuous_target=85,
            program_modes=(
                HUMIDIFIER_MODE_PRANA_MANUAL,
                HUMIDIFIER_MODE_PRANA_AUTO,
                HUMIDIFIER_MODE_AROMA,
            ),
            min_humidity=30,
            max_humidity=80,
            humidity_step=5,
        ),
        backlight=True,
        water_shortage_sensor=True,
        program_data_fields={
            PD_HUMIDIFIER_FITNESS_DURATION: ProgramDataField(
                mode=6, offset=0, min_value=15, max_value=60
            ),
            PD_HUMIDIFIER_YOGA_ASANAS: ProgramDataField(
                mode=7, offset=0, min_value=6, max_value=10
            ),
            PD_HUMIDIFIER_YOGA_DURATION: ProgramDataField(
                mode=7, offset=1, min_value=3, max_value=7
            ),
            PD_HUMIDIFIER_MEDITATION_DURATION: ProgramDataField(
                mode=8, offset=0, min_value=8, max_value=24
            ),
            PD_HUMIDIFIER_MEDITATION_HOUR: ProgramDataField(
                mode=8, offset=1, min_value=0, max_value=23
            ),
            PD_HUMIDIFIER_MEDITATION_MINUTE: ProgramDataField(
                mode=8, offset=2, min_value=0, max_value=59
            ),
            PD_HUMIDIFIER_MEDITATION_REPEAT: ProgramDataField(
                mode=8, offset=3, min_value=0, max_value=1
            ),
            PD_HUMIDIFIER_PRANA_CYCLES: ProgramDataField(
                mode=9, offset=0, min_value=5, max_value=20
            ),
            PD_HUMIDIFIER_PRANA_DURATION: ProgramDataField(
                mode=9, offset=1, min_value=3, max_value=24
            ),
            PD_HUMIDIFIER_PRANA_INHALE: ProgramDataField(
                mode=9, offset=2, min_value=1, max_value=4
            ),
            PD_HUMIDIFIER_PRANA_HOLD_IN: ProgramDataField(
                mode=9, offset=3, min_value=1, max_value=4
            ),
            PD_HUMIDIFIER_PRANA_EXHALE: ProgramDataField(
                mode=9, offset=4, min_value=1, max_value=4
            ),
            PD_HUMIDIFIER_PRANA_HOLD_OUT: ProgramDataField(
                mode=9, offset=5, min_value=1, max_value=4
            ),
            PD_HUMIDIFIER_PRANA_EXERCISE: ProgramDataField(
                mode=10, offset=0, min_value=1, max_value=2
            ),
        },
        switches=[
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
            FEATURE_ULTRAVIOLET,
            FEATURE_VOLUME,
            PD_HUMIDIFIER_MEDITATION_REPEAT,
        ],
        selects={
            FEATURE_HUMIDIFIER_SPEED: SelectConfig(
                options_map={"min": 1, "mid": 2, "max": 3}
            ),
            PD_HUMIDIFIER_FITNESS_DURATION: SelectConfig(
                options_map={"15": 15, "30": 30, "60": 60}
            ),
            PD_HUMIDIFIER_MEDITATION_DURATION: SelectConfig(
                options_map={"8": 8, "16": 16, "24": 24}
            ),
            PD_HUMIDIFIER_PRANA_CYCLES: SelectConfig(
                options_map={"5": 5, "10": 10, "15": 15, "20": 20}
            ),
            PD_HUMIDIFIER_PRANA_DURATION: SelectConfig(
                options_map={"3": 3, "6": 6, "12": 12, "24": 24}
            ),
            PD_HUMIDIFIER_PRANA_EXERCISE: SelectConfig(options_map={"a1": 1, "a2": 2}),
        },
        numbers=[
            PD_HUMIDIFIER_YOGA_ASANAS,
            PD_HUMIDIFIER_YOGA_DURATION,
            PD_HUMIDIFIER_MEDITATION_HOUR,
            PD_HUMIDIFIER_MEDITATION_MINUTE,
            PD_HUMIDIFIER_PRANA_INHALE,
            PD_HUMIDIFIER_PRANA_HOLD_IN,
            PD_HUMIDIFIER_PRANA_EXHALE,
            PD_HUMIDIFIER_PRANA_HOLD_OUT,
        ],
        sensors={
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
            FEATURE_HUMIDIFIER_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
        },
    ),
]

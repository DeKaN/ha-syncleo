"""Rusclimate humidifier profiles."""

from homeassistant.components.humidifier.const import (
    MODE_AUTO,
    MODE_BABY,
    MODE_NORMAL,
    MODE_SLEEP,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import EntityCategory, UnitOfTemperature, UnitOfTime
from pysyncleo.commands import CmdExpendables

from ..const import (
    FEATURE_BACKLIGHT,
    FEATURE_CURRENT_TEMPERATURE,
    FEATURE_ERROR,
    FEATURE_EXPENDABLES_FILTER,
    FEATURE_FAN_SPEED,
    FEATURE_IONIZATION,
    FEATURE_NIGHT,
    FEATURE_RESET_FILTER,
    FEATURE_TIMER,
    FEATURE_ULTRAVIOLET,
    FEATURE_VOLUME,
    FEATURE_WARM_STREAM,
    HUMIDIFIER_MODE_AROMA,
    HUMIDIFIER_MODE_FITNESS,
    HUMIDIFIER_MODE_HEALTH,
    HUMIDIFIER_MODE_MEDITATION,
    HUMIDIFIER_MODE_PRANA_AUTO,
    HUMIDIFIER_MODE_PRANA_MANUAL,
    HUMIDIFIER_MODE_YOGA,
    PD_FITNESS_TIMER,
    PD_MEDITATION_HOUR,
    PD_MEDITATION_MINUTE,
    PD_MEDITATION_REPEAT,
    PD_MEDITATION_TIMER,
    PD_PRANA_AUTO_CURRENT_ITERATION,
    PD_PRANA_AUTO_EXERCISE,
    PD_PRANA_CURRENT_ITERATION,
    PD_PRANA_EXHALE,
    PD_PRANA_EXHALE_DELAY,
    PD_PRANA_INHALE,
    PD_PRANA_INHALE_DELAY,
    PD_PRANA_ITERATION_TIME,
    PD_PRANA_ITERATIONS,
    PD_TURN_ON,
    PD_YOGA_ITERATIONS,
    PD_YOGA_TIMER,
    VENDOR_RUSCLIMATE,
)
from .profiles import (
    ButtonConfig,
    HumidifierProfile,
    NumberConfig,
    ProgramDataField,
    SelectConfig,
    SensorConfig,
)

# Hommyn labels the humidity slider endpoint 85 as CO (continuous humidification).
PROFILES = [
    HumidifierProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=4,
        min_humidity=30,
        max_humidity=85,
        target_humidity_step=5,
        modes_map={
            MODE_NORMAL: 1,
            MODE_AUTO: 2,
            MODE_SLEEP: 3,
            MODE_BABY: 4,
            HUMIDIFIER_MODE_HEALTH: 5,
            HUMIDIFIER_MODE_FITNESS: 6,
            HUMIDIFIER_MODE_YOGA: 7,
            HUMIDIFIER_MODE_MEDITATION: 8,
            HUMIDIFIER_MODE_PRANA_MANUAL: 9,
            HUMIDIFIER_MODE_PRANA_AUTO: 10,
            HUMIDIFIER_MODE_AROMA: 11,
        },
        default_mode=MODE_AUTO,
        program_data_fields={
            PD_FITNESS_TIMER: ProgramDataField(
                mode=6, min_value=15, max_value=60, step=5
            ),
            PD_YOGA_ITERATIONS: ProgramDataField(mode=7, min_value=6, max_value=10),
            PD_YOGA_TIMER: ProgramDataField(
                mode=7,
                offset=1,
                min_value=3,
                max_value=7,
                unit_of_measurement=UnitOfTime.MINUTES,
            ),
            PD_MEDITATION_TIMER: ProgramDataField(
                mode=8,
                min_value=8,
                max_value=24,
                step=8,
                unit_of_measurement=UnitOfTime.MINUTES,
            ),
            PD_MEDITATION_HOUR: ProgramDataField(mode=8, offset=1, max_value=23),
            PD_MEDITATION_MINUTE: ProgramDataField(mode=8, offset=2, max_value=59),
            PD_MEDITATION_REPEAT: ProgramDataField(mode=8, offset=3, max_value=1),
            PD_PRANA_ITERATIONS: ProgramDataField(
                mode=9, min_value=5, max_value=20, step=5
            ),
            PD_PRANA_ITERATION_TIME: ProgramDataField(
                mode=9,
                offset=1,
                min_value=3,
                max_value=24,
                step=3,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
            PD_PRANA_INHALE: ProgramDataField(
                mode=9, offset=2, min_value=1, max_value=4
            ),
            PD_PRANA_INHALE_DELAY: ProgramDataField(
                mode=9, offset=3, min_value=1, max_value=4
            ),
            PD_PRANA_EXHALE: ProgramDataField(
                mode=9, offset=4, min_value=1, max_value=4
            ),
            PD_PRANA_EXHALE_DELAY: ProgramDataField(
                mode=9, offset=5, min_value=1, max_value=4
            ),
            PD_PRANA_CURRENT_ITERATION: ProgramDataField(
                mode=9, offset=6, min_value=1, max_value=20
            ),
            PD_PRANA_AUTO_EXERCISE: ProgramDataField(mode=10, min_value=1, max_value=4),
            PD_PRANA_AUTO_CURRENT_ITERATION: ProgramDataField(
                mode=10, offset=1, min_value=1, max_value=20
            ),
        },
        binary_sensors=[FEATURE_ERROR],
        numbers=[
            PD_YOGA_ITERATIONS,
            PD_YOGA_TIMER,
            PD_MEDITATION_TIMER,
            PD_PRANA_ITERATIONS,
            PD_PRANA_ITERATION_TIME,
            PD_PRANA_INHALE,
            PD_PRANA_INHALE_DELAY,
            PD_PRANA_EXHALE,
            PD_PRANA_EXHALE_DELAY,
        ],
        selects={
            FEATURE_FAN_SPEED: SelectConfig(options_map={"1": 1, "2": 2, "3": 3}),
            PD_FITNESS_TIMER: SelectConfig(options_map={"15": 15, "30": 30, "60": 60}),
            PD_PRANA_AUTO_EXERCISE: SelectConfig(
                options_map={"A1": 1, "A2": 2, "A3": 3, "A4": 4}
            ),
        },
        sensors={
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
        },
        switches=[
            FEATURE_WARM_STREAM,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET,
            FEATURE_VOLUME,
        ],
    ),
    HumidifierProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=35,
        min_humidity=30,
        max_humidity=85,
        target_humidity_step=5,
        modes_map={
            MODE_NORMAL: 1,
            MODE_AUTO: 2,
            MODE_SLEEP: 3,
            MODE_BABY: 4,
            HUMIDIFIER_MODE_HEALTH: 5,
            HUMIDIFIER_MODE_FITNESS: 6,
            HUMIDIFIER_MODE_YOGA: 7,
            HUMIDIFIER_MODE_MEDITATION: 8,
            HUMIDIFIER_MODE_PRANA_MANUAL: 9,
            HUMIDIFIER_MODE_PRANA_AUTO: 10,
            HUMIDIFIER_MODE_AROMA: 11,
        },
        default_mode=MODE_AUTO,
        turn_on_program_data_field=PD_TURN_ON,
        program_data_fields={
            PD_TURN_ON: ProgramDataField(mode=0),
            PD_FITNESS_TIMER: ProgramDataField(
                mode=6, min_value=15, max_value=60, step=5
            ),
            PD_YOGA_ITERATIONS: ProgramDataField(mode=7, min_value=6, max_value=10),
            PD_YOGA_TIMER: ProgramDataField(
                mode=7,
                offset=1,
                min_value=3,
                max_value=7,
                unit_of_measurement=UnitOfTime.MINUTES,
            ),
            PD_MEDITATION_TIMER: ProgramDataField(
                mode=8,
                min_value=8,
                max_value=24,
                step=8,
                unit_of_measurement=UnitOfTime.MINUTES,
            ),
            PD_MEDITATION_HOUR: ProgramDataField(mode=8, offset=1, max_value=23),
            PD_MEDITATION_MINUTE: ProgramDataField(mode=8, offset=2, max_value=59),
            PD_MEDITATION_REPEAT: ProgramDataField(mode=8, offset=3, max_value=1),
            PD_PRANA_ITERATIONS: ProgramDataField(
                mode=9, min_value=5, max_value=20, step=5
            ),
            PD_PRANA_ITERATION_TIME: ProgramDataField(
                mode=9,
                offset=1,
                min_value=3,
                max_value=24,
                step=3,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
            PD_PRANA_INHALE: ProgramDataField(
                mode=9, offset=2, min_value=1, max_value=4
            ),
            PD_PRANA_INHALE_DELAY: ProgramDataField(
                mode=9, offset=3, min_value=1, max_value=4
            ),
            PD_PRANA_EXHALE: ProgramDataField(
                mode=9, offset=4, min_value=1, max_value=4
            ),
            PD_PRANA_EXHALE_DELAY: ProgramDataField(
                mode=9, offset=5, min_value=1, max_value=4
            ),
            PD_PRANA_AUTO_EXERCISE: ProgramDataField(mode=10, min_value=1, max_value=2),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        binary_sensors=[FEATURE_ERROR],
        numbers=[
            PD_YOGA_ITERATIONS,
            PD_YOGA_TIMER,
            PD_MEDITATION_TIMER,
            PD_PRANA_ITERATIONS,
            PD_PRANA_INHALE,
            PD_PRANA_INHALE_DELAY,
            PD_PRANA_EXHALE,
            PD_PRANA_EXHALE_DELAY,
        ],
        selects={
            FEATURE_FAN_SPEED: SelectConfig(options_map={"1": 1, "2": 2, "3": 3}),
            PD_FITNESS_TIMER: SelectConfig(options_map={"15": 15, "30": 30, "60": 60}),
            PD_PRANA_AUTO_EXERCISE: SelectConfig(options_map={"A1": 1, "A2": 2}),
            PD_PRANA_ITERATION_TIME: SelectConfig(
                options_map={"3": 3, "6": 6, "12": 12, "24": 24}
            ),
        },
        sensors={
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.DAYS,
                value_fn=lambda value: (
                    value[0] if isinstance(value, list) and value else None
                ),
            ),
        },
        switches=[
            FEATURE_WARM_STREAM,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET,
            FEATURE_VOLUME,
        ],
    ),
    HumidifierProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=81,
        min_humidity=40,
        max_humidity=85,
        target_humidity_step=5,
        modes_map={
            MODE_NORMAL: 1,
            MODE_AUTO: 2,
        },
        default_mode=MODE_AUTO,
        binary_sensors=[FEATURE_ERROR],
        numbers=[FEATURE_TIMER],
        number_configs={
            FEATURE_TIMER: NumberConfig(
                min_value=0,
                max_value=43200,
                step=3600,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
        },
        selects={
            FEATURE_FAN_SPEED: SelectConfig(options_map={"1": 1, "2": 2, "3": 3}),
        },
        sensors={
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
        },
        switches=[
            FEATURE_WARM_STREAM,
            FEATURE_BACKLIGHT,
            FEATURE_NIGHT,
        ],
    ),
]

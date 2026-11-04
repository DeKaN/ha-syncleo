"""Rusclimate air-cleaner profiles based on Hommyn controls."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    PERCENTAGE,
    EntityCategory,
    UnitOfTemperature,
    UnitOfTime,
    # UnitOfDensity,  # Not available in the minimum supported HA 2026.5.0.
)
from pysyncleo.commands import CmdExpendables, CmdProgramData

from ..const import (
    FEATURE_AIR_CLEANER_CHILD_LOCK,
    FEATURE_AIR_CLEANER_DISPLAY_BRIGHTNESS,
    FEATURE_BACKLIGHT,
    FEATURE_CHILD_LOCK,
    FEATURE_CURRENT_HUMIDITY,
    FEATURE_CURRENT_PM2,
    FEATURE_CURRENT_TEMPERATURE,
    FEATURE_ERROR,
    FEATURE_EXPENDABLES_FILTER,
    FEATURE_IONIZATION,
    FEATURE_RESET_FILTER,
    FEATURE_TIMER,
    FEATURE_ULTRAVIOLET,
    PD_BACKLIGHT_MODE,
    PD_FILTER_RESET,
    PD_LAST_PROGRAM,
    PD_LIGHT_TIME,
    PRESET_AUTO,
    PRESET_MANUAL,
    PRESET_NIGHT,
    VENDOR_RUSCLIMATE,
)
from .profiles import (
    AirCleanerProfile,
    ButtonConfig,
    NumberConfig,
    ProgramDataField,
    SelectConfig,
    SensorConfig,
)

PROFILES = [
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=1,
        speed_count=3,
        speed_preset_mode=PRESET_MANUAL,
        preset_speeds={PRESET_MANUAL: 1},
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 2,
            PRESET_MANUAL: 3,
        },
        default_preset_mode=PRESET_AUTO,
        turn_on_preset_field=PD_LAST_PROGRAM,
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=3),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        binary_sensors=[FEATURE_ERROR],
        sensors={
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                # Hommyn rounds the remaining hours against a 4320-hour resource.
                value_fn=lambda value: (
                    int(value[0] / 4320 * 100 + 0.5)
                    if isinstance(value, list) and value
                    else None
                ),
            ),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_ULTRAVIOLET,
            FEATURE_IONIZATION,
            FEATURE_CHILD_LOCK,
        ],
    ),
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=26,
        speed_count=4,
        speed_preset_mode=PRESET_MANUAL,
        preset_speeds={PRESET_MANUAL: 1},
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 2,
            PRESET_MANUAL: 3,
        },
        default_preset_mode=PRESET_AUTO,
        turn_on_preset_field=PD_LAST_PROGRAM,
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=3),
            PD_BACKLIGHT_MODE: ProgramDataField(mode=0, offset=1, max_value=4),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        selects={
            PD_BACKLIGHT_MODE: SelectConfig(
                options_map={"off": 0, "all": 1, "upper": 2, "middle": 3, "lower": 4}
            ),
        },
        binary_sensors=[FEATURE_ERROR],
        sensors={
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda value: (
                    value[0] if isinstance(value, list) and value else None
                ),
            ),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_ULTRAVIOLET,
            FEATURE_IONIZATION,
            FEATURE_CHILD_LOCK,
        ],
    ),
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=117,
        speed_count=4,
        min_speed=0,
        speed_preset_mode=PRESET_MANUAL,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 2,
            PRESET_MANUAL: 3,
        },
        default_preset_mode=PRESET_AUTO,
        turn_on_preset_field=PD_LAST_PROGRAM,
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=3),
            PD_FILTER_RESET: ProgramDataField(mode=1),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdProgramData(mode=1, data=b"\x01"),
                entity_category=EntityCategory.CONFIG,
            ),
        },
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
        sensors={
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda value: (
                    value[0] if isinstance(value, list) and value else None
                ),
            ),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_ULTRAVIOLET,
            FEATURE_AIR_CLEANER_CHILD_LOCK,
        ],
    ),
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=122,
        speed_count=6,
        min_speed=0,
        speed_preset_mode=PRESET_MANUAL,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 2,
            PRESET_MANUAL: 3,
        },
        default_preset_mode=PRESET_AUTO,
        turn_on_preset_field=PD_LAST_PROGRAM,
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=3),
            PD_FILTER_RESET: ProgramDataField(mode=1),
            PD_LIGHT_TIME: ProgramDataField(mode=2, max_value=3),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdProgramData(mode=1, data=b"\x01"),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        selects={
            FEATURE_AIR_CLEANER_DISPLAY_BRIGHTNESS: SelectConfig(
                options_map={"25%": 0, "50%": 1, "75%": 2, "100%": 3}
            ),
            PD_LIGHT_TIME: SelectConfig(options_map={"off": 0, "1": 1, "3": 2, "5": 3}),
        },
        binary_sensors=[FEATURE_ERROR],
        sensors={
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda value: (
                    value[0] if isinstance(value, list) and value else None
                ),
            ),
        },
        switches=[FEATURE_CHILD_LOCK],
    ),
]

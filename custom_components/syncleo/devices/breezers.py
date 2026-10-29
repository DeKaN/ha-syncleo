from homeassistant.components.climate.const import ClimateEntityFeature, HVACMode
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    STATE_OFF,
    EntityCategory,
    # UnitOfDensity,  # Not available in the minimum supported HA 2026.5.0.
    UnitOfTime,
)
from pysyncleo.commands import CmdExpendables, CmdProgramData

from ..const import (
    FEATURE_ACTIVATE_OPTIONS,
    FEATURE_AUTO_OFF_BACKLIGHT,
    FEATURE_BREEZER_DAMPER,
    FEATURE_BREEZER_MELODY,
    FEATURE_CURRENT_CO2,
    FEATURE_CURRENT_PM2,
    FEATURE_ERROR,
    FEATURE_EXPENDABLES_FILTER,
    FEATURE_EXPENDABLES_PREFILTER,
    FEATURE_IONIZATION,
    FEATURE_REMAINING_TIME,
    FEATURE_RESET_FILTER,
    FEATURE_RESET_PREFILTER,
    FEATURE_ULTRAVIOLET,
    FEATURE_VOLUME,
    PD_BREEZER_AUTO_INTENSITY,
    PD_BREEZER_DAMPER_STATE,
    PD_CO2_INSTALLED,
    PD_COOLDOWN,
    PD_HEATER_INSTALLED,
    PD_NIGHT_SPEED,
    PD_TURN_ON,
    PD_UV_INSTALLED,
    PRESET_AUTO,
    PRESET_MANUAL,
    PRESET_MELODY_BIRDS_SINGING,
    PRESET_MELODY_FIREPLACE_SOUND,
    PRESET_MELODY_FOREST_SOUND,
    PRESET_MELODY_RAIN_SOUND,
    PRESET_MELODY_SEA_SOUND,
    PRESET_NIGHT,
    PRESET_TURBO,
    PRESET_VENTILATION,
    VENDOR_RUSCLIMATE,
)
from .profiles import (
    BreezerProfile,
    ButtonConfig,
    ProgramDataField,
    SelectConfig,
    SensorConfig,
    SwitchConfig,
)

PROFILES = [
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=3,
        min_temp=5,
        max_temp=25,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.FAN_ONLY: 2,
        },
        default_hvac_mode=HVACMode.FAN_ONLY,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
        },
        fan_modes_map={
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
        },
        program_data_fields={
            PD_NIGHT_SPEED: ProgramDataField(mode=3, min_value=1, max_value=3),
            PD_COOLDOWN: ProgramDataField(mode=4, size=2, max_value=7200),
        },
        binary_sensors=[FEATURE_ERROR],
        numbers=[PD_NIGHT_SPEED],
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
        min_temp=5,
        max_temp=25,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.FAN_ONLY: 1,
        },
        default_hvac_mode=HVACMode.FAN_ONLY,
        turn_on_program_data_field=PD_TURN_ON,
        target_temperature_requirement=PD_HEATER_INSTALLED,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
        },
        fan_modes_map={
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
        },
        program_data_fields={
            PD_HEATER_INSTALLED: ProgramDataField(mode=0),
            PD_UV_INSTALLED: ProgramDataField(mode=0, offset=1),
            PD_TURN_ON: ProgramDataField(mode=1, offset=0),
            PD_NIGHT_SPEED: ProgramDataField(
                mode=1, offset=1, min_value=1, max_value=3
            ),
            PD_BREEZER_DAMPER_STATE: ProgramDataField(mode=1, offset=2),
            PD_BREEZER_AUTO_INTENSITY: ProgramDataField(
                mode=1, offset=3, min_value=1, max_value=3
            ),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0, 100),
                entity_category=EntityCategory.CONFIG,
            ),
            FEATURE_RESET_PREFILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(100, 0),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        binary_sensors=[
            FEATURE_ERROR,
            PD_HEATER_INSTALLED,
            PD_BREEZER_DAMPER_STATE,
        ],
        numbers=[PD_NIGHT_SPEED],
        switches=[
            FEATURE_AUTO_OFF_BACKLIGHT,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET,
            FEATURE_VOLUME,
            FEATURE_BREEZER_DAMPER,
        ],
        switch_configs={
            FEATURE_ULTRAVIOLET: SwitchConfig(
                required_program_data_field=PD_UV_INSTALLED
            ),
        },
        sensors={
            FEATURE_REMAINING_TIME: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
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
        device_type=32,
        min_temp=5,
        max_temp=25,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.FAN_ONLY: 5,
        },
        default_hvac_mode=HVACMode.FAN_ONLY,
        turn_on_program_data_field=PD_TURN_ON,
        preset_mode_requirements={PRESET_AUTO: PD_CO2_INSTALLED},
        target_temperature_requirement=PD_HEATER_INSTALLED,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
            PRESET_VENTILATION: 5,
        },
        fan_modes_map={
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
        },
        program_data_fields={
            PD_HEATER_INSTALLED: ProgramDataField(mode=0),
            PD_CO2_INSTALLED: ProgramDataField(mode=0, offset=1),
            PD_TURN_ON: ProgramDataField(mode=1, offset=0),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        binary_sensors=[
            FEATURE_ERROR,
            PD_CO2_INSTALLED,
            PD_HEATER_INSTALLED,
        ],
        switches=[FEATURE_AUTO_OFF_BACKLIGHT, FEATURE_VOLUME],
        sensors={
            FEATURE_REMAINING_TIME: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
            FEATURE_CURRENT_CO2: SensorConfig(
                required_program_data_field=PD_CO2_INSTALLED,
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
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=59,
        min_temp=5,
        max_temp=25,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.FAN_ONLY: 1,
        },
        default_hvac_mode=HVACMode.FAN_ONLY,
        turn_on_program_data_field=PD_TURN_ON,
        target_temperature_requirement=PD_HEATER_INSTALLED,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
        },
        fan_modes_map={
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
        },
        program_data_fields={
            PD_HEATER_INSTALLED: ProgramDataField(mode=0),
            PD_UV_INSTALLED: ProgramDataField(mode=0, offset=1),
            PD_TURN_ON: ProgramDataField(mode=1, offset=0),
            PD_NIGHT_SPEED: ProgramDataField(
                mode=1, offset=1, min_value=1, max_value=3
            ),
            PD_BREEZER_DAMPER_STATE: ProgramDataField(mode=1, offset=2),
            PD_BREEZER_AUTO_INTENSITY: ProgramDataField(
                mode=1, offset=3, min_value=1, max_value=3
            ),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0, 100),
                entity_category=EntityCategory.CONFIG,
            ),
            FEATURE_RESET_PREFILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(100, 0),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        binary_sensors=[
            FEATURE_ERROR,
            PD_HEATER_INSTALLED,
            PD_BREEZER_DAMPER_STATE,
        ],
        numbers=[PD_NIGHT_SPEED, PD_BREEZER_AUTO_INTENSITY],
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
            FEATURE_AUTO_OFF_BACKLIGHT,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET,
            FEATURE_VOLUME,
            FEATURE_BREEZER_DAMPER,
        ],
        switch_configs={
            FEATURE_ULTRAVIOLET: SwitchConfig(
                required_program_data_field=PD_UV_INSTALLED
            ),
        },
        sensors={
            FEATURE_REMAINING_TIME: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
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
        device_type=69,
        min_temp=5,
        max_temp=25,
        hvac_modes_map={
            HVACMode.OFF: 0,
            HVACMode.FAN_ONLY: 5,
        },
        default_hvac_mode=HVACMode.FAN_ONLY,
        turn_on_program_data_field=PD_TURN_ON,
        preset_mode_requirements={PRESET_AUTO: PD_CO2_INSTALLED},
        target_temperature_requirement=PD_HEATER_INSTALLED,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
            PRESET_VENTILATION: 5,
        },
        fan_modes_map={
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
        },
        program_data_fields={
            PD_HEATER_INSTALLED: ProgramDataField(mode=0),
            PD_CO2_INSTALLED: ProgramDataField(mode=0, offset=1),
            PD_TURN_ON: ProgramDataField(mode=1, offset=0),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        binary_sensors=[
            FEATURE_ERROR,
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
        switches=[FEATURE_AUTO_OFF_BACKLIGHT, FEATURE_VOLUME],
        sensors={
            FEATURE_REMAINING_TIME: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
            FEATURE_CURRENT_CO2: SensorConfig(
                required_program_data_field=PD_CO2_INSTALLED,
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
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=102,
        min_temp=5,
        max_temp=25,
        supported_features=(
            ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.FAN_ONLY: 1},
        default_hvac_mode=HVACMode.FAN_ONLY,
        turn_on_program_data_field=PD_TURN_ON,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
        },
        fan_modes_map={
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
        },
        program_data_fields={
            PD_TURN_ON: ProgramDataField(mode=1),
            PD_NIGHT_SPEED: ProgramDataField(
                mode=1, offset=1, min_value=1, max_value=3
            ),
            # Offset 2 is ignored on writes; retain it in received blocks.
            PD_BREEZER_AUTO_INTENSITY: ProgramDataField(
                mode=1, offset=3, min_value=1, max_value=3
            ),
        },
        binary_sensors=[FEATURE_ERROR],
        numbers=[PD_NIGHT_SPEED],
        switches=[FEATURE_AUTO_OFF_BACKLIGHT, FEATURE_VOLUME],
        buttons={
            FEATURE_ACTIVATE_OPTIONS: ButtonConfig(
                command_factory=lambda: CmdProgramData(data=b"\x01", mode=2),
                entity_category=EntityCategory.CONFIG,
                entity_registry_enabled_default=False,
            ),
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(100, 0),
                entity_category=EntityCategory.CONFIG,
            ),
            FEATURE_RESET_PREFILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0, 100),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        sensors={
            FEATURE_REMAINING_TIME: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_EXPENDABLES_PREFILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: val[0] if isinstance(val, list) and val else None,
            ),
        },
    ),
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=105,
        min_temp=5,
        max_temp=25,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.FAN_ONLY: 1},
        default_hvac_mode=HVACMode.FAN_ONLY,
        turn_on_program_data_field=PD_TURN_ON,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
        },
        fan_modes_map={
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
        },
        program_data_fields={
            PD_TURN_ON: ProgramDataField(mode=1),
            PD_NIGHT_SPEED: ProgramDataField(
                mode=1, offset=1, min_value=1, max_value=3
            ),
            # Offset 2 is ignored on writes; retain it in received blocks.
            PD_BREEZER_AUTO_INTENSITY: ProgramDataField(
                mode=1, offset=3, min_value=1, max_value=3
            ),
        },
        binary_sensors=[FEATURE_ERROR],
        numbers=[PD_NIGHT_SPEED, PD_BREEZER_AUTO_INTENSITY],
        switches=[FEATURE_AUTO_OFF_BACKLIGHT, FEATURE_VOLUME],
        buttons={
            FEATURE_ACTIVATE_OPTIONS: ButtonConfig(
                command_factory=lambda: CmdProgramData(data=b"\x01", mode=2),
                entity_category=EntityCategory.CONFIG,
                entity_registry_enabled_default=False,
            ),
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(100, 0),
                entity_category=EntityCategory.CONFIG,
            ),
            FEATURE_RESET_PREFILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0, 100),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        sensors={
            FEATURE_CURRENT_CO2: SensorConfig(
                device_class=SensorDeviceClass.CO2,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
            ),
            FEATURE_REMAINING_TIME: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_EXPENDABLES_PREFILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: val[0] if isinstance(val, list) and val else None,
            ),
        },
    ),
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=106,
        min_temp=5,
        max_temp=25,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.FAN_ONLY: 1},
        default_hvac_mode=HVACMode.FAN_ONLY,
        turn_on_program_data_field=PD_TURN_ON,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
        },
        fan_modes_map={
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
        },
        program_data_fields={
            PD_TURN_ON: ProgramDataField(mode=1),
            PD_NIGHT_SPEED: ProgramDataField(
                mode=1, offset=1, min_value=1, max_value=3
            ),
            # Offset 2 is ignored on writes; retain it in received blocks.
            PD_BREEZER_AUTO_INTENSITY: ProgramDataField(
                mode=1, offset=3, min_value=1, max_value=3
            ),
        },
        binary_sensors=[FEATURE_ERROR],
        numbers=[PD_NIGHT_SPEED],
        switches=[FEATURE_AUTO_OFF_BACKLIGHT, FEATURE_VOLUME],
        buttons={
            FEATURE_ACTIVATE_OPTIONS: ButtonConfig(
                command_factory=lambda: CmdProgramData(data=b"\x01", mode=2),
                entity_category=EntityCategory.CONFIG,
                entity_registry_enabled_default=False,
            ),
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(100, 0),
                entity_category=EntityCategory.CONFIG,
            ),
            FEATURE_RESET_PREFILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0, 100),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        sensors={
            FEATURE_REMAINING_TIME: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_EXPENDABLES_PREFILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: val[0] if isinstance(val, list) and val else None,
            ),
        },
    ),
    BreezerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=107,
        min_temp=5,
        max_temp=25,
        supported_features=(
            ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        ),
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.FAN_ONLY: 1},
        default_hvac_mode=HVACMode.FAN_ONLY,
        turn_on_program_data_field=PD_TURN_ON,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_TURBO: 4,
        },
        fan_modes_map={
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
        },
        program_data_fields={
            PD_TURN_ON: ProgramDataField(mode=1),
            PD_NIGHT_SPEED: ProgramDataField(
                mode=1, offset=1, min_value=1, max_value=3
            ),
            # Offset 2 is ignored on writes; retain it in received blocks.
            PD_BREEZER_AUTO_INTENSITY: ProgramDataField(
                mode=1, offset=3, min_value=1, max_value=3
            ),
        },
        binary_sensors=[FEATURE_ERROR],
        numbers=[PD_NIGHT_SPEED, PD_BREEZER_AUTO_INTENSITY],
        switches=[FEATURE_AUTO_OFF_BACKLIGHT, FEATURE_VOLUME],
        buttons={
            FEATURE_ACTIVATE_OPTIONS: ButtonConfig(
                command_factory=lambda: CmdProgramData(data=b"\x01", mode=2),
                entity_category=EntityCategory.CONFIG,
                entity_registry_enabled_default=False,
            ),
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(100, 0),
                entity_category=EntityCategory.CONFIG,
            ),
            FEATURE_RESET_PREFILTER: ButtonConfig(
                command_factory=lambda: CmdExpendables(0, 100),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        sensors={
            FEATURE_CURRENT_CO2: SensorConfig(
                device_class=SensorDeviceClass.CO2,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
            ),
            FEATURE_REMAINING_TIME: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                unit_of_measurement=UnitOfTime.SECONDS,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_EXPENDABLES_PREFILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: val[0] if isinstance(val, list) and val else None,
            ),
        },
    ),
]

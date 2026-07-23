from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.water_heater import (
    STATE_ECO,
    STATE_ELECTRIC,
    STATE_HEAT_PUMP,
    STATE_OFF,
    STATE_PERFORMANCE,
    WaterHeaterEntityFeature,
)
from homeassistant.const import STATE_ON, UnitOfTime, UnitOfVolume

from ..const import (
    FEATURE_ACCESS_CONTROL,
    FEATURE_BSS,
    FEATURE_ERROR,
    FEATURE_EXPENDABLES_ANODE,
    FEATURE_KEEP_WARM,
    FEATURE_SMART_MODE,
    FEATURE_TANK,
    PD_EXPENDABLES_ANODE,
    PD_DISPLAY_HALF_POWER,
    PD_LAST_PROGRAM,
    PD_TURN_ON,
    VENDOR_RUSCLIMATE,
)
from .profiles import BoilerProfile, SensorConfig, ProgramDataField

PROFILES = [
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=2,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        sensors={
            FEATURE_TANK: SensorConfig(
                device_class=SensorDeviceClass.VOLUME_STORAGE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfVolume.LITERS,
            ),
        },
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
            FEATURE_KEEP_WARM,
        ],
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=1),
        },
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=7,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
            STATE_HEAT_PUMP: 5,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
        ],
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=12,
        min_temp=35,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
            STATE_HEAT_PUMP: 5,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_BSS,
        ],
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=16,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ELECTRIC: 1,
            STATE_PERFORMANCE: 2,
        },
        default_operation_mode=STATE_ELECTRIC,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=18,
        min_temp=35,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
            STATE_HEAT_PUMP: 5,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_BSS,
        ],
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=19,
        min_temp=35,
        max_temp=75,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ON: 3,
        },
        default_operation_mode=STATE_ON,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=33,
        min_temp=35,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_BSS,
        ],
        sensors={
            FEATURE_TANK: SensorConfig(
                device_class=SensorDeviceClass.VOLUME_STORAGE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfVolume.LITERS,
            ),
        },
        program_data_fields={
            PD_TURN_ON: ProgramDataField(mode=0),
        },
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=44,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
            PD_DISPLAY_HALF_POWER,
        ],
        sensors={
            PD_EXPENDABLES_ANODE: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.DAYS,
            ),
        },
        program_data_fields={
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0),
            PD_LAST_PROGRAM: ProgramDataField(mode=1, min_value=1, max_value=1),
            PD_EXPENDABLES_ANODE: ProgramDataField(mode=2, min_value=0, max_value=2),
        },
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=74,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
            FEATURE_KEEP_WARM,
        ],
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=1),
        },
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=76,
        min_temp=35,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
            PD_DISPLAY_HALF_POWER,
        ],
        sensors={
            FEATURE_EXPENDABLES_ANODE: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.DAYS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
        },
        program_data_fields={
            PD_TURN_ON: ProgramDataField(mode=0),
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=1, offset=1),
        },
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=77,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
            PD_DISPLAY_HALF_POWER,
        ],
        sensors={
            PD_EXPENDABLES_ANODE: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.DAYS,
            ),
        },
        program_data_fields={
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0),
            PD_LAST_PROGRAM: ProgramDataField(mode=1, min_value=1, max_value=1),
            PD_EXPENDABLES_ANODE: ProgramDataField(mode=2, min_value=0, max_value=2),
        },
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=80,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
            PD_DISPLAY_HALF_POWER,
        ],
        program_data_fields={
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0),
            PD_LAST_PROGRAM: ProgramDataField(mode=1, min_value=1, max_value=1),
            PD_EXPENDABLES_ANODE: ProgramDataField(mode=2, min_value=0, max_value=2),
        },
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=90,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
            PD_DISPLAY_HALF_POWER,
        ],
        sensors={
            PD_EXPENDABLES_ANODE: SensorConfig(
                device_class=SensorDeviceClass.DURATION,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.DAYS,
            ),
        },
        program_data_fields={
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0),
            PD_LAST_PROGRAM: ProgramDataField(mode=1, min_value=1, max_value=1),
            PD_EXPENDABLES_ANODE: ProgramDataField(mode=2, min_value=0, max_value=2),
        },
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=91,
        min_temp=35,
        max_temp=75,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ON: 3,
        },
        default_operation_mode=STATE_ON,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=2,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
            FEATURE_KEEP_WARM,
        ],
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=1),
        },
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=109,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
            FEATURE_KEEP_WARM,
        ],
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=1),
        },
    ),
    BoilerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=119,
        min_temp=30,
        max_temp=75,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
        binary_sensors=[
            FEATURE_ACCESS_CONTROL,
            FEATURE_ERROR,
        ],
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
            FEATURE_KEEP_WARM,
        ],
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=1),
        },
    ),
]

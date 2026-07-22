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
from pysyncleo.enums import UdpCommandType

from ..const import (
    FEATURE_BSS,
    FEATURE_EXPENDABLES_ANODE,
    FEATURE_KEEP_WARM,
    FEATURE_SMART_MODE,
    FEATURE_TANK,
    PD_EXPENDABLES_ANODE,
    PD_DISPLAY_HALF_POWER,
    PD_LAST_PROGRAM,
    PD_TURN_ON,
    PROFILE_TYPE_BOILER,
    VENDOR_RUSCLIMATE,
)
from .profiles import SensorConfig, WaterHeaterProfile, ProgramDataField

PROFILES = [
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=2,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
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
            FEATURE_KEEP_WARM,
        ],
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=1),
        },
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=7,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
            STATE_HEAT_PUMP: 5,
        },
        default_operation_mode=STATE_ECO,
        switches=[
            FEATURE_SMART_MODE,
            FEATURE_BSS,
        ],
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=12,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=35,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
            STATE_HEAT_PUMP: 5,
        },
        default_operation_mode=STATE_ECO,
        switches=[
            FEATURE_BSS,
        ],
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=16,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ELECTRIC: 1,
            STATE_PERFORMANCE: 2,
        },
        default_operation_mode=STATE_ELECTRIC,
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=18,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=35,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
            STATE_HEAT_PUMP: 5,
        },
        default_operation_mode=STATE_ECO,
        switches=[
            FEATURE_BSS,
        ],
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=19,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=35,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ON: 3,
        },
        default_operation_mode=STATE_ON,
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=33,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=35,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ECO: 1,
            STATE_ELECTRIC: 2,
            STATE_PERFORMANCE: 3,
        },
        default_operation_mode=STATE_ECO,
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
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=44,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
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
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=74,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
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
            FEATURE_KEEP_WARM,
        ],
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=1),
        },
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=76,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=35,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
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
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=77,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
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
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=80,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
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
        program_data_fields={
            PD_DISPLAY_HALF_POWER: ProgramDataField(mode=0),
            PD_LAST_PROGRAM: ProgramDataField(mode=1, min_value=1, max_value=1),
            PD_EXPENDABLES_ANODE: ProgramDataField(mode=2, min_value=0, max_value=2),
        },
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=90,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
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
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=91,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=35,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
        operation_modes_map={
            STATE_OFF: 0,
            STATE_ON: 3,
        },
        default_operation_mode=STATE_ON,
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=2,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
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
            FEATURE_KEEP_WARM,
        ],
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=1),
        },
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=109,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
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
            FEATURE_KEEP_WARM,
        ],
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=1),
        },
    ),
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=119,
        profile_type=PROFILE_TYPE_BOILER,
        min_temp=30,
        max_temp=75,
        target_temp_step=1.0,
        supported_features=(
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.ON_OFF
        ),
        cmd_mode=UdpCommandType.MODE,
        cmd_target_temp=UdpCommandType.TARGET_TEMPERATURE,
        cmd_current_temp=UdpCommandType.TEMPERATURE,
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
            FEATURE_KEEP_WARM,
        ],
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=1),
        },
    ),
]

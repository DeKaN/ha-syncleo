from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.water_heater import (
    STATE_ECO,
    STATE_ELECTRIC,
    STATE_OFF,
    STATE_PERFORMANCE,
    WaterHeaterEntityFeature,
)
from homeassistant.const import UnitOfTime, UnitOfVolume
from pysyncleo.enums import UdpCommandType

from ..const import (
    FEATURE_BSS,
    FEATURE_SMART_MODE,
    FEATURE_TANK,
    PD_EXPENDABLES_ANODE,
    PD_DISPLAY_HALF_POWER,
    PD_LAST_PROGRAM,
    VENDOR_RUSCLIMATE,
)
from .profiles import SensorConfig, WaterHeaterProfile, ProgramDataField

PROFILES = [
    WaterHeaterProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=90,
        profile_type="boiler",
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
            FEATURE_TANK: SensorConfig(
                device_class=SensorDeviceClass.VOLUME_STORAGE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfVolume.LITERS,
            ),
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
    )
]

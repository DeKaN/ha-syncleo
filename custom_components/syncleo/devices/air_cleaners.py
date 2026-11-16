from homeassistant.components.fan import FanEntityFeature
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfDensity,
    PERCENTAGE,
    STATE_OFF,
    UnitOfTemperature,
    UnitOfTime,
)
from pysyncleo.enums import UdpCommandType

from ..const import (
    PRESET_AUTO,
    PRESET_MANUAL,
    PRESET_NIGHT,
    FEATURE_EXPENDABLES_FILTER,
    FEATURE_TIMER,
    FEATURE_BACKLIGHT,
    FEATURE_CHILD_LOCK,
    FEATURE_CURRENT_HUMIDITY,
    FEATURE_ERROR,
    FEATURE_VOLUME,
    FEATURE_IONIZATION,
    FEATURE_ULTRAVIOLET,
    FEATURE_PM2,
    PROFILE_TYPE_AIRCLEANER,
    VENDOR_POLARIS,
    VENDOR_RUSCLIMATE,
)
from .profiles import (
    AirCleanerProfile,
    NumberConfig,
    ProgramDataField,
    SelectConfig,
    SensorConfig,
    TimeConfig,
)

PROFILES = [
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=1,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET,
        ],
        sensors={
            FEATURE_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
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
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=26,
        speed_count=4,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET,
        ],
        sensors={
            FEATURE_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
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
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=117,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_ULTRAVIOLET,
        ],
        sensors={
            FEATURE_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
        },
        times=[FEATURE_TIMER],
        time_configs={
            FEATURE_TIMER: TimeConfig(min_time=0, max_time=43200, default_time=0),
        },
    ),
    AirCleanerProfile(
        vendor=VENDOR_POLARIS,
        device_type=140,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_VOLUME,
        ],
        sensors={
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
        times=[FEATURE_TIMER],
        time_configs={
            FEATURE_TIMER: TimeConfig(min_time=0, max_time=43200, default_time=0),
        },
    ),
    AirCleanerProfile(
        vendor=VENDOR_POLARIS,
        device_type=151,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_MANUAL: 2,
            PRESET_NIGHT: 3,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_VOLUME,
            FEATURE_CHILD_LOCK,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET
        ],
        sensors={
            FEATURE_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
        },
        times=[FEATURE_TIMER],
        time_configs={
            FEATURE_TIMER: TimeConfig(min_time=0, max_time=43200, default_time=0),
        },
    ),
    AirCleanerProfile(
        vendor=VENDOR_POLARIS,
        device_type=152,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_MANUAL: 2,
            PRESET_NIGHT: 3,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_VOLUME,
            FEATURE_CHILD_LOCK,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET
        ],
        sensors={
            FEATURE_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
        },
        times=[FEATURE_TIMER],
        time_configs={
            FEATURE_TIMER: TimeConfig(min_time=0, max_time=43200, default_time=0),
        },
    ),
    AirCleanerProfile(
        vendor=VENDOR_POLARIS,
        device_type=172,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_VOLUME,
        ],
        sensors={
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
        times=[FEATURE_TIMER],
        time_configs={
            FEATURE_TIMER: TimeConfig(min_time=0, max_time=43200, default_time=0),
        },
    ),
    AirCleanerProfile(
        vendor=VENDOR_POLARIS,
        device_type=203,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_MANUAL: 2,
            PRESET_NIGHT: 3,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_VOLUME,
            FEATURE_CHILD_LOCK,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET
        ],
        sensors={
            FEATURE_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
        },
        times=[FEATURE_TIMER],
        time_configs={
            FEATURE_TIMER: TimeConfig(min_time=0, max_time=43200, default_time=0),
        },
    ),
    AirCleanerProfile(
        vendor=VENDOR_POLARIS,
        device_type=204,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_MANUAL: 2,
            PRESET_NIGHT: 3,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_VOLUME,
            FEATURE_CHILD_LOCK,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET
        ],
        sensors={
            FEATURE_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
        },
        times=[FEATURE_TIMER],
        time_configs={
            FEATURE_TIMER: TimeConfig(min_time=0, max_time=43200, default_time=0),
        },
    ),
    AirCleanerProfile(
        vendor=VENDOR_POLARIS,
        device_type=250,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_MANUAL: 2,
            PRESET_NIGHT: 3,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_VOLUME,
            FEATURE_CHILD_LOCK,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET
        ],
        sensors={
            FEATURE_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
        },
        times=[FEATURE_TIMER],
        time_configs={
            FEATURE_TIMER: TimeConfig(min_time=0, max_time=43200, default_time=0),
        },
    ),
    AirCleanerProfile(
        vendor=VENDOR_POLARIS,
        device_type=251,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_MANUAL: 2,
            PRESET_NIGHT: 3,
        },
        default_preset_mode=PRESET_AUTO,
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_VOLUME,
            FEATURE_CHILD_LOCK,
            FEATURE_IONIZATION,
            FEATURE_ULTRAVIOLET
        ],
        sensors={
            FEATURE_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
        },
        times=[FEATURE_TIMER],
        time_configs={
            FEATURE_TIMER: TimeConfig(min_time=0, max_time=43200, default_time=0),
        },
    ),
]
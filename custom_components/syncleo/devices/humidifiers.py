from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.humidifier import (
    HumidifierDeviceClass,
    HumidifierEntity,
    HumidifierEntityFeature,
)
from homeassistant.components.number import NumberDeviceClass, NumberEntityDescription
from homeassistant.const import (
    EntityCategory,
    PERCENTAGE,
    STATE_OFF,
    UnitOfTemperature,
    UnitOfTime,
)

from ..const import (
    FEATURE_BACKLIGHT,
    FEATURE_CHILD_LOCK,
    FEATURE_CURRENT_TEMPERATURE,
    FEATURE_CURRENT_HUMIDITY,
    FEATURE_ERROR,
    FEATURE_EXPENDABLES_FILTER,
    FEATURE_EXPENDABLES_CLEAN,
    FEATURE_IONIZATION,
    FEATURE_NIGHT,
    FEATURE_SPEED,
    FEATURE_TIMER,
    FEATURE_ULTRAVIOLET,
    FEATURE_VOLUME,
    FEATURE_WARM_STREAM,
    FEATURE_HUMIDIFIER_INTENSITY,
    PRESET_AUTO,
    PRESET_HEALTH,
    PRESET_BABY,
    PRESET_NIGHT,
    PRESET_TURBO,
    PRESET_MANUAL,
    PRESET_ECO,
    PRESET_FITNES, 
    PRESET_YOGA, 
    PRESET_MEDITATION, 
    PRESET_PRANA_HANDS, 
    PRESET_PRANA_AUTO, 
    PRESET_AROMA,
    PD_BACKLIGHT_BLUE,
    PD_BACKLIGHT_GREEN,
    PD_BACKLIGHT_RED,
    PROFILE_TYPE_HUMIDIFIER,
    VENDOR_RUSCLIMATE,
    VENDOR_POLARIS,
)

from .profiles import (
    HumidifierProfile,
    NumberConfig,
    ProgramDataField,
    SensorConfig,
    SwitchConfig,
    TimeConfig,
    LightConfig,
)

PROFILES = [
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=4,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_HEALTH: 2,
            PRESET_BABY: 3,
            PRESET_NIGHT: 4,
            PRESET_TURBO: 5,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=7),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=15,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=7),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=17,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_HEALTH: 2,
            PRESET_BABY: 3,
            PRESET_NIGHT: 4,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=7),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=18,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_HEALTH: 2,
            PRESET_BABY: 3,
            PRESET_NIGHT: 4,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=7),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=25,
        preset_modes_map={
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_ECO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=44,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_HEALTH: 2,
            PRESET_BABY: 3,
            PRESET_NIGHT: 4,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=7),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=70,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_HEALTH: 2,
            PRESET_BABY: 3,
            PRESET_NIGHT: 4,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=7),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
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
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=71,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=72,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 4,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=73,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=74,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 4,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=75,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=87,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 4,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=99,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=137,
        preset_modes_map={
            PRESET_TURBO: 5,
        },
        default_preset_mode=PRESET_TURBO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=147,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 4,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=7),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=153,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_TURBO: 5,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=155,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 4,
            PRESET_TURBO: 5,
            PRESET_MANUAL: 6,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
        ],
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=157,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_TURBO: 5,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_POLARIS,
        device_type=158,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_TURBO: 5,
            PRESET_ECO: 7,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=0, max_value=3),
        },
        switches=[
            FEATURE_NIGHT,
            FEATURE_CHILD_LOCK,
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_EXPENDABLES_CLEAN: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[1] if isinstance(val, list) and len(val) > 1 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=4,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_BABY: 4,
            PRESET_HEALTH: 5,
            PRESET_FITNES: 6, 
            PRESET_YOGA: 7, 
            PRESET_MEDITATION: 8, 
            PRESET_PRANA_HANDS: 9, 
            PRESET_PRANA_AUTO: 10, 
            PRESET_AROMA: 11,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=1, max_value=3),
        },
        switches=[
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
            FEATURE_ULTRAVIOLET,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
        lights={
            FEATURE_BACKLIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=35,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
            PRESET_NIGHT: 3,
            PRESET_BABY: 4,
            PRESET_HEALTH: 5,
            PRESET_FITNES: 6, 
            PRESET_YOGA: 7, 
            PRESET_MEDITATION: 8, 
            PRESET_PRANA_HANDS: 9, 
            PRESET_PRANA_AUTO: 10, 
            PRESET_AROMA: 11,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=1, max_value=3),
        },
        switches=[
            FEATURE_VOLUME,
            FEATURE_IONIZATION,
            FEATURE_WARM_STREAM,
            FEATURE_ULTRAVIOLET,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTime.HOURS,
                value_fn=lambda val: (
                    val[0] if isinstance(val, list) and len(val) > 0 else None
                ),
            ),
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
                translation_key="current_temperature_humidifier",
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
        lights={
            FEATURE_BACKLIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
            ),
        },
    ),
    HumidifierProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=81,
        preset_modes_map={
            PRESET_MANUAL: 1,
            PRESET_AUTO: 2,
        },
        default_preset_mode=PRESET_AUTO,
        numbers=[FEATURE_HUMIDIFIER_INTENSITY],
        number_configs={
            FEATURE_HUMIDIFIER_INTENSITY: NumberConfig(min_value=1, max_value=3),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_NIGHT,
            FEATURE_WARM_STREAM,
        ],
        switch_configs={
            FEATURE_WARM_STREAM: SwitchConfig(translation_key="humidifier_warm_stream"),
        },
        sensors={
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
        },
    ),
]
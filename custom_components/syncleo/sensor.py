import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .devices import SensorConfig, SensorMixin
from .entity import FEATURE_TO_COMMAND_MAP, SyncleoBaseEntity
from .utils import get_device_profile

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Syncleo sensor platform."""
    conn = entry.runtime_data
    profile = get_device_profile(conn.device)

    if isinstance(profile, SensorMixin) and profile.sensors:
        entities = [
            SyncleoSensor(conn, profile, entry, feature_key, config)
            for feature_key, config in profile.sensors.items()
        ]
        async_add_entities(entities)


class SyncleoSensor(SyncleoBaseEntity, SensorEntity):
    def __init__(
        self, connection, profile, entry, feature_key: str, config: SensorConfig
    ):
        super().__init__(connection, profile, entry)

        self._feature_key = feature_key
        self._is_program_data = feature_key in profile.program_data_fields
        self._cmd_class = FEATURE_TO_COMMAND_MAP.get(feature_key)

        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        self._attr_translation_key = feature_key

        self._attr_device_class = config.device_class
        self._attr_state_class = config.state_class
        self._attr_native_unit_of_measurement = config.unit_of_measurement

        self._value = None

    async def async_added_to_hass(self):
        self._connection.register_callback(self._handle_device_update)

    async def async_will_remove_from_hass(self):
        self._connection.unregister_callback(self._handle_device_update)

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        value = self._value
        if self._is_program_data:
            data = self.get_program_data(self._feature_key)
            _LOGGER.info(
                "Handle program data update for device %s, received data: %s",
                self._attr_unique_id,
                data.hex(),
            )
            value = int.from_bytes(data, byteorder="little") if data else None

        elif self._cmd_class and cmd.command_type == self._cmd_class.command_type:
            _LOGGER.info(
                "Handle update for device %s, received command: %s",
                self._attr_unique_id,
                cmd,
            )
            value = cmd.value
        else:
            _LOGGER.debug(
                "Entity %s ignoring unrelated cmd: %s", self._attr_unique_id, cmd
            )

        if value != self._value:
            self._value = value
            self.async_write_ha_state()

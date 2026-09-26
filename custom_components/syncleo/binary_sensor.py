import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .devices import BinarySensorMixin
from .entity import FEATURE_TO_COMMAND_MAP, SyncleoBaseEntity
from .utils import get_device_profile_by_device

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    conn = entry.runtime_data
    profile = get_device_profile_by_device(conn.device)

    if isinstance(profile, BinarySensorMixin) and profile.binary_sensors:
        entities = [
            SyncleoBinarySensor(conn, profile, entry, feature_key)
            for feature_key in profile.binary_sensors
        ]
        async_add_entities(entities)


class SyncleoBinarySensor(SyncleoBaseEntity, BinarySensorEntity):
    def __init__(self, connection, profile, entry, feature_key: str):
        super().__init__(connection, profile, entry)

        self._feature_key = feature_key
        self._is_program_data = feature_key in profile.program_data_fields
        self._cmd_class = FEATURE_TO_COMMAND_MAP.get(feature_key)

        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        self._attr_translation_key = feature_key
        self._is_on: bool | None = None if self._is_program_data else False

    @property
    def is_on(self) -> bool | None:
        return self._is_on

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        is_on = self._is_on

        if self._is_program_data:
            data = self.get_program_data(self._feature_key)
            is_on = int.from_bytes(data, byteorder="little") != 0

        elif self._cmd_class and cmd.command_type == self._cmd_class.command_type:
            _LOGGER.debug(
                "Handle update for device %s, received command: %s",
                self._attr_unique_id,
                cmd,
            )
            is_on = bool(cmd.value)

        if is_on != self._is_on:
            self._is_on = is_on
            self.async_write_ha_state()

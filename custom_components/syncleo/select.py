import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .devices import SelectConfig, SelectMixin
from .entity import FEATURE_TO_COMMAND_MAP, SyncleoBaseEntity
from .utils import get_device_profile

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    conn = entry.runtime_data
    profile = get_device_profile(conn.device)

    if isinstance(profile, SelectMixin) and profile.selects:
        entities = [
            SyncleoSelect(conn, profile, entry, feature_key, config)
            for feature_key, config in profile.selects.items()
            if feature_key in FEATURE_TO_COMMAND_MAP
        ]
        async_add_entities(entities)


class SyncleoSelect(SyncleoBaseEntity, SelectEntity):
    def __init__(
        self, connection, profile, entry, feature_key: str, config: SelectConfig
    ):
        super().__init__(connection, profile, entry)

        self._feature_key = feature_key
        self._is_program_data = feature_key in profile.program_data_fields
        self._cmd_class = FEATURE_TO_COMMAND_MAP.get(feature_key)

        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        self._attr_translation_key = feature_key

        self._options_map = config.options_map
        self._attr_options = config.options

        self._rev_options_map = {v: k for k, v in self._options_map.items()}

        self._current_option = None

    @property
    def current_option(self) -> str | None:
        return self._current_option

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        current_option = self._current_option

        if self._is_program_data:
            data = self.get_program_data(self._feature_key)
            _LOGGER.info(
                "Handle program data update for device %s, received data: %s",
                self._attr_unique_id,
                data.hex(),
            )
            value = int.from_bytes(data, byteorder="little") if data else 0

        elif self._cmd_class and cmd.command_type == self._cmd_class.command_type:
            _LOGGER.info(
                "Handle update for device %s, received command: %s",
                self._attr_unique_id,
                cmd,
            )
            value = int(cmd.value)

        text_value = self._rev_options_map.get(value)

        if text_value is not None:
            current_option = text_value

        if current_option != self._current_option:
            self._current_option = current_option
            self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        value = self._options_map.get(option)

        if value is None:
            _LOGGER.error("Invalid option %s for %s", option, self._feature_key)
            return

        if self._is_program_data:
            field_config = self._profile.program_data_fields[self._feature_key]
            data = value.to_bytes(field_config.size, byteorder="little")

            await self.async_set_program_data(self._feature_key, data)
        elif self._cmd_class:
            await self.async_send_command(self._cmd_class(value))

        self._current_option = option
        self.async_write_ha_state()

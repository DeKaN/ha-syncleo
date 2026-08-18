import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MAC
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pysyncleo.commands import CmdDataSource, DataSource

from .const import CONF_IS_VIRTUAL, DATASOURCE_PRESET_NONE, DOMAIN, VIRTUAL_DEVICE_TYPE
from .devices import SelectConfig, SelectMixin
from .entity import FEATURE_TO_COMMAND_MAP, SyncleoBaseEntity
from .utils import get_device_profile_by_device

_LOGGER = logging.getLogger(__name__)
_MAC_NONE = "00:00:00:00:00:00"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    conn = entry.runtime_data
    profile = get_device_profile_by_device(conn.device)

    if isinstance(profile, SelectMixin) and profile.selects:
        entities = [
            SyncleoSelect(conn, profile, entry, feature_key, config)
            for feature_key, config in profile.selects.items()
        ]
        async_add_entities(entities)


class SyncleoSelect(SyncleoBaseEntity, SelectEntity):
    def __init__(
        self, connection, profile, entry, feature_key: str, config: SelectConfig
    ):
        super().__init__(connection, profile, entry)

        self._feature_key = feature_key
        self._config = config
        self._is_program_data = feature_key in profile.program_data_fields
        self._is_data_source = feature_key in profile.data_source_features
        self._cmd_class = FEATURE_TO_COMMAND_MAP.get(feature_key)

        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        self._attr_translation_key = feature_key

        self._options_map = config.options_map
        self._attr_options = config.options

        self._rev_options_map = {v: k for k, v in self._options_map.items()}

        self._current_option: str | None = None
        self._cached_data_source: dict[str, DataSource | None] = {
            f: None for f in profile.data_source_features
        }

    @property
    def _virtual_sensors(self) -> dict[str, str]:
        sensors = {_MAC_NONE: DATASOURCE_PRESET_NONE}

        for config_entry in self.hass.config_entries.async_entries(DOMAIN):
            if config_entry.data.get(CONF_IS_VIRTUAL):
                mac = config_entry.data.get(CONF_MAC, _MAC_NONE).lower()
                sensors[mac] = config_entry.title

        return sensors

    @property
    def options(self) -> list[str]:
        return (
            list(self._virtual_sensors.values())
            if self._is_data_source
            else self._config.options
        )

    @property
    def current_option(self) -> str | None:
        return (
            self._virtual_sensors.get(self._current_option, DATASOURCE_PRESET_NONE)
            if self._is_data_source and self._current_option
            else self._current_option
        )

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        current_option = self._current_option

        if self._is_data_source and isinstance(cmd, CmdDataSource):
            cmd.map_features(self._profile.data_source_features)
            self._cached_data_source |= cmd.value

            source = cmd.value.get(self._feature_key)
            reported_mac = source.mac if source and source.mac else _MAC_NONE

            if self._current_option != reported_mac:
                self._current_option = reported_mac
                self.async_write_ha_state()
                return

        elif self._is_program_data:
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
        else:
            _LOGGER.debug(
                "Entity %s ignoring unrelated cmd: %s", self._attr_unique_id, cmd
            )
            return

        text_value = self._rev_options_map.get(value)

        if text_value is not None:
            current_option = text_value

        if current_option != self._current_option:
            self._current_option = current_option
            self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        if self._is_data_source:
            mac = next(
                (m for m, title in self._virtual_sensors.items() if title == option),
                _MAC_NONE,
            )

            self._cached_data_source[self._feature_key] = DataSource(
                mac=mac, device_type=VIRTUAL_DEVICE_TYPE
            )
            cmd = CmdDataSource(self._cached_data_source)
            await self.async_send_command(cmd)

            self._current_option = mac
            self.async_write_ha_state()
            return

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

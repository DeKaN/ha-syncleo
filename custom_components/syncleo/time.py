import logging
from datetime import time
from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .devices import TimeMixin
from .entity import FEATURE_TO_COMMAND_MAP, SyncleoBaseEntity
from .utils import get_device_profile

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Syncleo time platform."""
    conn = entry.runtime_data
    profile = get_device_profile(conn.device)

    if isinstance(profile, TimeMixin) and profile.times:
        entities = [
            SyncleoTime(conn, profile, entry, feature_key)
            for feature_key in profile.times
        ]
        async_add_entities(entities)


class SyncleoTime(SyncleoBaseEntity, TimeEntity):
    def __init__(self, conn, profile, entry, feature_key: str):
        super().__init__(conn, profile, entry)
        self._feature_key = feature_key
        self._is_program_data = feature_key in profile.program_data_fields
        self._cmd_class = FEATURE_TO_COMMAND_MAP.get(feature_key)
        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        
        if isinstance(profile, TimeMixin) and feature_key in profile.time_configs:
            config = profile.time_configs.get(feature_key)

        if config:
            self._attr_translation_key = config.translation_key if config.translation_key else feature_key
            self._min_time = config.min_time if config.min_time else 0
            self._max_time = config.max_time if config.max_time else 43200
            self._default_time = config.default_time if config.default_time else 0
        else:
            _LOGGER.warning(
                "No number_config found for %s, using defaults", feature_key
            )
            self._attr_translation_key = feature_key
            self._min_time = 0
            self._max_time = 43200
            self._default_time = 0
        hours = self._default_time // 3600
        minutes = (self._default_time % 3600) // 60
        seconds = self._default_time % 60
        self._attr_native_value = time(hours, minutes, seconds)
        self._value = self._min_time

    @property
    def native_value(self) -> time | None:
        return self._attr_native_value

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        value = self._value

        if self._cmd_class and cmd.command_type == self._cmd_class.command_type:
            value = cmd.value
            _LOGGER.info(
                "Handle command update for device %s, raw: %s, processed: %s",
                self._attr_unique_id,
                cmd.value,
                value,
            )
        else:
            _LOGGER.info(
                "Entity %s ignoring unrelated cmd: %s", self._attr_unique_id, cmd
            )

        if value != self._value:
            self._value = value
            hours = value // 3600
            minutes = (value % 3600) // 60
            seconds = value % 60
            self._attr_native_value = time(hours, minutes, seconds)
            self.async_write_ha_state()

    async def async_set_value(self, value: time) -> None:
        """Update the time."""
        
        if self._cmd_class:
            value_hour=value.hour
            value_minute=value.minute
            value_second=0
            value_in_seconds = value.hour * 3600 + value.minute * 60
            if value_in_seconds > self._max_time:
                value_in_seconds = self._max_time
            await self.async_send_command(self._cmd_class(value_in_seconds))
        else:
            _LOGGER.error(
                "No command class or program data field defined for feature: %s",
                self._feature_key,
            )
            return
        self._value = value
        self.async_write_ha_state()



"""Humidifier platform for Syncleo devices."""

import logging
from typing import Any

from homeassistant.components.humidifier import HumidifierDeviceClass, HumidifierEntity
from homeassistant.const import STATE_OFF
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pysyncleo.commands import CmdMode, CmdTargetHumidity
from pysyncleo.enums import UdpCommandType

from .const import TRANSLATION_KEY_HUMIDIFIER
from .devices import HumidifierProfile
from .entity import SyncleoBaseEntity
from .models import SyncleoConfigEntry
from .utils import get_device_profile_by_device

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SyncleoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    connection = entry.runtime_data
    profile = get_device_profile_by_device(connection.device)
    if isinstance(profile, HumidifierProfile):
        async_add_entities([SyncleoHumidifier(connection, profile, entry)])


class SyncleoHumidifier(SyncleoBaseEntity, HumidifierEntity):
    _attr_name = None
    _attr_should_poll = False
    _attr_translation_key = TRANSLATION_KEY_HUMIDIFIER
    _attr_device_class = HumidifierDeviceClass.HUMIDIFIER

    def __init__(
        self, connection, profile: HumidifierProfile, entry: SyncleoConfigEntry
    ) -> None:
        super().__init__(connection, profile, entry)
        self._attr_unique_id = f"{self._device_unique_id}_{profile.profile_type}"
        self._attr_supported_features = profile.supported_features
        self._attr_min_humidity = profile.min_humidity
        self._attr_max_humidity = profile.max_humidity
        self._attr_target_humidity_step = profile.target_humidity_step
        self._attr_available_modes = list(profile.modes_map)
        self._rev_modes_map = {value: key for key, value in profile.modes_map.items()}
        self._attr_is_on = False
        self._attr_mode = STATE_OFF

    @callback
    def _handle_device_update(self, command):
        super()._handle_device_update(command)
        if command.command_type == UdpCommandType.MODE:
            raw_mode = int(command.value)
            self._attr_is_on = raw_mode != 0
            self._attr_mode = (
                self._rev_modes_map.get(raw_mode) if raw_mode else STATE_OFF
            )
        elif command.command_type == UdpCommandType.CURRENT_HUMIDITY:
            self._attr_current_humidity = float(command.value)
        elif command.command_type == UdpCommandType.TARGET_HUMIDITY:
            self._attr_target_humidity = float(command.value)
        else:
            return
        _LOGGER.debug("Handled update for %s: %s", self._attr_unique_id, command)
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        field_key = self._profile.turn_on_program_data_field
        if field_key is None:
            await self.async_set_mode(self._profile.default_mode)
            return

        field = self._profile.program_data_fields[field_key]
        await self.async_set_program_data_fields(
            {field_key: True.to_bytes(field.size, byteorder="little")}
        )
        self._attr_is_on = True
        if self._attr_mode == STATE_OFF:
            self._attr_mode = None
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.async_send_command(CmdMode(0))
        self._attr_is_on = False
        self._attr_mode = STATE_OFF
        self.async_write_ha_state()

    async def async_set_mode(self, mode: str) -> None:
        raw_mode = self._profile.modes_map.get(mode)
        if raw_mode is not None:
            await self.async_send_command(CmdMode(raw_mode))
            self._attr_is_on = True
            self._attr_mode = mode
            self.async_write_ha_state()

    async def async_set_humidity(self, humidity: int) -> None:
        await self.async_send_command(CmdTargetHumidity(humidity))
        self._attr_target_humidity = humidity
        self.async_write_ha_state()

import logging
import math
from typing import Any

from homeassistant.components.fan import FanEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.util.percentage import (
    percentage_to_ranged_value,
    ranged_value_to_percentage,
)

from pysyncleo.commands import CmdMode, CmdSpeed, UdpCommandType

from .const import TRANLATION_KEY_FAN
from .devices import BreezerProfile
from .entity import SyncleoBaseEntity
from .models import SyncleoConfigEntry
from .utils import get_device_profile

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: SyncleoConfigEntry, async_add_entities
):
    conn = entry.runtime_data
    profile = get_device_profile(conn.device)

    if isinstance(profile, BreezerProfile):
        async_add_entities([SyncleoFan(conn, profile, entry)])


class SyncleoFan(SyncleoBaseEntity, FanEntity):
    _attr_name = None
    _attr_translation_key = TRANLATION_KEY_FAN

    def __init__(
        self,
        connection,
        profile: BreezerProfile,
        entry: SyncleoConfigEntry,
    ):
        super().__init__(connection, profile, entry)

        self._profile = profile
        self._attr_unique_id = f"{self._device_unique_id}_{profile.profile_type}"
        self._attr_supported_features = profile.supported_features
        self._attr_speed_count = profile.speed_count

        self._attr_preset_modes = list(profile.preset_modes_map.keys())
        self._rev_preset_map = {v: k for k, v in profile.preset_modes_map.items()}

        self._is_on = False
        self._current_preset_mode = None
        self._raw_speed = 0
        self._speed_range = (1, profile.speed_count)

    @property
    def is_on(self) -> bool | None:
        return self._is_on

    @property
    def preset_mode(self) -> str | None:
        return self._current_preset_mode

    @property
    def percentage(self) -> int | None:
        if not self._is_on or self._raw_speed == 0:
            return 0

        return ranged_value_to_percentage(self._speed_range, self._raw_speed)

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        update_needed = False

        if cmd.command_type == UdpCommandType.MODE:
            raw_val = int(cmd.value)

            if raw_val == 0:
                self._is_on = False
                self._current_preset_mode = None
            else:
                self._is_on = True
                self._current_preset_mode = self._rev_preset_map.get(raw_val)
            update_needed = True

        elif cmd.command_type == UdpCommandType.SPEED:
            self._raw_speed = int(cmd.value)
            update_needed = True

        else:
            _LOGGER.debug(
                "Entity %s ignoring unrelated cmd: %s", self._attr_unique_id, cmd
            )

        if update_needed:
            _LOGGER.info(
                "Handled update for device %s, received command: %s",
                self._attr_unique_id,
                cmd,
            )
            self.async_write_ha_state()

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        if preset_mode:
            await self.async_set_preset_mode(preset_mode)
        elif percentage is not None:
            await self.async_set_percentage(percentage)
        else:
            await self.async_set_preset_mode(self._profile.default_preset_mode)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.async_send_command(CmdMode(0))

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        raw_val = self._profile.preset_modes_map.get(preset_mode)
        if raw_val is not None:
            await self.async_send_command(CmdMode(raw_val))

    async def async_set_percentage(self, percentage: int) -> None:
        if percentage == 0:
            await self.async_turn_off()
            return

        raw_speed = math.ceil(percentage_to_ranged_value(self._speed_range, percentage))
        await self.async_send_command(CmdSpeed(raw_speed))

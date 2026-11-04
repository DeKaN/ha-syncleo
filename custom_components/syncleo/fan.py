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
from .devices import AirCleanerProfile, VentilationProfile
from .entity import SyncleoBaseEntity
from .models import SyncleoConfigEntry
from .utils import get_device_profile_by_device

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: SyncleoConfigEntry, async_add_entities
):
    conn = entry.runtime_data
    profile = get_device_profile_by_device(conn.device)

    if isinstance(profile, (AirCleanerProfile, VentilationProfile)):
        async_add_entities([SyncleoFan(conn, profile, entry)])


class SyncleoFan(SyncleoBaseEntity, FanEntity):
    _attr_name = None
    _attr_translation_key = TRANLATION_KEY_FAN

    def __init__(
        self,
        connection,
        profile: AirCleanerProfile | VentilationProfile,
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
        self._current_preset_mode: str | None = None
        self._raw_speed: int | None = (
            None if profile.speed_preset_mode is not None else 0
        )
        self._speed_range = (
            profile.min_speed,
            profile.min_speed + profile.speed_count - 1,
        )

    @property
    def is_on(self) -> bool | None:
        return self._is_on

    @property
    def preset_mode(self) -> str | None:
        if self._current_preset_mode == self._profile.speed_preset_mode:
            return None
        return self._current_preset_mode

    @property
    def percentage(self) -> int | None:
        if not self._is_on:
            return 0

        if (
            self._profile.speed_preset_mode is not None
            and self._current_preset_mode != self._profile.speed_preset_mode
        ):
            return None
        if self._raw_speed is None:
            return None
        if self._raw_speed == 0 and self._profile.speed_preset_mode is None:
            return 0
        if (
            self._profile.speed_preset_mode is not None
            and not self._speed_range[0] <= self._raw_speed <= self._speed_range[1]
        ):
            return None

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
            _LOGGER.debug(
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
            field_key = self._profile.turn_on_preset_field
            last_program = self.get_known_program_data(field_key) if field_key else None
            if last_program is not None:
                await self.async_send_command(
                    CmdMode(int.from_bytes(last_program, byteorder="little"))
                )
            else:
                await self.async_set_preset_mode(self._profile.default_preset_mode)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.async_send_command(CmdMode(0))

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        raw_val = self._profile.preset_modes_map.get(preset_mode)
        if raw_val is not None:
            await self.async_send_command(CmdMode(raw_val))
            speed = self._profile.preset_speeds.get(preset_mode)
            if speed is not None:
                await self.async_send_command(CmdSpeed(speed))

    async def async_set_percentage(self, percentage: int) -> None:
        if percentage == 0:
            await self.async_turn_off()
            return

        raw_speed = math.ceil(percentage_to_ranged_value(self._speed_range, percentage))
        preset = self._profile.speed_preset_mode
        if preset is not None and self._current_preset_mode != preset:
            await self.async_send_command(
                CmdMode(self._profile.preset_modes_map[preset])
            )
        await self.async_send_command(CmdSpeed(raw_speed))

import logging
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    SWING_BOTH,
    SWING_HORIZONTAL,
    SWING_OFF,
    SWING_VERTICAL,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback

from pysyncleo.commands import CmdTargetTemperature, CmdMode, CmdSpeed


from .const import PD_SWING_MODE, TRANLATION_KEY_CLIMATE
from .devices import ClimateProfile
from .entity import SyncleoBaseEntity
from .models import SyncleoConfigEntry
from .utils import get_device_profile

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: SyncleoConfigEntry, async_add_entities
):
    conn = entry.runtime_data
    profile = get_device_profile(conn.device)

    if isinstance(profile, ClimateProfile):
        async_add_entities([SyncleoClimate(conn, profile, entry)])


class SyncleoClimate(SyncleoBaseEntity, ClimateEntity):
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_name = None
    _attr_translation_key = TRANLATION_KEY_CLIMATE

    def __init__(self, connection, profile: ClimateProfile, entry: SyncleoConfigEntry):
        super().__init__(connection, profile, entry)

        self._profile = profile
        self._attr_unique_id = f"{self._device_unique_id}_{profile.profile_type}"
        self._attr_min_temp = profile.min_temp
        self._attr_max_temp = profile.max_temp
        self._attr_target_temperature_step = profile.target_temp_step
        self._attr_supported_features = profile.supported_features

        self._attr_hvac_modes = list(profile.hvac_modes_map.keys())
        self._rev_hvac_map = {v: k for k, v in profile.hvac_modes_map.items()}
        self._rev_presets_map = {v: k for k, v in profile.preset_modes_map.items()}

        if profile.fan_modes_map:
            self._attr_fan_modes = list(profile.fan_modes_map.keys())
            self._rev_fan_map = {v: k for k, v in profile.fan_modes_map.items()}

        if profile.preset_modes_map:
            self._attr_preset_modes = list(profile.preset_modes_map.keys())

        if profile.supported_swing_modes:
            self._attr_swing_modes = profile.supported_swing_modes

        self._is_on = False
        self._current_hvac_mode = HVACMode.OFF
        self._current_preset_mode = None
        self._target_temp = None
        self._current_temp = None
        self._fan_mode = None

    @property
    def hvac_mode(self) -> HVACMode:
        return self._current_hvac_mode

    @property
    def preset_mode(self) -> str | None:
        return self._current_preset_mode

    @property
    def target_temperature(self) -> float | None:
        return self._target_temp

    @property
    def current_temperature(self) -> float | None:
        return self._current_temp

    @property
    def fan_mode(self) -> str | None:
        return self._fan_mode

    @property
    def swing_mode(self) -> str | None:
        field = self._profile.program_data_fields.get(PD_SWING_MODE)
        if not field or field.size != 2:
            return None

        raw_bytes = self.get_program_data(PD_SWING_MODE)

        if len(raw_bytes) < 2:
            return SWING_OFF

        horizontal = raw_bytes[0] > 0
        vertical = raw_bytes[1] > 0

        if horizontal and vertical:
            return SWING_BOTH
        if vertical:
            return SWING_VERTICAL
        if horizontal:
            return SWING_HORIZONTAL

        return SWING_OFF

    async def async_added_to_hass(self):
        self._connection.register_callback(self._handle_device_update)

    async def async_will_remove_from_hass(self):
        self._connection.unregister_callback(self._handle_device_update)

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)
        update_needed = False

        if cmd.command_type == self._profile.cmd_mode:
            raw_val = int(cmd.value)
            resolved_mode = self._rev_hvac_map.get(raw_val)
            resolved_preset = self._rev_presets_map.get(raw_val)
            _LOGGER.info(
                "Mode change for device %s: raw=%s, resolved_mode=%s, resolved_preset=%s",
                self._attr_unique_id,
                raw_val,
                resolved_mode,
                resolved_preset,
            )

            if resolved_mode:
                self._current_hvac_mode = resolved_mode

            if resolved_preset:
                self._current_preset_mode = resolved_preset
                if self._current_hvac_mode == HVACMode.OFF:
                    self._current_hvac_mode = self._profile.default_hvac_mode

            self._is_on = self._current_hvac_mode != HVACMode.OFF
            if not self._is_on:
                self._current_preset_mode = None

            update_needed = True

        elif cmd.command_type == self._profile.cmd_target_temp:
            self._target_temp = float(cmd.value)
            update_needed = True

        elif (
            self._profile.cmd_current_temp
            and cmd.command_type == self._profile.cmd_current_temp
        ):
            self._current_temp = float(cmd.value)
            update_needed = True

        elif (
            self._profile.cmd_fan_mode
            and cmd.command_type == self._profile.cmd_fan_mode
        ):
            self._fan_mode = self._rev_fan_map.get(int(cmd.value))
            update_needed = True

        if update_needed:
            _LOGGER.info(
                "Handled update for device %s, received command: %s",
                self._attr_unique_id,
                cmd,
            )
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        await self.async_set_hvac_mode(self._profile.default_hvac_mode)

    async def async_turn_off(self, **kwargs):
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_set_hvac_mode(self, hvac_mode: HVACMode):
        raw_val = self._profile.hvac_modes_map.get(hvac_mode)
        if raw_val is not None:
            await self._connection.send_command(CmdMode(raw_val))
            self._current_hvac_mode = hvac_mode
            self._is_on = hvac_mode != HVACMode.OFF
            self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs):
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is not None:
            temp = max(self._attr_min_temp, min(self._attr_max_temp, float(temp)))
            await self._connection.send_command(CmdTargetTemperature(temp))
            self._current_temp = temp
            self.async_write_ha_state()

    async def async_set_fan_mode(self, fan_mode: str):
        raw_val = self._profile.fan_modes_map.get(fan_mode)
        if raw_val is not None:
            await self._connection.send_command(CmdSpeed(raw_val))

    async def async_set_swing_mode(self, swing_mode: str):
        field = self._profile.program_data_fields.get(PD_SWING_MODE)
        if not field or field.size != 2:
            return

        h_val = swing_mode in (SWING_HORIZONTAL, SWING_BOTH)
        v_val = swing_mode in (SWING_VERTICAL, SWING_BOTH)

        packed_bytes = bytes([h_val, v_val])

        await self.async_set_program_data(PD_SWING_MODE, packed_bytes)

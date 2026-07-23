import logging
from typing import Any

from homeassistant.components.water_heater import WaterHeaterEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, STATE_OFF, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from pysyncleo.commands import CmdTargetTemperature, CmdMode, UdpCommandType

from .const import DOMAIN
from .devices import WaterHeaterProfile
from .entity import SyncleoBaseEntity
from .utils import get_device_profile


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Syncleo water heater platform."""
    conn = entry.runtime_data
    profile = get_device_profile(conn.device)

    if isinstance(profile, WaterHeaterProfile):
        async_add_entities([SyncleoWaterHeater(conn, profile, entry)])


class SyncleoWaterHeater(SyncleoBaseEntity, WaterHeaterEntity):
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_name = None

    def __init__(self, connection, profile: WaterHeaterProfile, entry):
        """Initialize the water heater entity."""
        super().__init__(connection, profile, entry)

        self._profile = profile
        self._attr_unique_id = f"{self._device_unique_id}_{profile.profile_type}"
        self._attr_translation_key = f"{DOMAIN}_{profile.profile_type}"
        self._attr_min_temp = profile.min_temp
        self._attr_max_temp = profile.max_temp
        self._attr_target_temperature_step = profile.target_temp_step
        self._attr_supported_features = profile.supported_features

        self._op_mode_map = profile.operation_modes_map
        self._rev_op_mode_map = {v: k for k, v in self._op_mode_map.items()}

        self._attr_operation_list = list(self._op_mode_map.keys())

        self._current_operation = STATE_OFF
        self._target_temp = None
        self._current_temp = None

    @property
    def current_operation(self) -> str | None:
        return self._current_operation

    @property
    def current_temperature(self) -> float | None:
        return self._current_temp

    @property
    def target_temperature(self) -> float | None:
        return self._target_temp

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)
        update_needed = False

        if cmd.command_type == UdpCommandType.MODE:
            raw_val = int(cmd.value)
            resolved_mode = self._rev_op_mode_map.get(raw_val)
            if resolved_mode:
                self._current_operation = resolved_mode
                update_needed = True

        elif cmd.command_type == UdpCommandType.TARGET_TEMPERATURE:
            self._target_temp = float(cmd.value)
            update_needed = True

        elif cmd.command_type == UdpCommandType.TEMPERATURE:
            self._current_temp = float(cmd.value)
            update_needed = True

        if update_needed:
            _LOGGER.info(
                "Handled update for device %s, received command: %s",
                self._attr_unique_id,
                cmd,
            )
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        await self.async_set_operation_mode(self._profile.default_operation_mode)

    async def async_turn_off(self, **kwargs):
        await self.async_set_operation_mode(STATE_OFF)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is not None:
            temp = max(self._attr_min_temp, min(self._attr_max_temp, float(temp)))
            await self.async_send_command(CmdTargetTemperature(temp))
            self._current_temp = temp
            self.async_write_ha_state()

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        raw_val = self._op_mode_map.get(operation_mode)
        if raw_val is not None:
            await self.async_send_command(CmdMode(raw_val))
            self._current_operation = operation_mode
            self.async_write_ha_state()

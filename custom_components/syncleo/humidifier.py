import logging
from homeassistant.components.humidifier import (
    HumidifierDeviceClass,
    HumidifierEntity,
    HumidifierEntityFeature,
    HumidifierAction,
)
from homeassistant.components.humidifier.const import ATTR_HUMIDITY
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
    STATE_OFF,
)
from homeassistant.core import HomeAssistant, callback
from pysyncleo.commands import CmdTargetHumidity, CmdCurrentHumidity, CmdMode, UdpCommandType

from .devices import HumidifierProfile
from .entity import SyncleoBaseEntity
from .models import SyncleoConfigEntry
from .utils import get_device_profile

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: SyncleoConfigEntry, async_add_entities
):
    conn = entry.runtime_data
    profile = get_device_profile(conn.device)
# New         profile = get_device_profile_by_device(conn.device)
    if isinstance(profile, HumidifierProfile):
        async_add_entities([SyncleoHumidifier(conn, profile, entry)])

class SyncleoHumidifier(SyncleoBaseEntity, HumidifierEntity):
    _attr_name = None

    def __init__(self, connection, profile: HumidifierProfile, entry: SyncleoConfigEntry):
        super().__init__(connection, profile, entry)

        self._profile = profile
        self._attr_translation_key = profile.profile_type
        self._attr_unique_id = f"{self._device_unique_id}_{profile.profile_type}"
        self._attr_max_humidity = profile.max_humidity
        self._attr_min_humidity = profile.min_humidity
        
        self._attr_target_humidity_step = 1.0
        self._attr_supported_features = profile.supported_features

        self._rev_presets_map = {v: k for k, v in profile.preset_modes_map.items()}

        if profile.preset_modes_map:
            self._attr_preset_modes = list(profile.preset_modes_map.keys())

        self._attr_is_on = False
        self._attr_action = HumidifierAction.OFF
        self._current_preset_mode = profile.default_preset_mode
        self._target_humidity = self._attr_min_humidity
        self._current_humidity = None

#    @property
#    def action(self) -> HumidifierAction | None:
#        return self._action

    @property
    def current_humidity(self) -> float | None:
        return self._current_humidity

    @property
    def target_humidity(self) -> float | None:
        return self._target_humidity

    @property
    def mode(self) -> str | None:
        return self._current_preset_mode

    @property
    def available_modes(self) -> list[str] | None:
        return self._attr_preset_modes

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)
        update_needed = False
        
        if cmd.command_type == UdpCommandType.MODE:
            raw_val = int(cmd.value)
            if raw_val == 0:
                self._attr_action = HumidifierAction.OFF
            else:
                resolved_preset = self._rev_presets_map.get(raw_val)
                self._current_preset_mode = resolved_preset
                self._attr_action = HumidifierAction.HUMIDIFYING
                _LOGGER.info(
                    "Mode change for device %s: raw=%s, resolved_preset=%s",
                    self._attr_unique_id,
                    raw_val,
                    resolved_preset,
                )
            self._attr_is_on = True if self._attr_action != HumidifierAction.OFF else False
            update_needed = True

        elif cmd.command_type == UdpCommandType.TARGET_HUMIDITY:
            self._target_humidity = max(self._attr_min_humidity, min(self._attr_max_humidity, float(cmd.value)))
            update_needed = True

        elif cmd.command_type == UdpCommandType.CURRENT_HUMIDITY:
            self._current_humidity = float(cmd.value)
            update_needed = True

        if update_needed:
            _LOGGER.info(
                "Handled update for device %s, received command: %s",
                self._attr_unique_id,
                cmd,
            )
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        await self.async_set_mode(self._current_preset_mode)

    async def async_turn_off(self, **kwargs):
        await self.async_set_mode(STATE_OFF)

    async def async_set_humidity(self, humidity: int) -> None:
#        humidity = kwargs.get(ATTR_HUMIDITY)
        if humidity is not None:
            humidity = max(self._attr_min_humidity, min(self._attr_max_humidity, float(humidity)))
            await self.async_send_command(CmdTargetHumidity(humidity))
            self._current_humidity = humidity
            self.async_write_ha_state()

    async def async_set_mode(self, mode: str) -> None:
        if mode == STATE_OFF:
            raw_val = 0
        else:
            raw_val = self._profile.preset_modes_map.get(mode)
        if raw_val is not None:
            await self.async_send_command(CmdMode(raw_val))
            if mode != STATE_OFF:
                self._current_preset_mode = mode
            self.async_write_ha_state()
import logging
from typing import Any

from homeassistant.components.humidifier import (
    HumidifierDeviceClass,
    HumidifierEntity,
    HumidifierEntityFeature,
)
from homeassistant.core import HomeAssistant, callback
from pysyncleo.commands import (
    CmdMode,
    CmdTargetHumidity,
    UdpCommandType,
)

from .const import TRANLATION_KEY_HUMIDIFIER
from .devices import HumidifierProfile
from .entity import SyncleoBaseEntity
from .humidifier_logic import (
    Command,
    available_modes,
    plan_set_humidity,
    plan_set_mode,
    plan_turn_on,
    resolve_mode,
    visible_target,
)
from .models import SyncleoConfigEntry
from .utils import get_device_profile_by_device

_LOGGER = logging.getLogger(__name__)

DEFAULT_MANUAL_TARGET = 50


async def async_setup_entry(
    hass: HomeAssistant, entry: SyncleoConfigEntry, async_add_entities
):
    conn = entry.runtime_data
    profile = get_device_profile_by_device(conn.device)

    if isinstance(profile, HumidifierProfile):
        async_add_entities([SyncleoHumidifier(conn, profile, entry)])


class SyncleoHumidifier(SyncleoBaseEntity, HumidifierEntity):
    _attr_name = None
    _attr_translation_key = TRANLATION_KEY_HUMIDIFIER
    _attr_device_class = HumidifierDeviceClass.HUMIDIFIER
    _attr_supported_features = HumidifierEntityFeature.MODES

    def __init__(
        self,
        connection,
        profile: HumidifierProfile,
        entry: SyncleoConfigEntry,
    ):
        super().__init__(connection, profile, entry)

        self._profile = profile
        self._model = profile.model
        self._attr_unique_id = f"{self._device_unique_id}_humidifier"
        self._attr_available_modes = available_modes(self._model)
        self._attr_min_humidity = self._model.min_humidity
        self._attr_max_humidity = self._model.max_humidity

        self._device_mode: int | None = None
        self._target: int | None = None
        self._current_humidity: int | None = None
        self._last_on_mode: int = self._model.modes_map[self._model.manual_mode]
        self._last_on_target: int | None = None
        self._last_manual_target: int = DEFAULT_MANUAL_TARGET

    @property
    def _is_off(self) -> bool:
        return self._device_mode == self._model.off_mode

    @property
    def is_on(self) -> bool | None:
        if self._device_mode is None:
            return None
        return not self._is_off

    @property
    def mode(self) -> str | None:
        if self._device_mode is None:
            return None
        if self._is_off:
            return resolve_mode(self._model, self._last_on_mode, self._last_on_target)
        return resolve_mode(self._model, self._device_mode, self._target)

    @property
    def target_humidity(self) -> int | None:
        if self._device_mode is None or self._is_off:
            return None
        return visible_target(self._model, self._device_mode, self._target)

    @property
    def current_humidity(self) -> int | None:
        return self._current_humidity

    def _remember(self) -> None:
        """Remember restorable state after mode/target changes."""
        mode = self._device_mode
        if mode is None:
            return
        model = self._model
        if mode != model.off_mode:
            self._last_on_mode = mode
            self._last_on_target = self._target
        if (
            mode == model.modes_map[model.manual_mode]
            and self._target is not None
            and model.min_humidity <= self._target <= model.max_humidity
        ):
            self._last_manual_target = self._target

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        update_needed = False

        if cmd.command_type == UdpCommandType.MODE:
            self._device_mode = int(cmd.value)
            self._remember()
            update_needed = True

        elif cmd.command_type == UdpCommandType.TARGET_HUMIDITY:
            self._target = int(cmd.value)
            self._remember()
            update_needed = True

        elif cmd.command_type == UdpCommandType.CURRENT_HUMIDITY:
            self._current_humidity = int(cmd.value)
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

    async def _async_execute(self, commands: list[Command]) -> None:
        for kind, value in commands:
            if kind == "mode":
                await self.async_send_command(CmdMode(int(value)))
                self._device_mode = int(value)
            else:
                await self.async_send_command(CmdTargetHumidity(float(value)))
                self._target = int(value)
            self._remember()
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._async_execute(
            plan_turn_on(self._model, self._last_on_mode, self._last_on_target)
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._async_execute([("mode", self._model.off_mode)])

    async def async_set_mode(self, mode: str) -> None:
        await self._async_execute(
            plan_set_mode(self._model, mode, self._target, self._last_manual_target)
        )

    async def async_set_humidity(self, humidity: int) -> None:
        await self._async_execute(
            plan_set_humidity(self._model, humidity, self._device_mode)
        )

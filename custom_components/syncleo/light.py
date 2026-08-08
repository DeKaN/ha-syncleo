import logging
import math
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.color import brightness_to_value, value_to_brightness

from pysyncleo.commands import CmdBacklight
from .devices import DeviceBaseProfile, LightMixin
from .devices.profiles import LightConfig
from .entity import SyncleoBaseEntity
from .models import SyncleoConfigEntry
from .utils import get_device_profile

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SyncleoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Syncleo light entities from a config entry."""
    conn = entry.runtime_data
    profile = get_device_profile(conn.device)

    if isinstance(profile, LightMixin) and profile.lights:
        entities = [
            SyncleoLight(conn, profile, entry, light_key, config)
            for light_key, config in profile.lights.items()
        ]
        async_add_entities(entities)


class SyncleoLight(SyncleoBaseEntity, LightEntity):
    """Representation of a Syncleo Light supporting both RGB and Brightness."""

    _attr_color_mode = ColorMode.RGB
    _attr_supported_color_modes = {ColorMode.RGB}

    def __init__(
        self,
        connection,
        profile: DeviceBaseProfile,
        entry: SyncleoConfigEntry,
        feature_key: str,
        config: LightConfig,
    ) -> None:
        """Initialize the RGB and Brightness light entity."""
        super().__init__(connection, profile, entry)
        self._feature_key = feature_key
        self._is_program_data = feature_key in profile.program_data_fields

        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        self._attr_translation_key = feature_key

        self._red_key = config.red_key
        self._green_key = config.green_key
        self._blue_key = config.blue_key
        self._brightness_key = config.brightness_key
        self._brightness_max_level = config.brightness_levels

        self._brightness_levels = (1, self._brightness_max_level)
        self._current_level = 0
        self._last_level = self._brightness_max_level
        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    @property
    def brightness(self) -> int | None:
        return value_to_brightness(self._brightness_levels, self._current_level)

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        r_bytes = self.get_program_data(self._red_key)
        g_bytes = self.get_program_data(self._green_key)
        b_bytes = self.get_program_data(self._blue_key)

        r = r_bytes[0] if r_bytes else 0
        g = g_bytes[0] if g_bytes else 0
        b = b_bytes[0] if b_bytes else 0

        return (r, g, b)

    async def async_turn_on(self, **kwargs: Any) -> None:
        if ATTR_RGB_COLOR in kwargs:
            r, g, b = kwargs[ATTR_RGB_COLOR]
            await self.async_set_program_data(self._red_key, bytes([r]))
            await self.async_set_program_data(self._green_key, bytes([g]))
            await self.async_set_program_data(self._blue_key, bytes([b]))

        if ATTR_BRIGHTNESS in kwargs:
            target_level = math.ceil(
                brightness_to_value(self._brightness_levels, kwargs[ATTR_BRIGHTNESS])
            )
        else:
            target_level = (
                self._last_level if self._last_level > 0 else self._brightness_max_level
            )

        if (
            self._brightness_key
            and self._brightness_key in self._profile.program_data_fields
        ):
            await self.async_set_program_data(
                self._brightness_key, bytes([target_level])
            )
        else:
            await self.async_send_command(CmdBacklight(state=True))

        self._current_level = target_level
        self._last_level = target_level
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        if (
            self._brightness_key
            and self._brightness_key in self._profile.program_data_fields
        ):
            await self.async_set_program_data(self._brightness_key, bytes([0]))
        else:
            await self.async_send_command(CmdBacklight(state=False))

        self._current_level = 0
        self._is_on = False
        self.async_write_ha_state()

    @callback
    def _handle_device_update(self, cmd) -> None:
        """Handle incoming device status updates for color, brightness, or state changes."""
        super()._handle_device_update(cmd)

        need_update = False

        if (
            self._brightness_key
            and self._brightness_key in self._profile.program_data_fields
        ):
            data = self.get_program_data(self._brightness_key)
            if data:
                self._current_level = data[0]
                self._is_on = self._current_level > 0
                if self._current_level > 0:
                    self._last_level = self._current_level
                need_update = True

        elif isinstance(cmd, CmdBacklight):
            self._is_on = bool(cmd.value)
            self._current_level = self._brightness_max_level if self._is_on else 0

            if self._current_level > 0:
                self._last_level = self._current_level
            need_update = True

        else:
            _LOGGER.debug(
                "Entity %s ignoring unrelated cmd: %s", self._attr_unique_id, cmd
            )

        if need_update:
            self.async_write_ha_state()

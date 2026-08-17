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

from pysyncleo.commands import CmdBacklight, CmdProgramData, CmdNight
from .devices import DeviceBaseProfile, LightMixin
from .devices.profiles import LightConfig
from .entity import FEATURE_TO_COMMAND_MAP, SyncleoBaseEntity
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
        self._cmd_class = FEATURE_TO_COMMAND_MAP.get(feature_key)
        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        self._attr_translation_key = feature_key

        # Кэш для текущего цвета, чтобы не парсить дважды (для RGB и Brightness)
        self._current_rgb: Optional[tuple] = None

        self._red_key = config.red_key
        self._green_key = config.green_key
        self._blue_key = config.blue_key
        self._brightness_key = config.brightness_key
        self._brightness_max_level = config.brightness_levels

        self._brightness_levels = (1, self._brightness_max_level)
        self._current_level = 255 # Если 0, то при первом включении будет яркость 0 (черный)
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

        # Вычисляем яркость по максимальному каналу
        max_channel = max(r, g, b)
        
        if max_channel == 0:
            # Цвет черный - яркость 0, истинный цвет (0,0,0)
            self._attr_brightness = 0
            self._current_level = 0
        else:
            # Яркость для ползунка HA (0-255)
            self._attr_brightness = max_channel
            self._current_level = max_channel

            # Вычисляем "истинный" цвет.
            # Если пришел 128,0,0 (тусклый красный), а яркость 128...
            # То истинный цвет 255,0,0. Делим на коэффициент.
            factor = 255.0 / max_channel
            self._current_rgb = (
                min(255, int(r * factor)),
                min(255, int(g * factor)),
                min(255, int(b * factor))
            )
        return self._current_rgb

    async def async_turn_on(self, **kwargs: Any) -> None:
        updates = {}
        rgb = None
        if ATTR_RGB_COLOR in kwargs:
            rgb = kwargs[ATTR_RGB_COLOR]
            updates |= {
                self._red_key: bytes([rgb[0]]),
                self._green_key: bytes([rgb[1]]),
                self._blue_key: bytes([rgb[2]]),
            }

        if ATTR_BRIGHTNESS in kwargs:
            target_level = math.ceil(
                brightness_to_value(self._brightness_levels, kwargs[ATTR_BRIGHTNESS])
            )
        else:
            target_level = (
                self._last_level if self._last_level > 0 else self._brightness_max_level
            )
        
        target_rgb = rgb if rgb is not None else self._current_rgb or (255,255,255)
        
        if (
            self._brightness_key
            and self._brightness_key in self._profile.program_data_fields
        ):
            updates[self._brightness_key] = bytes([target_level])
        elif self._cmd_class:

            # Применяем яркость (HA передает ее от 0 до 255)
            factor = target_level / 255.0
            target_rgb = tuple(int(c * factor) for c in target_rgb)
            updates |= {
                self._red_key: bytes([target_rgb[0]]),
                self._green_key: bytes([target_rgb[1]]),
                self._blue_key: bytes([target_rgb[2]]),
            }

            await self.async_send_command(self._cmd_class(True))
        else:
#            await self.async_send_command(CmdBacklight(state=True))
            _LOGGER.error(
                "No command class or program data field defined for feature: %s",
                self._feature_key,
            )
            return

        if updates:
            await self.async_set_program_data_fields(updates)

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
        elif self._cmd_class:
            await self.async_send_command(self._cmd_class(False))
        else:
#            await self.async_send_command(CmdBacklight(state=False))
            _LOGGER.error(
                "No command class or program data field defined for feature: %s",
                self._feature_key,
            )
            return

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

        elif isinstance(cmd, CmdProgramData):
            need_update = True
            
            
        elif self._cmd_class and cmd.command_type == self._cmd_class.command_type:
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

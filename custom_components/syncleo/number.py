import logging

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .devices import NumberMixin
from .entity import FEATURE_TO_COMMAND_MAP, SyncleoBaseEntity
from .utils import get_device_profile_by_device

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Syncleo number platform."""
    conn = entry.runtime_data
    profile = get_device_profile_by_device(conn.device)

    if isinstance(profile, NumberMixin) and profile.numbers:
        entities = [
            SyncleoNumber(conn, profile, entry, feature_key)
            for feature_key in profile.numbers
        ]
        async_add_entities(entities)


class SyncleoNumber(SyncleoBaseEntity, NumberEntity):
    def __init__(self, conn, profile, entry, feature_key: str):
        super().__init__(conn, profile, entry)
        self._feature_key = feature_key
        self._is_program_data = feature_key in profile.program_data_fields
        self._cmd_class = FEATURE_TO_COMMAND_MAP.get(feature_key)

        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        self._attr_translation_key = feature_key

        if self._is_program_data:
            config = profile.program_data_fields[feature_key]
        elif isinstance(profile, NumberMixin) and feature_key in profile.number_configs:
            config = profile.number_configs.get(feature_key)
        else:
            config = None

        if config:
            scale = config.value_scale if self._is_program_data else 1.0
            offset = config.value_offset if self._is_program_data else 0.0
            self._attr_native_min_value = config.min_value * scale + offset
            self._attr_native_max_value = config.max_value * scale + offset
            self._attr_native_step = config.step * scale
            self._attr_native_unit_of_measurement = config.unit_of_measurement
        else:
            _LOGGER.warning(
                "No number_config found for %s, using defaults", feature_key
            )
            self._attr_native_min_value = 0
            self._attr_native_max_value = 100
            self._attr_native_step = 1

        self._value = float(self._attr_native_min_value)

    @property
    def native_value(self) -> float | None:
        return self._value

    @property
    def available(self) -> bool:
        if not super().available:
            return False
        if self._is_program_data:
            condition = self._profile.program_data_fields[
                self._feature_key
            ].available_when
            if condition is not None:
                source, expected_value = condition
                data = self.get_known_program_data(source)
                return (
                    data is not None
                    and int.from_bytes(data, byteorder="little") == expected_value
                )
        return True

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        value = self._value
        bounds_changed = False

        if self._is_program_data:
            data = self.get_program_data(self._feature_key)

            if not data:
                _LOGGER.warning(
                    "No program data available for feature: %s", self._feature_key
                )
                value = self._attr_native_min_value

            field_config = self._profile.program_data_fields[self._feature_key]
            raw_min, raw_max = self.get_program_data_bounds(self._feature_key)
            min_value = raw_min * field_config.value_scale + field_config.value_offset
            max_value = raw_max * field_config.value_scale + field_config.value_offset
            bounds_changed = (
                min_value != self._attr_native_min_value
                or max_value != self._attr_native_max_value
            )
            self._attr_native_min_value = min_value
            self._attr_native_max_value = max_value
            parsed_value = (
                int.from_bytes(data, byteorder="little") * field_config.value_scale
                + field_config.value_offset
            )
            value = max(
                self._attr_native_min_value,
                min(self._attr_native_max_value, parsed_value),
            )
            _LOGGER.debug(
                "Handle program data update for device %s, raw: %s, parsed: %s, processed: %s",
                self._attr_unique_id,
                data.hex(),
                parsed_value,
                value,
            )
        elif self._cmd_class and cmd.command_type == self._cmd_class.command_type:
            value = float(cmd.value)
            _LOGGER.debug(
                "Handle command update for device %s, raw: %s, processed: %s",
                self._attr_unique_id,
                cmd.value,
                value,
            )
        else:
            _LOGGER.debug(
                "Entity %s ignoring unrelated cmd: %s", self._attr_unique_id, cmd
            )

        if value != self._value or bounds_changed:
            self._value = value
            self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        if self._is_program_data:
            field_config = self._profile.program_data_fields[self._feature_key]

            raw_value = int(value)
            if field_config.value_scale != 1.0 or field_config.value_offset != 0.0:
                raw_value = round(
                    (value - field_config.value_offset) / field_config.value_scale
                )
            min_value, max_value = self.get_program_data_bounds(self._feature_key)
            fixed_value = max(min_value, min(max_value, raw_value))
            data = fixed_value.to_bytes(field_config.size, byteorder="little")

            await self.async_set_program_data(self._feature_key, data)
        elif self._cmd_class:
            await self.async_send_command(self._cmd_class(value))
        else:
            _LOGGER.error(
                "No command class or program data field defined for feature: %s",
                self._feature_key,
            )
            return

        self._value = value
        self.async_write_ha_state()

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_call_later
from pysyncleo.enums import UdpCommandType

from .const import FEATURE_WATER_SHORTAGE
from .devices import BinarySensorMixin
from .devices.profiles import HumidifierProfile
from .entity import FEATURE_TO_COMMAND_MAP, SyncleoBaseEntity
from .humidifier_logic import is_water_shortage
from .utils import get_device_profile_by_device

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    conn = entry.runtime_data
    profile = get_device_profile_by_device(conn.device)

    entities: list[BinarySensorEntity] = []

    if isinstance(profile, BinarySensorMixin) and profile.binary_sensors:
        entities.extend(
            SyncleoBinarySensor(conn, profile, entry, feature_key)
            for feature_key in profile.binary_sensors
        )

    if isinstance(profile, HumidifierProfile) and profile.water_shortage_sensor:
        entities.append(SyncleoWaterShortageSensor(conn, profile, entry))

    if entities:
        async_add_entities(entities)


class SyncleoBinarySensor(SyncleoBaseEntity, BinarySensorEntity):
    def __init__(self, connection, profile, entry, feature_key: str):
        super().__init__(connection, profile, entry)

        self._feature_key = feature_key
        self._is_program_data = feature_key in profile.program_data_fields
        self._cmd_class = FEATURE_TO_COMMAND_MAP.get(feature_key)

        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        self._attr_translation_key = feature_key
        self._is_on: bool | None = None if self._is_program_data else False

    @property
    def is_on(self) -> bool | None:
        return self._is_on

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        is_on = self._is_on

        if self._is_program_data:
            data = self.get_program_data(self._feature_key)
            is_on = int.from_bytes(data, byteorder="little") != 0

        elif self._cmd_class and cmd.command_type == self._cmd_class.command_type:
            _LOGGER.debug(
                "Handle update for device %s, received command: %s",
                self._attr_unique_id,
                cmd,
            )
            is_on = bool(cmd.value)

        if is_on != self._is_on:
            self._is_on = is_on
            self.async_write_ha_state()


_WATER_SHORTAGE_DELAY = 5


class SyncleoWaterShortageSensor(SyncleoBaseEntity, BinarySensorEntity):
    """Water shortage inferred from mode/target/speed, debounced by 5 seconds."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, connection, profile: HumidifierProfile, entry):
        super().__init__(connection, profile, entry)
        self._model = profile.model
        self._attr_unique_id = f"{self._device_unique_id}_{FEATURE_WATER_SHORTAGE}"
        self._attr_translation_key = FEATURE_WATER_SHORTAGE
        self._mode: int | None = None
        self._target: int | None = None
        self._speed: int | None = None
        self._is_on: bool | None = None
        self._cancel_eval: CALLBACK_TYPE | None = None

    @property
    def is_on(self) -> bool | None:
        return self._is_on

    def _cancel_pending(self) -> None:
        if self._cancel_eval:
            self._cancel_eval()
            self._cancel_eval = None

    async def async_will_remove_from_hass(self) -> None:
        self._cancel_pending()
        await super().async_will_remove_from_hass()

    @callback
    def _handle_device_update(self, cmd) -> None:
        super()._handle_device_update(cmd)
        command_type = cmd.command_type
        if command_type == UdpCommandType.MODE:
            self._mode = int(cmd.value)
        elif command_type == UdpCommandType.TARGET_HUMIDITY:
            self._target = int(cmd.value)
        elif command_type == UdpCommandType.SPEED:
            self._speed = int(cmd.value)
        else:
            return
        self._cancel_pending()
        self._cancel_eval = async_call_later(
            self.hass, _WATER_SHORTAGE_DELAY, self._evaluate
        )

    @callback
    def _evaluate(self, _now) -> None:
        self._cancel_eval = None
        is_on = is_water_shortage(self._model, self._mode, self._target, self._speed)
        if is_on != self._is_on:
            self._is_on = is_on
            self.async_write_ha_state()

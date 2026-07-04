import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant, callback


from .devices import DeviceBaseProfile, SwitchMixin
from .entity import FEATURE_TO_COMMAND_MAP, SyncleoBaseEntity
from .models import SyncleoConfigEntry
from .utils import get_device_profile


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: SyncleoConfigEntry, async_add_entities
):
    conn = entry.runtime_data
    profile = get_device_profile(conn.device)

    if isinstance(profile, SwitchMixin) and profile.switches:
        entities = [
            SyncleoSwitch(conn, profile, entry, key)
            for key in profile.switches
            if key in FEATURE_TO_COMMAND_MAP
        ]
        async_add_entities(entities)


class SyncleoSwitch(SyncleoBaseEntity, SwitchEntity):
    def __init__(
        self,
        connection,
        profile: DeviceBaseProfile,
        entry: SyncleoConfigEntry,
        feature_key: str,
    ):
        super().__init__(connection, profile, entry)
        self._feature_key = feature_key
        self._is_program_data = feature_key in profile.program_data_fields
        self._cmd_class = FEATURE_TO_COMMAND_MAP.get(feature_key)

        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        self._attr_translation_key = feature_key
        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_added_to_hass(self):
        self._connection.register_callback(self._handle_device_update)

    async def async_will_remove_from_hass(self):
        self._connection.unregister_callback(self._handle_device_update)

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        is_on = self._is_on

        if self._is_program_data:
            data = self.get_program_data(self._feature_key)
            _LOGGER.info(
                "Handle program data update for device %s, received data: %s",
                self._attr_unique_id,
                data.hex(),
            )
            is_on = int.from_bytes(data, byteorder="little") != 0 if data else False

        elif self._cmd_class and cmd.command_type == self._cmd_class.command_type:
            _LOGGER.info(
                "Handle update for device %s, received command: %s",
                self._attr_unique_id,
                cmd,
            )
            is_on = bool(cmd.value)
        else:
            _LOGGER.debug(
                "Entity %s ignoring unrelated cmd: %s", self._attr_unique_id, cmd
            )

        if is_on != self._is_on:
            self._is_on = is_on
            self.async_write_ha_state()

    async def _async_switch_set_state(self, value: bool):
        if self._is_program_data:
            field_size = self._profile.program_data_fields[self._feature_key].size
            await self.async_set_program_data(
                self._feature_key, value.to_bytes(field_size, byteorder="little")
            )
        elif self._cmd_class:
            await self._connection.send_command(self._cmd_class(value))
        else:
            _LOGGER.error(
                "No command class or program data field defined for feature: %s",
                self._feature_key,
            )
            return

        self._is_on = value
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        await self._async_switch_set_state(True)

    async def async_turn_off(self, **kwargs):
        await self._async_switch_set_state(False)

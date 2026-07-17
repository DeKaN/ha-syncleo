import logging
from typing import Dict

from homeassistant.const import CONF_MAC, CONF_MODEL
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import DeviceInfo

from pysyncleo.commands import (
    CmdAccessControl,
    CmdBacklight,
    CmdBss,
    CmdCO2,
    CmdChildLock,
    CmdCurrentTemperature,
    CmdDamper,
    CmdError,
    CmdExpendables,
    CmdIonization,
    CmdKeepWarm,
    CmdNight,
    CmdPlaceholder1,
    CmdPlaceholder2,
    CmdPlaceholder3,
    CmdProgramData,
    CmdSmartMode,
    CmdSpeed,
    CmdTank,
    CmdTargetId,
    CmdTurbo,
    CmdUltraviolet,
    CmdVolume,
    CmdWarmStream,
)
from pysyncleo.enums import ConnectionState, UdpCommandType

from .const import (
    DOMAIN,
    CONF_MANUFACTURER,
    FEATURE_ACCESS_CONTROL,
    FEATURE_AURUS_PF_AUTO_OFF_DISPLAY,
    FEATURE_AURUS_PF_HALF_POWER,
    FEATURE_AURUS_SCREENSAVER_MODE,
    FEATURE_AURUS_VRF_CHILD_LOCK,
    FEATURE_AURUS_VRF_ECO_MODE,
    FEATURE_AURUS_VRF_NOISELESS_MODE,
    FEATURE_BACKLIGHT,
    FEATURE_ANTI_MELDEW,
    FEATURE_BSS,
    FEATURE_CHILD_LOCK,
    FEATURE_CURRENT_CO2,
    FEATURE_CURRENT_TEMPERATURE,
    FEATURE_DAMPER,
    FEATURE_ERROR,
    FEATURE_EXPENDABLES_ANODE,
    FEATURE_EXPENDABLES_FILTER,
    FEATURE_GOLDSTAR_GSTI_BREEZE_AWAY,
    FEATURE_GOLDSTAR_GSTI_CLEAN,
    FEATURE_GOLDSTAR_GSTI_DAMPER,
    FEATURE_GOLDSTAR_GSTI_FREEZE_PROTECTION,
    FEATURE_IONIZATION,
    FEATURE_KEEP_WARM,
    FEATURE_NIGHT,
    FEATURE_POWER_LEVEL,
    FEATURE_ECO_AS_SMART_MODE,
    FEATURE_SHUFT_SFMS_09_ANTI_MELDEW,
    FEATURE_SHUFT_SFMS_07_09_FREEZE_PROTECTION,
    FEATURE_SMART_MODE,
    FEATURE_TANK,
    FEATURE_TURBO,
    FEATURE_ULTRAVIOLET,
    FEATURE_VOLUME,
    FEATURE_WARM_STREAM,
)
from .devices import DeviceBaseProfile
from .models import SyncleoConfigEntry

_LOGGER = logging.getLogger(__name__)

FEATURE_TO_COMMAND_MAP = {
    FEATURE_ACCESS_CONTROL: CmdAccessControl,
    FEATURE_ANTI_MELDEW: CmdBss,
    FEATURE_BACKLIGHT: CmdBacklight,
    FEATURE_BSS: CmdBss,
    FEATURE_CHILD_LOCK: CmdChildLock,
    FEATURE_CURRENT_CO2: CmdCO2,
    FEATURE_CURRENT_TEMPERATURE: CmdCurrentTemperature,
    FEATURE_DAMPER: CmdDamper,
    FEATURE_ECO_AS_SMART_MODE: CmdSmartMode,
    FEATURE_ERROR: CmdError,
    FEATURE_EXPENDABLES_ANODE: CmdExpendables,
    FEATURE_EXPENDABLES_FILTER: CmdExpendables,
    FEATURE_IONIZATION: CmdIonization,
    FEATURE_KEEP_WARM: CmdKeepWarm,
    FEATURE_NIGHT: CmdNight,
    FEATURE_POWER_LEVEL: CmdSpeed,
    FEATURE_SMART_MODE: CmdSmartMode,
    FEATURE_TANK: CmdTank,
    FEATURE_TURBO: CmdTurbo,
    FEATURE_ULTRAVIOLET: CmdUltraviolet,
    FEATURE_VOLUME: CmdVolume,
    FEATURE_WARM_STREAM: CmdWarmStream,
    # Custom device specific features
    FEATURE_AURUS_PF_AUTO_OFF_DISPLAY: CmdPlaceholder1,
    FEATURE_AURUS_PF_HALF_POWER: CmdPlaceholder2,
    FEATURE_AURUS_SCREENSAVER_MODE: CmdPlaceholder3,
    FEATURE_AURUS_VRF_CHILD_LOCK: CmdPlaceholder3,
    FEATURE_AURUS_VRF_ECO_MODE: CmdPlaceholder1,
    FEATURE_AURUS_VRF_NOISELESS_MODE: CmdPlaceholder2,
    FEATURE_GOLDSTAR_GSTI_BREEZE_AWAY: CmdPlaceholder1,
    FEATURE_GOLDSTAR_GSTI_CLEAN: CmdPlaceholder2,
    FEATURE_GOLDSTAR_GSTI_DAMPER: CmdDamper,
    FEATURE_GOLDSTAR_GSTI_FREEZE_PROTECTION: CmdPlaceholder3,
    FEATURE_SHUFT_SFMS_07_09_FREEZE_PROTECTION: CmdPlaceholder1,
    FEATURE_SHUFT_SFMS_09_ANTI_MELDEW: CmdPlaceholder2,
}


class SyncleoBaseEntity(Entity):
    """Base class for all Syncleo entities."""

    _attr_has_entity_name = True
    _device_connection_states: dict[str, ConnectionState] = {}

    def __init__(
        self, connection, profile: DeviceBaseProfile, entry: SyncleoConfigEntry
    ):
        self._connection = connection
        self._profile = profile
        self._entry = entry
        self._device_unique_id = self._connection.device.mac_address
        self._program_data_modes: Dict[int, bytearray] = {}

    @property
    def available(self) -> bool:
        return self._connection.state == ConnectionState.CONNECTED

    async def async_added_to_hass(self):
        self._connection.register_callback(self._handle_device_update)
        self._connection.register_state_callback(self._handle_connection_state)

    async def async_will_remove_from_hass(self):
        self._connection.unregister_callback(self._handle_device_update)
        self._connection.unregister_state_callback(self._handle_connection_state)

    async def async_send_command(self, cmd) -> None:
        _LOGGER.info("Sending command %s", cmd)
        await self._connection.send_command(cmd)
        await self._async_set_device_target()

    async def _async_set_device_target(self):
        domain_data = self.hass.data.get(DOMAIN)
        command = (
            CmdTargetId(bytes.fromhex(domain_data.ha_uuid))
            if domain_data and domain_data.ha_uuid
            else CmdTargetId()
        )
        _LOGGER.info("Also sending command %s", command)
        await self._connection.send_command(command)

    @callback
    def _handle_connection_state(self, state: ConnectionState):
        self.async_write_ha_state()
        if state == (
            last_state := self._device_connection_states.get(self._device_unique_id, "")
        ):
            return

        self._device_connection_states[self._device_unique_id] = state
        _LOGGER.info(
            "Connection state changed from '%s' to '%s' for device %s",
            last_state,
            state,
            self._device_unique_id,
        )

        if state == ConnectionState.CONNECTED:
            self.hass.async_create_task(self._async_set_device_target())

    @callback
    def _handle_device_update(self, cmd):
        _LOGGER.info(
            "Start handling update for device %s, received command: %s",
            self._attr_unique_id,
            cmd,
        )
        if cmd.command_type == UdpCommandType.PROGRAM_DATA:
            if cmd.data:
                self._program_data_modes[cmd.mode] = bytearray(cmd.data)

                self.async_write_ha_state()

    def get_program_data(self, feature_key: str) -> bytes:
        field = self._profile.program_data_fields.get(feature_key)
        if not field:
            return b""

        data = self._program_data_modes.get(field.mode)
        if data and len(data) >= field.offset + field.size:
            return data[field.offset : field.offset + field.size]

        return bytes(field.size)

    async def async_set_program_data(self, feature_key: str, value: bytes):
        field = self._profile.program_data_fields.get(feature_key)
        if not field:
            _LOGGER.error(
                "Attempted to set unknown program_data field: %s", feature_key
            )
            return

        if len(value) != field.size:
            _LOGGER.warning(
                "Size mismatch for %s: expected %d bytes, got %d bytes.",
                feature_key,
                field.size,
                len(value),
            )
            value = value.rjust(field.size, b"\x00")[: field.size]

        mode_length = max(
            (
                f.offset + f.size
                for f in self._profile.program_data_fields.values()
                if f.mode == field.mode
            ),
            default=field.offset + field.size,
        )

        cached_data = self._program_data_modes.get(field.mode)

        if cached_data is None:
            data = bytearray(mode_length)
        else:
            data = bytearray(cached_data)
            if len(data) < mode_length:
                data.extend(b"\x00" * (mode_length - len(data)))

        data[field.offset : field.offset + field.size] = value

        await self.async_send_command(CmdProgramData(data=data, mode=field.mode))

        self._program_data_modes[field.mode] = data
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return centralized device info for the Home Assistant Device Registry."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.data[CONF_MAC])},
            name=self._entry.title,
            manufacturer=self._entry.data[CONF_MANUFACTURER],
            model=self._entry.data[CONF_MODEL],
        )

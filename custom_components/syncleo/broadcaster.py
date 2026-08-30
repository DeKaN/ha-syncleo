import hashlib
import logging
import socket
from collections.abc import Callable

from homeassistant.components import network, zeroconf
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, State
from homeassistant.helpers.event import async_track_state_change_event
from pysyncleo.const import SYNCLEO_MDNS_TYPE
from zeroconf.asyncio import AsyncServiceInfo

from .const import (
    CONF_FIRMWARE,
    CONF_PROTOCOL,
    CONF_PUBLIC_KEY,
    CONF_VENDOR,
    VENDOR_RUSCLIMATE,
    VIRTUAL_DEVICE_TYPE,
    ZEROCONF_CURRENT_TEMPERATURE,
    ZEROCONF_CURVE,
    ZEROCONF_DEVICE_TYPE,
    ZEROCONF_MAC_ADDRESS,
)

_LOGGER = logging.getLogger(__name__)


class SyncleoVirtualZeroconfBroadcaster:
    def __init__(self, hass: HomeAssistant, source_entity_id: str, mac: str, port: int):
        self.hass = hass
        self.source_entity_id = source_entity_id
        self.mac = mac.lower()
        self.cleaned_mac = self.mac.replace(":", "")
        self.port = port
        self.service_name = f"{self.cleaned_mac}.{SYNCLEO_MDNS_TYPE}"

        self._aiozc: zeroconf.HaAsyncZeroconf | None = None
        self._ip: str = ""
        self._info: AsyncServiceInfo | None = None
        self._unsub_state_change: Callable[[], None] | None = None
        self._is_registered: bool = False

        self._properties: dict[str, str] = {
            CONF_PUBLIC_KEY: hashlib.sha256(self.mac.encode()).hexdigest(),
            ZEROCONF_CURVE: "29",
            CONF_VENDOR: VENDOR_RUSCLIMATE,
            ZEROCONF_DEVICE_TYPE: str(VIRTUAL_DEVICE_TYPE),
            CONF_FIRMWARE: "1.43",
            CONF_PROTOCOL: "3",
            ZEROCONF_MAC_ADDRESS: self.mac,
        }

    async def async_start(self):
        """Initialize and register the zeroconf service."""
        self._aiozc = await zeroconf.async_get_async_instance(self.hass)
        self._ip = await network.async_get_source_ip(self.hass)

        self._unsub_state_change = async_track_state_change_event(
            self.hass, [self.source_entity_id], self._async_on_state_change
        )

        initial_state = self.hass.states.get(self.source_entity_id)
        await self._process_state(initial_state)

    async def async_stop(self):
        """Unregister the service and cleanup listeners."""
        if self._unsub_state_change:
            self._unsub_state_change()

        if self._is_registered and self._aiozc and self._info:
            await self._aiozc.async_unregister_service(self._info)

    async def _async_on_state_change(self, event: Event[EventStateChangedData]):
        """Callback when the HA temperature sensor updates."""
        await self._process_state(event.data.get("new_state"))

    async def _process_state(self, state: State | None):
        if self._aiozc is None or not self._ip:
            _LOGGER.info("Zeroconf service is not initialized.")
            return

        current_temp = state and self._parse_temp(state)

        if current_temp is not None:
            _LOGGER.info(
                "Got new temperature '%s' from %s", current_temp, self.source_entity_id
            )

            self._properties[ZEROCONF_CURRENT_TEMPERATURE] = str(current_temp)
            self._info = AsyncServiceInfo(
                type_=SYNCLEO_MDNS_TYPE,
                name=self.service_name,
                addresses=[socket.inet_aton(self._ip)],
                port=self.port,
                properties=self._properties,
                server=f"{self.cleaned_mac}.local.",
            )

            if self._is_registered:
                await self._aiozc.async_update_service(self._info)
            else:
                await self._aiozc.async_register_service(self._info)
                self._is_registered = True
                _LOGGER.info(
                    "Sensor %s is back online. Registered zeroconf service.",
                    self.source_entity_id,
                )
        else:
            if self._is_registered and self._info:
                await self._aiozc.async_unregister_service(self._info)
                self._is_registered = False
                _LOGGER.info(
                    "Sensor %s became unavailable. Unregistered zeroconf service to force failover.",
                    self.source_entity_id,
                )

    def _parse_temp(self, state: State) -> float | None:
        if state and state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            try:
                return round(float(state.state), 2)
            except ValueError:
                _LOGGER.debug(
                    "Invalid temperature value '%s' from %s",
                    state.state,
                    self.source_entity_id,
                )
        return None

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_IP_ADDRESS,
    CONF_MAC,
    CONF_PORT,
    CONF_TOKEN,
)

from pysyncleo.transport import TransportManager
from pysyncleo.models import SyncleoUdpDevice

from .const import CONF_PUBLIC_KEY, CONF_PROTOCOL, CONF_VENDOR, DOMAIN
from .models import SyncleoConfigEntry, SyncleoDomainData
from .utils import get_device_profile

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: SyncleoConfigEntry) -> bool:
    """Set up Syncleo from a config entry."""
    assert entry.unique_id is not None

    if DOMAIN not in hass.data:
        manager = TransportManager()
        transport, _ = await hass.loop.create_datagram_endpoint(
            lambda: manager, local_addr=("0.0.0.0", 0)
        )

        hass.data[DOMAIN] = SyncleoDomainData(manager=manager, transport=transport)

    domain_data: SyncleoDomainData = hass.data[DOMAIN]
    manager = domain_data.manager

    public_key = entry.data.get(CONF_PUBLIC_KEY)
    device = SyncleoUdpDevice(
        mac_address=entry.data[CONF_MAC],
        inet_address=(entry.data[CONF_IP_ADDRESS], entry.data[CONF_PORT]),
        vendor=entry.data[CONF_VENDOR],
        device_type=entry.data[CONF_DEVICE_CLASS],
        protocol=entry.data[CONF_PROTOCOL],
        device_token=bytes.fromhex(entry.data[CONF_TOKEN]),
        device_pubkey=bytes.fromhex(public_key) if public_key else None,
    )

    connection = manager.register_device(device)
    if not connection:
        return False

    entry.runtime_data = connection

    profile = get_device_profile(connection.device)

    if profile:
        platforms = profile.supported_platforms
        _LOGGER.debug(
            f"Loading platforms {platforms} for {connection.device.mac_address}"
        )
        await hass.config_entries.async_forward_entry_setups(entry, platforms)

        entry.async_create_background_task(
            hass, connection.connect(), "syncleo-handshake"
        )
    else:
        _LOGGER.warning(
            f"No profile found for {connection.device.vendor} Type {connection.device.device_type}. "
            "Skipping entity creation."
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    connection = entry.runtime_data
    profile = get_device_profile(connection.device)

    unload_ok = True

    if profile:
        unload_ok = await hass.config_entries.async_unload_platforms(
            entry, profile.supported_platforms
        )

    if unload_ok:
        domain_data: SyncleoDomainData = hass.data[DOMAIN]
        domain_data.manager.connections.pop(
            entry.runtime_data.device.inet_address, None
        )

        if not domain_data.manager.connections:
            domain_data.transport.close()
            hass.data.pop(DOMAIN)
            _LOGGER.info("All Syncleo devices removed. UDP Socket closed.")

    return unload_ok

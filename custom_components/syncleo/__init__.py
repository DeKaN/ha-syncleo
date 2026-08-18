import asyncio
import logging

from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_IP_ADDRESS,
    CONF_MAC,
    CONF_PORT,
    CONF_TOKEN,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.instance_id import async_get
from pysyncleo.models import SyncleoUdpDevice
from pysyncleo.transport import TransportManager

from .broadcaster import SyncleoVirtualZeroconfBroadcaster
from .const import (
    CONF_IS_VIRTUAL,
    CONF_PROTOCOL,
    CONF_PUBLIC_KEY,
    CONF_SOURCE_ENTITY,
    CONF_VENDOR,
    DOMAIN,
)
from .models import SyncleoDomainData, SyncleoGenericConfigEntry
from .utils import get_device_profile_by_device

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: SyncleoGenericConfigEntry
) -> bool:
    """Set up Syncleo from a config entry."""
    assert entry.unique_id is not None

    if entry.data.get(CONF_IS_VIRTUAL, False):
        _LOGGER.info(
            "Setting up Virtual Zeroconf Broadcaster for %s", entry.data[CONF_MAC]
        )
        source_entity = entry.data[CONF_SOURCE_ENTITY]
        mac = entry.data[CONF_MAC]
        port = entry.data[CONF_PORT]

        broadcaster = SyncleoVirtualZeroconfBroadcaster(hass, source_entity, mac, port)
        await broadcaster.async_start()

        entry.runtime_data = broadcaster

        return True

    lock_name = f"{DOMAIN}_setup_lock"
    if lock_name not in hass.data:
        hass.data[lock_name] = asyncio.Lock()

    async with hass.data[lock_name]:
        if DOMAIN not in hass.data:
            ha_uuid = await async_get(hass)
            manager = TransportManager()
            transport, _ = await hass.loop.create_datagram_endpoint(
                lambda: manager, local_addr=("0.0.0.0", 0)
            )

            hass.data[DOMAIN] = SyncleoDomainData(
                manager=manager, transport=transport, ha_uuid=ha_uuid
            )

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

    profile = get_device_profile_by_device(connection.device)

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


async def async_unload_entry(
    hass: HomeAssistant, entry: SyncleoGenericConfigEntry
) -> bool:
    """Unload a config entry."""
    if isinstance(entry.runtime_data, SyncleoVirtualZeroconfBroadcaster):
        _LOGGER.info(
            "Unloading Virtual Zeroconf Broadcaster for %s", entry.data[CONF_MAC]
        )
        broadcaster: SyncleoVirtualZeroconfBroadcaster = entry.runtime_data

        await broadcaster.async_stop()
        return True

    connection = entry.runtime_data
    profile = get_device_profile_by_device(connection.device)

    unload_ok = True

    if profile:
        unload_ok = await hass.config_entries.async_unload_platforms(
            entry, profile.supported_platforms
        )

    if unload_ok:
        domain_data: SyncleoDomainData = hass.data[DOMAIN]
        domain_data.manager.unregister_device(connection.device)

        if not domain_data.manager.connections:
            domain_data.transport.close()
            hass.data.pop(DOMAIN)
            _LOGGER.info("All Syncleo devices removed. UDP Socket closed.")

    return unload_ok

import asyncio
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from pysyncleo.transport import SyncleoConnection, TransportManager

from .broadcaster import SyncleoVirtualZeroconfBroadcaster


@dataclass
class SyncleoDomainData:
    manager: TransportManager
    transport: asyncio.DatagramTransport
    ha_uuid: str


type SyncleoGenericConfigEntry = ConfigEntry[
    SyncleoConnection | SyncleoVirtualZeroconfBroadcaster
]
type SyncleoConfigEntry = ConfigEntry[SyncleoConnection]

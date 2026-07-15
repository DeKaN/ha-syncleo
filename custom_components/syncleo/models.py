import asyncio
from dataclasses import dataclass
from homeassistant.config_entries import ConfigEntry

from pysyncleo.transport import TransportManager, SyncleoConnection


@dataclass
class SyncleoDomainData:
    manager: TransportManager
    transport: asyncio.DatagramTransport
    ha_uuid: str


type SyncleoConfigEntry = ConfigEntry[SyncleoConnection]

from datetime import timedelta
import logging
import aiohttp
from awesomeversion import AwesomeVersion, AwesomeVersionException
from homeassistant.components.update import (
    UpdateEntity,
    UpdateDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_FIRMWARE
from .entity import SyncleoBaseEntity
from .utils import get_device_firmware_url, get_device_profile_by_device

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(days=1)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    conn = entry.runtime_data
    profile = get_device_profile_by_device(conn.device)

    if profile:
        async_add_entities([SyncleoUpdate(conn, profile, entry)])


class SyncleoUpdate(SyncleoBaseEntity, UpdateEntity):
    _attr_device_class = UpdateDeviceClass.FIRMWARE
    _attr_should_poll = True

    def __init__(self, connection, profile, entry: ConfigEntry) -> None:
        super().__init__(connection, profile, entry)

        self._attr_unique_id = f"{self._device_unique_id}_update"
        self._attr_installed_version = entry.data[CONF_FIRMWARE]

        self._latest_version: str | None = None

    @property
    def latest_version(self) -> str | None:
        return self._latest_version or self.installed_version

    async def async_update(self) -> None:
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                get_device_firmware_url(self._profile),
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    _LOGGER.info("Got firmware version: %s", data)
                    versions = []
                    for x in data.get("stable", []):
                        try:
                            versions.append(AwesomeVersion(x.get("version")))
                        except AwesomeVersionException:
                            pass

                    if versions:
                        self._latest_version = str(max(versions))
                else:
                    _LOGGER.debug(
                        "Failed to check firmware update: HTTP %s", response.status
                    )

        except TimeoutError:
            _LOGGER.debug("Timeout connecting to firmware update server")
        except aiohttp.ClientError as err:
            _LOGGER.debug("Network error checking firmware update: %s", err)
        except Exception as err:
            _LOGGER.error("Unexpected error parsing firmware update JSON: %s", err)

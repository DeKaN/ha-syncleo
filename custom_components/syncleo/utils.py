import logging
import urllib.parse
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_FRIENDLY_NAME,
    CONF_MAC,
    CONF_TOKEN,
)

from pysyncleo.models import SyncleoUdpDevice

from .devices import DEVICE_PROFILES, DeviceBaseProfile
from .const import CONF_ATTRIBUTES, CONF_VENDOR, FIRMVARE_HOST_BY_VENDOR

_LOGGER = logging.getLogger(__name__)


def parse_share_url(url: str) -> dict:
    """Extracts device metadata and authorization tokens from the Syncleo share URL."""
    parsed = urllib.parse.urlparse(url)

    path_parts = parsed.path.strip("/").split("/")[::-1]

    if len(path_parts) < 3:
        raise ValueError("Invalid URL path structure")

    vendor = path_parts[2]
    device_type = int(path_parts[1])
    mac = path_parts[0].lower()

    query = urllib.parse.parse_qs(parsed.query)
    token = query.get("token", [""])[0]
    name = query.get("name", ["Syncleo Device"])[0]

    attributes = {}
    for key, value_list in query.items():
        if key.startswith("attributes_"):
            clean_key = key[len("attributes_") :]
            attributes[clean_key] = value_list[0]

    return {
        CONF_VENDOR: vendor,
        CONF_DEVICE_CLASS: device_type,
        CONF_MAC: mac,
        CONF_TOKEN: token,
        CONF_FRIENDLY_NAME: name,
        CONF_ATTRIBUTES: attributes,
    }


def get_device_profile_by_device(device: SyncleoUdpDevice) -> DeviceBaseProfile | None:
    return get_device_profile(device.vendor, device.device_type)


def get_device_profile(vendor: str, device_type: int) -> DeviceBaseProfile | None:
    profile = DEVICE_PROFILES.get((vendor.lower(), device_type))
    if not profile:
        _LOGGER.error(
            "No profile found for vendor '%s' type %s",
            vendor,
            device_type,
        )
    return profile


def get_device_firmware_url(profile: DeviceBaseProfile) -> str:
    return f"https://{FIRMVARE_HOST_BY_VENDOR[profile.vendor]}/{profile.vendor}/{profile.device_type}/slots/latest.json"

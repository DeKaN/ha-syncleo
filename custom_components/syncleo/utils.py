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
from .const import CONF_ATTRIBUTES, CONF_VENDOR

_LOGGER = logging.getLogger(__name__)


def parse_share_url(url: str) -> dict:
    """Extracts device metadata and authorization tokens from the Syncleo share URL."""
    parsed = urllib.parse.urlparse(url)

    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) < 3:
        raise ValueError("Invalid URL path structure")

    vendor = path_parts[0]
    device_type = int(path_parts[1])
    mac = path_parts[2].lower()

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
        CONF_FRIENDLY_NAME: urllib.parse.unquote(name),
        CONF_ATTRIBUTES: attributes,
    }


def get_device_profile(device: SyncleoUdpDevice) -> DeviceBaseProfile | None:
    profile = DEVICE_PROFILES.get((device.vendor.lower(), device.device_type))
    if not profile:
        _LOGGER.error(
            "No profile found for vendor '%s' type %s",
            device.vendor,
            device.device_type,
        )
    return profile

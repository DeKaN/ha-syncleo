import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_FRIENDLY_NAME,
    CONF_IP_ADDRESS,
    CONF_MAC,
    CONF_MODEL,
    CONF_PORT,
    CONF_TOKEN,
    CONF_URL,
)
from homeassistant.helpers.device_registry import format_mac

from .const import (
    CONF_ATTRIBUTES,
    CONF_MANUFACTURER,
    DOMAIN,
    CONF_VENDOR,
    CONF_PROTOCOL,
    CONF_PUBLIC_KEY,
    ZEROCONF_CURVE,
    ZEROCONF_DEVICE_TYPE,
    ZEROCONF_MAC_ADDRESS,
)
from .utils import parse_share_url

_LOGGER = logging.getLogger(__name__)


class SyncleoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._discovered_host = None
        self._discovered_port = None
        self._discovered_properties = {}
        self._entry_data = {}

    async def async_step_zeroconf(
        self, discovery_info: ZeroconfServiceInfo
    ) -> ConfigFlowResult:
        """Handle zeroconf discovery and cache ALL available properties."""

        mac = discovery_info.properties.get(ZEROCONF_MAC_ADDRESS)

        if not mac:
            _LOGGER.warning(
                "Zeroconf discovery for device at %s is missing MAC address",
                discovery_info.host,
            )
            return self.async_abort(reason="missing_mac")

        formatted_mac = format_mac(mac)

        await self.async_set_unique_id(formatted_mac)

        self._abort_if_unique_id_configured(
            updates={CONF_IP_ADDRESS: discovery_info.host}
        )

        self._discovered_host = discovery_info.host
        self._discovered_port = discovery_info.port
        self._discovered_properties = discovery_info.properties

        host_str = self._discovered_host or "Unknown Host"

        _LOGGER.info(
            "Zeroconf discovered device at %s:%s with properties %s",
            host_str,
            self._discovered_port,
            self._discovered_properties,
        )

        vendor_raw = self._discovered_properties.get(CONF_VENDOR) or "Syncleo"
        vendor_name = vendor_raw.capitalize()

        self.context["title_placeholders"] = {"host": host_str, "vendor": vendor_name}

        return await self.async_step_zeroconf_confirm()

    async def async_step_zeroconf_confirm(self, user_input=None) -> ConfigFlowResult:
        """Confirm discovery, validate the URL, and prioritize Zeroconf data."""
        errors = {}
        host_str = self._discovered_host or "Unknown Host"

        vendor_raw = self._discovered_properties.get(CONF_VENDOR) or "Syncleo"
        vendor_name = vendor_raw.capitalize()

        if user_input is not None:
            try:
                parsed_data = parse_share_url(user_input[CONF_URL])
                url_mac = format_mac(parsed_data[CONF_MAC])
                url_device_type = parsed_data[CONF_DEVICE_CLASS]

                _LOGGER.debug(f"Parsed URL data: {parsed_data}")

                mac = self._discovered_properties.get(ZEROCONF_MAC_ADDRESS)
                if mac and format_mac(mac) != url_mac:
                    errors["base"] = "mac_mismatch"

                device_type = self._discovered_properties.get(ZEROCONF_DEVICE_TYPE)
                if device_type and int(device_type) != url_device_type and not errors:
                    errors["base"] = "type_mismatch"

                if not errors:
                    await self.async_set_unique_id(url_mac)
                    self._abort_if_unique_id_configured()

                    extracted_model = parsed_data[CONF_ATTRIBUTES].get(
                        "model", "Unknown Model"
                    )
                    port = self._discovered_port
                    protocol = int(self._discovered_properties.get(CONF_PROTOCOL, "1"))
                    curve = int(self._discovered_properties.get(ZEROCONF_CURVE, 0))
                    pubkey = self._discovered_properties.get(CONF_PUBLIC_KEY)
                    pubkey_length = len(pubkey) if pubkey else 0
                    if protocol > 1 and (curve != 29 or pubkey_length != 64):
                        _LOGGER.warning(
                            f"Device at {host_str}:{port} advertises protocol version {protocol} with curve {curve} and public key size {pubkey_length}. Fallback to protocol 1."
                        )
                        protocol = 1

                    self._entry_data = {
                        CONF_IP_ADDRESS: host_str,
                        CONF_PORT: port,
                        CONF_MAC: url_mac,
                        CONF_MODEL: extracted_model,
                        CONF_ATTRIBUTES: parsed_data[CONF_ATTRIBUTES],
                        CONF_DEVICE_CLASS: int(device_type)
                        if device_type
                        else url_device_type,
                        CONF_VENDOR: self._discovered_properties.get(CONF_VENDOR),
                        CONF_TOKEN: parsed_data[CONF_TOKEN],
                        CONF_PROTOCOL: protocol,
                        CONF_PUBLIC_KEY: pubkey,
                        CONF_FRIENDLY_NAME: parsed_data[CONF_FRIENDLY_NAME],
                    }
                    _LOGGER.debug(
                        "Prepared entry data for device %s: %s",
                        host_str,
                        self._entry_data,
                    )

                    return await self.async_step_model_config()
            except ValueError:
                errors["base"] = "invalid_url"
            except Exception:
                _LOGGER.exception("Unexpected exception in zeroconf config flow")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="zeroconf_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL): str,
                }
            ),
            description_placeholders={"host": host_str, "vendor": vendor_name},
            errors=errors,
        )

    async def async_step_model_config(self, user_input=None) -> ConfigFlowResult:
        """Allow user to review and explicitly set the device manufacturer and model."""
        if user_input is not None:
            self._entry_data[CONF_MODEL] = user_input[CONF_MODEL]
            self._entry_data[CONF_MANUFACTURER] = user_input[CONF_MANUFACTURER]

            entry_title = self._entry_data.get(
                CONF_FRIENDLY_NAME, user_input[CONF_MODEL]
            )

            _LOGGER.info(
                "Creating config entry %s with data %s",
                entry_title,
                self._entry_data,
            )
            return self.async_create_entry(
                title=entry_title,
                data=self._entry_data,
            )

        vendor = self._entry_data.get(CONF_VENDOR, "syncleo")
        suggested_model = self._entry_data.get(CONF_MODEL, "Unknown Model")

        _LOGGER.debug(
            "Found device vendor '%s' and model '%s', trying to suggest manufacturer and model for user confirmation",
            vendor,
            suggested_model,
        )

        if vendor.lower() == "rusclimate" and "_" in suggested_model:
            parts = suggested_model.split("_")
            suggested_manufacturer = parts[0].capitalize()
            suggested_model = " ".join([part.capitalize() for part in parts[1:]])
        else:
            suggested_manufacturer = vendor.capitalize()

        _LOGGER.debug(
            "Calculated suggested manufacturer '%s' and model '%s'",
            suggested_manufacturer,
            suggested_model,
        )

        return self.async_show_form(
            step_id="model_config",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_MANUFACTURER, default=suggested_manufacturer
                    ): str,
                    vol.Required(CONF_MODEL, default=suggested_model): str,
                }
            ),
            description_placeholders={"vendor": vendor.capitalize()},
        )

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Manual setup is blocked; wait for network discovery."""
        return self.async_abort(reason="manual_setup_requires_discovery")

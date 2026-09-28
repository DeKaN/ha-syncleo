from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .devices import ButtonConfig, ButtonMixin, DeviceBaseProfile
from .entity import SyncleoBaseEntity
from .models import SyncleoConfigEntry
from .utils import get_device_profile_by_device


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SyncleoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    conn = entry.runtime_data
    profile = get_device_profile_by_device(conn.device)

    if isinstance(profile, ButtonMixin) and profile.buttons:
        entities = [
            SyncleoButton(conn, profile, entry, key, config)
            for key, config in profile.buttons.items()
        ]
        async_add_entities(entities)


class SyncleoButton(SyncleoBaseEntity, ButtonEntity):
    def __init__(
        self,
        connection,
        profile: DeviceBaseProfile,
        entry: SyncleoConfigEntry,
        feature_key: str,
        config: ButtonConfig,
    ) -> None:
        super().__init__(connection, profile, entry)
        self._command_factory = config.command_factory
        self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
        self._attr_translation_key = feature_key
        self._attr_entity_category = config.entity_category
        self._attr_entity_registry_enabled_default = (
            config.entity_registry_enabled_default
        )

    async def async_press(self) -> None:
        await self.async_send_command(self._command_factory())

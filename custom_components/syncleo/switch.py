import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import slugify

from .devices import SwitchMixin
from .entity import FEATURE_TO_COMMAND_MAP, SyncleoBaseEntity
#from .models import SyncleoConfigEntry
from .utils import get_device_profile


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Syncleo switch platform."""
    conn = entry.runtime_data
    profile = get_device_profile(conn.device)

    if isinstance(profile, SwitchMixin) and profile.switches:
        _LOGGER.info("profile.switches %s", profile.switches)
        entities = [
            SyncleoSwitch(conn, profile, entry, feature_key)
            for feature_key in profile.switches
        ]
        async_add_entities(entities)


#    if isinstance(profile, SwitchMixin) and profile.switches:
#        entities = []
#        for feature_key in profile.switches:
            # Получаем translation_key из switch_configs
#            translation_key = feature_key  # значение по умолчанию
            
#            if feature_key in profile.switch_configs:
#                config = profile.switch_configs[feature_key]
#                if config.translation_key:
#                    translation_key = config.translation_key
#                    _LOGGER.info(f"Using translation_key '{translation_key}' for {feature_key}")
            
#            entities.append(SyncleoSwitch(conn, profile, entry, feature_key, translation_key))
        
#        async_add_entities(entities)

#    await hass.async_add_executor_job(lambda: None)  # Даем время HA обработать
#    from homeassistant.helpers import entity_registry as er
#    entity_registry = er.async_get(hass)
        
#    for entity in entities:
#        unique_id = entity.unique_id
#        entity_id = entity_registry.async_get_entity_id("switch", "syncleo", unique_id)
#        if entity_id:
#            _LOGGER.info(f"✅ Entity registered: {entity_id}")
#        else:
#            _LOGGER.warning(f"❌ Entity NOT found: {unique_id}")




class SyncleoSwitch(SyncleoBaseEntity, SwitchEntity):
    _attr_has_entity_name = True
    
    def __init__(self, conn, profile, entry, feature_key: str, translation_key: str = None):
        super().__init__(conn, profile, entry)
        self._feature_key = feature_key
        self._is_program_data = feature_key in profile.program_data_fields
        self._cmd_class = FEATURE_TO_COMMAND_MAP.get(feature_key)

        if self._is_program_data:
            config = profile.program_data_fields[feature_key]
        elif isinstance(profile, SwitchMixin) and feature_key in profile.switch_configs:
            config = profile.switch_configs.get(feature_key)
        else:
            config = None
#        _LOGGER.info("ENTRY %s", f"switch.{slugify(entry.title)}_{feature_key}")
        if config:
#            _LOGGER.info(f"Config for {feature_key}: translation_key={config.translation_key}")
            self._attr_unique_id = f"{self._device_unique_id}_{config.translation_key}"
#            self._attr_entity_id = f"switch.{slugify(entry.title)}_{feature_key}"
            self._attr_translation_key = config.translation_key
        else:
#            _LOGGER.info(f"No config for {feature_key}, using feature_key as translation_key")
            self._attr_unique_id = f"{self._device_unique_id}_{feature_key}"
#        self._attr_entity_id = f"switch.{slugify(entry.title)}_{feature_key}"
#        self._entity_id = f"switch.{slugify(entry.title)}_{feature_key}"
#        self.entity_id = f"switch.{slugify(entry.title)}_{feature_key}"
            self._attr_translation_key = feature_key
#        self._attr_name = feature_key
        _LOGGER.info("unique_id %s, translation_key %s", self._attr_unique_id, self._attr_translation_key)
        self._is_on = False


    @property
    def is_on(self) -> bool:
        return self._is_on

    @callback
    def _handle_device_update(self, cmd):
        super()._handle_device_update(cmd)

        is_on = self._is_on

        if self._is_program_data:
            data = self.get_program_data(self._feature_key)
            _LOGGER.info(
                "Handle program data update for device %s, received data: %s",
                self._attr_unique_id,
                data.hex(),
            )
            is_on = int.from_bytes(data, byteorder="little") != 0 if data else False

        elif self._cmd_class and cmd.command_type == self._cmd_class.command_type:
            _LOGGER.info(
                "Handle update for device %s, received command: %s",
                self._attr_unique_id,
                cmd,
            )
            is_on = bool(cmd.value)
        else:
            _LOGGER.debug(
                "Entity %s ignoring unrelated cmd: %s", self._attr_unique_id, cmd
            )

        if is_on != self._is_on:
            self._is_on = is_on
            self.async_write_ha_state()

    async def _async_switch_set_state(self, value: bool):
        if self._is_program_data:
            field_size = self._profile.program_data_fields[self._feature_key].size
            await self.async_set_program_data(
                self._feature_key, value.to_bytes(field_size, byteorder="little")
            )
        elif self._cmd_class:
            await self.async_send_command(self._cmd_class(value))
        else:
            _LOGGER.error(
                "No command class or program data field defined for feature: %s",
                self._feature_key,
            )
            return

        self._is_on = value
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        await self._async_switch_set_state(True)

    async def async_turn_off(self, **kwargs):
        await self._async_switch_set_state(False)

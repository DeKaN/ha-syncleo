"""Debug helpers for Syncleo integration."""
import asyncio
import logging
import socket
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE_CLASS, CONF_PORT, CONF_IP_ADDRESS, CONF_MAC
from homeassistant.helpers import entity_registry as er

from pysyncleo.commands import (
    CmdMode,
    CmdTargetTemperature,
    CmdCurrentTemperature,
    CmdSpeed,
    CmdPower,
    CmdChildLock,
    CmdBacklight,
    CmdVolume,
    CmdError,
    CmdProgramData,
)
from pysyncleo.enums import ConnectionState, UdpCommandType

from .const import CONF_VENDOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

# Глобальный флаг для отслеживания регистрации сервисов
_SERVICES_REGISTERED = False

_LOGGER.info("Read debug_helpers")

async def async_register_debug_services(hass: HomeAssistant) -> None:
    """Register debug services if not already registered."""
    global _SERVICES_REGISTERED
    _LOGGER.info("Read debug_helpers")
    if _SERVICES_REGISTERED:
        return

    async def handle_emulate_connect(call: ServiceCall) -> None:
        """Handle emulate connect service."""
        hass = call.hass
        mac = call.data.get("mac")
        state = call.data.get("state", "connected")
    
        if not mac:
            _LOGGER.error("MAC address is required")
            return
    
        for entry in hass.config_entries.async_entries(DOMAIN):
            if entry.data.get(CONF_MAC) == mac:
                connection = entry.runtime_data
                if not connection:
                    _LOGGER.error(f"No connection found for device {mac}")
                    return
    
                # 1. Останавливаем reconnect
                if hasattr(connection, '_reconnect_attempts'):
                    connection._reconnect_attempts = 9999
                
                if hasattr(connection, '_reconnect_unsubscribe') and connection._reconnect_unsubscribe:
                    try:
                        connection._reconnect_unsubscribe()
                    except Exception as e:
                        _LOGGER.error(f"Error stopping reconnect: {e}")
                    connection._reconnect_unsubscribe = None
    
                # 2. Определяем новое состояние
                if state == "connected":
                    new_state = ConnectionState.CONNECTED
                elif state == "disconnected":
                    new_state = ConnectionState.DISCONNECTED
                else:
                    _LOGGER.error(f"Unknown state: {state}")
                    return
    
                # 3. Устанавливаем состояние ВО ВСЕ ВОЗМОЖНЫЕ МЕСТА
                # Прямое присвоение
                connection._state = new_state
                
                # Если есть свойство state, пробуем установить через него
                if hasattr(connection, 'state'):
                    try:
                        connection.state = new_state
                    except AttributeError:
                        pass
                
                _LOGGER.info(f"Device {mac} _state set to {connection._state}")
                _LOGGER.info(f"Device {mac} state property = {connection.state if hasattr(connection, 'state') else 'N/A'}")
    
                # 4. Вызываем колбэки состояния
                if hasattr(connection, '_state_callbacks'):
                    callbacks = list(connection._state_callbacks)
                    for callback in callbacks:
                        try:
                            if callable(callback):
                                callback(new_state)
                        except Exception as e:
                            _LOGGER.error(f"Error in state callback: {e}")
                    _LOGGER.info(f"Executed {len(callbacks)} state callbacks for {mac}")
    
                # 5. Отправляем начальные данные
                if state == "connected":
                    commands = [CmdError(0)]
                    if hasattr(connection, '_callbacks'):
                        callbacks = list(connection._callbacks)
                        for cmd in commands:
                            for callback in callbacks:
                                try:
                                    if callable(callback):
                                        callback(cmd)
                                except Exception as e:
                                    _LOGGER.error(f"Error in command callback: {e}")
                            _LOGGER.info(f"Sent init command: {cmd}")
    
                # 6. Принудительно обновляем все сущности через их _handle_connection_state
                entity_registry = er.async_get(hass)
                for entity_entry in entity_registry.entities.values():
                    if entity_entry.config_entry_id == entry.entry_id:
                        # Получаем саму сущность
                        component = hass.data.get("entity_component", {}).get(entity_entry.domain)
                        if component and hasattr(component, "get_entity"):
                            entity = component.get_entity(entity_entry.entity_id)
                            if entity and hasattr(entity, "_handle_connection_state"):
                                # Вызываем обработчик состояния напрямую
                                entity._handle_connection_state(new_state)
                                _LOGGER.info(f"Directly updated entity: {entity_entry.entity_id}")
                        else:
                            # Fallback: обновляем через state machine
                            state_obj = hass.states.get(entity_entry.entity_id)
                            if state_obj:
                                hass.states.async_set(
                                    entity_entry.entity_id,
                                    state_obj.state,
                                    state_obj.attributes,
                                    force_update=True,
                                )
                                _LOGGER.info(f"Force updated entity: {entity_entry.entity_id}")
    
                _LOGGER.info(f"Device {mac} successfully activated")
                return
    
        _LOGGER.error(f"Device {mac} not found")

    async def handle_emulate_command(call: ServiceCall) -> None:
        """Handle emulate command service."""
        hass = call.hass
        mac = call.data.get("mac")
        command_type = call.data.get("command_type")
        value = call.data.get("value")
        mode = call.data.get("mode", 0)
        data = call.data.get("data")
    
        if not mac or not command_type:
            _LOGGER.error("MAC and command_type are required")
            return
    
        for entry in hass.config_entries.async_entries(DOMAIN):
            if entry.data.get(CONF_MAC) == mac:
                connection = entry.runtime_data
                if not connection:
                    _LOGGER.error(f"No connection found for device {mac}")
                    return
    
                # Создаем команду в зависимости от типа
                if command_type == "mode":
                    cmd = CmdMode(int(value))
                elif command_type == "target_temperature":
                    cmd = CmdTargetTemperature(float(value))
                elif command_type == "temperature":
                    cmd = CmdTemperature(float(value))
                elif command_type == "current_temperature":
                    cmd = CmdCurrentTemperature(float(value))
                elif command_type == "speed":
                    cmd = CmdSpeed(int(value))
                elif command_type == "power":
                    cmd = CmdPower(bool(value))
                elif command_type == "child_lock":
                    cmd = CmdChildLock(bool(value))
                elif command_type == "backlight":
                    cmd = CmdBacklight(bool(value))
                elif command_type == "volume":
                    cmd = CmdVolume(bool(value))
                elif command_type == "error":
                    cmd = CmdError(int(value))
                elif command_type == "program_data":
                    data_bytes = bytes.fromhex(data) if data else b""
                    cmd = CmdProgramData(data=data_bytes, mode=mode)
                else:
                    _LOGGER.error(f"Unknown command type: {command_type}")
                    return
    
                # Отправляем команду через колбэки (как в рабочей функции)
                if hasattr(connection, '_callbacks'):
                    callbacks = list(connection._callbacks)
                    for callback in callbacks:
                        try:
                            if callable(callback):
                                callback(cmd)
                        except Exception as e:
                            _LOGGER.error(f"Error in command callback: {e}")
                    _LOGGER.info(f"Sent command: {cmd}")
    
                    # Обновляем состояние сущностей (как в рабочей функции)
                    entity_registry = er.async_get(hass)
                    for entity_entry in entity_registry.entities.values():
                        if entity_entry.config_entry_id == entry.entry_id:
                            # Получаем саму сущность
                            component = hass.data.get("entity_component", {}).get(entity_entry.domain)
                            if component and hasattr(component, "get_entity"):
                                entity = component.get_entity(entity_entry.entity_id)
                                if entity and hasattr(entity, "async_write_ha_state"):
                                    entity.async_write_ha_state()
                                    _LOGGER.info(f"Updated entity: {entity_entry.entity_id}")
                            else:
                                # Fallback: обновляем через state machine
                                state_obj = hass.states.get(entity_entry.entity_id)
                                if state_obj:
                                    hass.states.async_set(
                                        entity_entry.entity_id,
                                        state_obj.state,
                                        state_obj.attributes,
                                        force_update=True,
                                    )
                                    _LOGGER.info(f"Force updated entity: {entity_entry.entity_id}")
                else:
                    _LOGGER.warning(f"No _callbacks found for device {mac}")
                
                _LOGGER.info(f"Command {command_type}={value} sent to device {mac}")
                return
    
        _LOGGER.error(f"Device {mac} not found")

    async def handle_emulate_update(call: ServiceCall) -> None:
        """Handle emulate state update service - sends multiple commands at once."""
        mac = call.data.get("mac")
    
        if not mac:
            _LOGGER.error("MAC address is required")
            return
    
        # Собираем все команды из данных
        commands = []
    
        if "mode" in call.data:
            commands.append(("mode", str(call.data["mode"]), 0, None))
        if "target_temperature" in call.data:
            commands.append(("target_temperature", str(call.data["target_temperature"]), 0, None))
        if "temperature" in call.data:
            commands.append(("temperature", str(call.data["temperature"]), 0, None))
        if "current_temperature" in call.data:
            commands.append(("current_temperature", str(call.data["current_temperature"]), 0, None))
        if "child_lock" in call.data:
            commands.append(("child_lock", "1" if call.data["child_lock"] else "0", 0, None))
        if "backlight" in call.data:
            commands.append(("backlight", "1" if call.data["backlight"] else "0", 0, None))
        if "volume" in call.data:
            commands.append(("volume", "1" if call.data["volume"] else "0", 0, None))
        if "power" in call.data:
            commands.append(("power", "1" if call.data["power"] else "0", 0, None))
        if "speed" in call.data:
            commands.append(("speed", str(call.data["speed"]), 0, None))
        if "error" in call.data:
            commands.append(("error", str(call.data["error"]), 0, None))
        if "program_data" in call.data:
            commands.append(("program_data", "0", call.data.get("mode", 0), call.data.get("data", "00")))
    
        if not commands:
            _LOGGER.warning("No commands to send")
            return
    
        # Отправляем каждую команду напрямую, без создания ServiceCall
        for cmd_type, value, mode, data in commands:
            # Создаем объект, похожий на ServiceCall
            class FakeCall:
                def __init__(self):
                    self.hass = call.hass
                    self.data = {
                        "mac": mac,
                        "command_type": cmd_type,
                        "value": value,
                        "mode": mode,
                        "data": data,
                    }
                    self.context = call.context
                    self.origin = call.origin if hasattr(call, 'origin') else None
            
            fake_call = FakeCall()
            await handle_emulate_command(fake_call)

    async def handle_set_available(call: ServiceCall) -> None:
        """Handle set entity available service."""
        entity_id = call.data.get("entity_id")
        available = call.data.get("available", True)

        if not entity_id:
            _LOGGER.error("entity_id is required")
            return

        # Находим сущность
        if entity_id in hass.states.async_entity_ids():
            # Обновляем состояние
            entity = hass.states.get(entity_id)
            if entity:
                new_attributes = dict(entity.attributes)
                new_attributes["available"] = available

                hass.states.async_set(
                    entity_id,
                    entity.state,
                    new_attributes,
                )
                _LOGGER.info(f"Entity {entity_id} availability set to {available}")
        else:
            _LOGGER.error(f"Entity {entity_id} not found")

    async def handle_list_devices(call: ServiceCall) -> None:
        """Handle list devices service."""
        devices = []
        for entry in hass.config_entries.async_entries(DOMAIN):
            if entry.runtime_data:
                conn = entry.runtime_data
                devices.append(
                    {
                        "mac": entry.data.get(CONF_MAC),
                        "vendor": entry.data.get(CONF_VENDOR),
                        "device_type": entry.data.get(CONF_DEVICE_CLASS),
                        "state": str(conn.state),
                        "ip": entry.data.get(CONF_IP_ADDRESS),
                        "port": entry.data.get(CONF_PORT),
                    }
                )

        if devices:
            _LOGGER.info(f"Active devices: {devices}")
        else:
            _LOGGER.info("No active devices found")

        # Возвращаем как событие для отладки
        hass.bus.async_fire("syncleo_devices_list", {"devices": devices})

    async def handle_emulate_program_data(call: ServiceCall) -> None:
        """Handle emulate program data update."""
        mac = call.data.get("mac")
        mode = call.data.get("mode", 0)
        data = call.data.get("data", "00")

        if not mac:
            _LOGGER.error("MAC address is required")
            return

        await handle_emulate_command(
            ServiceCall(
                DOMAIN,
                "emulate_command",
                {
                    "mac": mac,
                    "command_type": "program_data",
                    "value": "0",
                    "mode": mode,
                    "data": data,
                },
                call.context,
                call.origin,
            )
        )

    async def handle_emulate_discover(call: ServiceCall) -> None:
        """Handle emulate discovery of new device."""
        mac = call.data.get("mac")
        ip = socket.inet_aton(call.data.get("ip", "192.168.1.100"))
        port = call.data.get("port", 54321)
        vendor = call.data.get("vendor", "Polaris")
        device_type = call.data.get("device_type", 56)

        if not mac:
            _LOGGER.error("MAC address is required")
            return

        # Проверяем, есть ли уже такое устройство
        for entry in hass.config_entries.async_entries(DOMAIN):
            if entry.data.get(CONF_MAC) == mac:
                _LOGGER.info(f"Device {mac} already configured")
                return

        # Эмулируем zeroconf обнаружение
        from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo
        from homeassistant.components import zeroconf
        _LOGGER.info("Discover %s", vendor)
        discovery_info = ZeroconfServiceInfo(
            port=port,
            hostname=f"{mac}.local.",
            type="_syncleo._tcp.local.",
            name=f"Syncleo Device {mac}",
            ip_address=ip,
            ip_addresses=[ip],
            properties={
                "public": "0000000000000000000000000000000000000000000000000000000000000123",
                "curve": "29",
                "macaddr": mac,
                "vendor": vendor,
                "devtype": str(device_type),
                "protocol": "2",
                "firmware": "1.0.0",
            }
        )

        # Находим flow и запускаем обнаружение
        for flow in hass.config_entries.flow.async_progress():
            if flow.get("context", {}).get("unique_id") == mac:
                _LOGGER.info(f"Flow already exists for {mac}")
                return

        # Создаем новый flow
        from homeassistant.data_entry_flow import FlowResultType

        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": "zeroconf"},
            data=discovery_info,
        )

        if result.get("type") == FlowResultType.FORM:
            _LOGGER.info(f"Discovery flow started for {mac}. Check UI for confirmation.")
        else:
            _LOGGER.info(f"Discovery result: {result}")

    # Регистрируем сервисы
    hass.services.async_register(DOMAIN, "emulate_connect", handle_emulate_connect)
    hass.services.async_register(DOMAIN, "emulate_command", handle_emulate_command)
    hass.services.async_register(DOMAIN, "emulate_update", handle_emulate_update)
    hass.services.async_register(DOMAIN, "set_available", handle_set_available)
    hass.services.async_register(DOMAIN, "list_devices", handle_list_devices)
    hass.services.async_register(DOMAIN, "emulate_program_data", handle_emulate_program_data)
    hass.services.async_register(DOMAIN, "emulate_discover", handle_emulate_discover)

    _SERVICES_REGISTERED = True
    _LOGGER.info("Syncleo debug services registered")

    # Загружаем сервисы в реестр
#    await hass.services.async_register(DOMAIN, "emulate_connect", handle_emulate_connect)


async def async_unregister_debug_services(hass: HomeAssistant) -> None:
    """Unregister debug services."""
    global _SERVICES_REGISTERED

    if _SERVICES_REGISTERED:
        for service in [
            "emulate_connect",
            "emulate_command",
            "emulate_update",
            "set_available",
            "list_devices",
            "emulate_program_data",
            "emulate_discover",
        ]:
            hass.services.async_remove(DOMAIN, service)

        _SERVICES_REGISTERED = False
        _LOGGER.info("Syncleo debug services unregistered")
        
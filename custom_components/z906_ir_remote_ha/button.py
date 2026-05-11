"""Button platform for stateless Logitech Z906 IR commands."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import CONF_EMITTER_ENTITY_ID, DEFAULT_NAME
from .ir import async_send_z906

PARALLEL_UPDATES = 1


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up Logitech Z906 stateless command buttons from YAML."""
    if discovery_info is None:
        return

    async_add_entities([Z906LevelButton(discovery_info)])


class Z906LevelButton(ButtonEntity):
    """Stateless button for the Logitech Z906 level command."""

    _attr_should_poll = False
    _attr_unique_id = "logitech_z906_level"

    def __init__(self, config: DiscoveryInfoType) -> None:
        """Initialize the Logitech Z906 level button."""
        receiver_name = config.get(CONF_NAME, DEFAULT_NAME)
        self._attr_name = f"{receiver_name} Level"
        self._attr_device_info = DeviceInfo(
            identifiers={("z906_ir_remote_ha", "logitech_z906")},
            manufacturer="Logitech",
            model="Z906",
            name="Logitech Z906",
        )
        self._emitter_entity_id: str = config[CONF_EMITTER_ENTITY_ID]

    async def async_press(self) -> None:
        """Send the stateless level command."""
        await async_send_z906(
            self.hass,
            self._emitter_entity_id,
            "level",
            context=self._context,
        )

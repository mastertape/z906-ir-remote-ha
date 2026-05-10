"""Media player platform for the Logitech Z906 IR receiver."""

from __future__ import annotations

from homeassistant.components.media_player import (
    ATTR_INPUT_SOURCE,
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    CONF_EMITTER_ENTITY_ID,
    CONF_SOURCES,
    DEFAULT_NAME,
    Z906_SOURCE_COMMANDS,
)
from .ir import async_send_z906

PARALLEL_UPDATES = 1


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Logitech Z906 media player from YAML."""
    if discovery_info is None:
        return

    async_add_entities([Z906MediaPlayer(discovery_info)])


class Z906MediaPlayer(RestoreEntity, MediaPlayerEntity):
    """IR-only Logitech Z906 receiver media player."""

    _attr_assumed_state = True
    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_should_poll = False
    _attr_supported_features = (
        MediaPlayerEntityFeature.SELECT_SOURCE | MediaPlayerEntityFeature.VOLUME_STEP
    )

    def __init__(self, config: DiscoveryInfoType) -> None:
        """Initialize the Logitech Z906 media player."""
        self._attr_name = config.get(CONF_NAME, DEFAULT_NAME)
        self._attr_unique_id = "logitech_z906_receiver"
        self._attr_state = MediaPlayerState.ON
        self._attr_device_info = DeviceInfo(
            identifiers={("z906_ir_remote_ha", "logitech_z906")},
            manufacturer="Logitech",
            model="Z906",
            name="Logitech Z906",
        )

        self._emitter_entity_id: str = config[CONF_EMITTER_ENTITY_ID]
        source_labels = Z906_SOURCE_COMMANDS | config.get(CONF_SOURCES, {})
        self._source_to_command = {
            label: command for command, label in source_labels.items()
        }
        self._attr_source_list = list(self._source_to_command)
        self._attr_source: str | None = None

    async def async_added_to_hass(self) -> None:
        """Restore the last optimistically selected source."""
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state is not None and last_state.attributes.get(ATTR_INPUT_SOURCE) in (
            self._attr_source_list or []
        ):
            self._attr_source = last_state.attributes[ATTR_INPUT_SOURCE]

    async def async_select_source(self, source: str) -> None:
        """Select an input source using the Z906 direct input IR commands."""
        if source not in self._source_to_command:
            raise HomeAssistantError(f"Unknown Logitech Z906 source: {source}")

        await async_send_z906(
            self.hass,
            self._emitter_entity_id,
            self._source_to_command[source],
            context=self._context,
        )
        self._attr_source = source
        self.async_write_ha_state()

    async def async_volume_up(self) -> None:
        """Send volume up command."""
        await async_send_z906(
            self.hass,
            self._emitter_entity_id,
            "volume_up",
            context=self._context,
        )

    async def async_volume_down(self) -> None:
        """Send volume down command."""
        await async_send_z906(
            self.hass,
            self._emitter_entity_id,
            "volume_down",
            context=self._context,
        )

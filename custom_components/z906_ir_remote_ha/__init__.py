"""Z906 IR Remote HA integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components.infrared import DOMAIN as INFRARED_DOMAIN
from homeassistant.const import CONF_ENTITY_ID, CONF_NAME, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import discovery
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_EMITTER_ENTITY_ID,
    CONF_SOURCES,
    DEFAULT_EMITTER,
    DEFAULT_NAME,
    DOMAIN,
    Z906_COMMANDS,
    Z906_SOURCE_COMMANDS,
)
from .ir import async_send_nec as async_send_nec_command
from .ir import async_send_z906 as async_send_z906_command
from .ir import parse_int


def _infrared_entity_id(value: str) -> str:
    """Validate an infrared entity ID."""
    entity_id = cv.entity_id(value)
    if entity_id.split(".", 1)[0] != INFRARED_DOMAIN:
        raise vol.Invalid("Entity must be an infrared entity")
    return entity_id


SEND_NEC_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_ENTITY_ID, default=DEFAULT_EMITTER): _infrared_entity_id,
        vol.Required("address"): vol.All(parse_int, vol.Range(min=0, max=0xFFFF)),
        vol.Required("command"): vol.All(parse_int, vol.Range(min=0, max=0xFF)),
        vol.Optional("modulation", default=38000): vol.All(
            vol.Coerce(int), vol.Range(min=30000, max=60000)
        ),
        vol.Optional("repeat_count", default=0): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=5)
        ),
    }
)

SEND_Z906_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_ENTITY_ID, default=DEFAULT_EMITTER): _infrared_entity_id,
        vol.Required("command"): vol.In(list(Z906_COMMANDS)),
        vol.Optional("repeat_count", default=0): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=5)
        ),
    }
)

DOMAIN_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_EMITTER_ENTITY_ID): _infrared_entity_id,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_SOURCES): vol.Schema(
            {vol.Optional(command): cv.string for command in Z906_SOURCE_COMMANDS}
        ),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Any(None, DOMAIN_CONFIG_SCHEMA),
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Z906 IR services and media player."""
    domain_config = config.get(DOMAIN) or {}
    discovery_config = {
        CONF_EMITTER_ENTITY_ID: domain_config.get(
            CONF_EMITTER_ENTITY_ID, DEFAULT_EMITTER
        ),
        CONF_NAME: domain_config.get(CONF_NAME, DEFAULT_NAME),
        CONF_SOURCES: domain_config.get(CONF_SOURCES, {}),
    }

    async def async_send_nec(call: ServiceCall) -> None:
        """Send a generic NEC / extended NEC command."""
        await async_send_nec_command(
            hass,
            call.data[CONF_ENTITY_ID],
            call.data["address"],
            call.data["command"],
            call.data["modulation"],
            repeat_count=call.data["repeat_count"],
            context=call.context,
        )

    async def async_send_z906(call: ServiceCall) -> None:
        """Send a Logitech Z906 command."""
        await async_send_z906_command(
            hass,
            call.data[CONF_ENTITY_ID],
            call.data["command"],
            repeat_count=call.data["repeat_count"],
            context=call.context,
        )

    hass.services.async_register(
        DOMAIN,
        "send_nec",
        async_send_nec,
        schema=SEND_NEC_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        "send_z906",
        async_send_z906,
        schema=SEND_Z906_SCHEMA,
    )

    await discovery.async_load_platform(
        hass,
        Platform.MEDIA_PLAYER,
        DOMAIN,
        discovery_config,
        config,
    )

    return True

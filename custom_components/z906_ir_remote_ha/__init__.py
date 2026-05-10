"""Tiny IR helper services for Home Assistant infrared emitters."""

from __future__ import annotations

import voluptuous as vol

from infrared_protocols import NECCommand

from homeassistant.components import infrared
from homeassistant.components.infrared import DOMAIN as INFRARED_DOMAIN
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

DOMAIN = "z906_ir_remote_ha"

DEFAULT_EMITTER = "infrared.xiao_smart_ir_mate_ir_proxy_transmitter"

Z906_ADDRESS = 0xA002
Z906_MODULATION = 38650

Z906_COMMANDS: dict[str, int] = {
    "power_toggle": 0x80,
    "input_next": 0x08,
    "input_1": 0x04,
    "input_2": 0x82,
    "input_3": 0x0C,
    "input_4": 0x8C,
    "input_5": 0x02,
    "aux": 0x42,
    "mute": 0xEA,
    "level": 0x0A,
    "effect": 0x0E,
    "volume_down": 0x6A,
    "volume_up": 0xAA,
    "test": 0x01,
}


def _parse_int(value: int | str) -> int:
    """Parse decimal or hex values."""
    if isinstance(value, int):
        return value
    return int(value, 0)


def _infrared_entity_id(value: str) -> str:
    """Validate an infrared entity ID."""
    entity_id = cv.entity_id(value)
    if entity_id.split(".", 1)[0] != INFRARED_DOMAIN:
        raise vol.Invalid("Entity must be an infrared entity")
    return entity_id


SEND_NEC_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_ENTITY_ID, default=DEFAULT_EMITTER): _infrared_entity_id,
        vol.Required("address"): vol.All(_parse_int, vol.Range(min=0, max=0xFFFF)),
        vol.Required("command"): vol.All(_parse_int, vol.Range(min=0, max=0xFF)),
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


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up IR helper services."""

    async def async_send_nec(call: ServiceCall) -> None:
        """Send a generic NEC / extended NEC command."""
        ir_command = NECCommand(
            address=call.data["address"],
            command=call.data["command"],
            modulation=call.data["modulation"],
            repeat_count=call.data["repeat_count"],
        )

        await infrared.async_send_command(
            hass,
            call.data[CONF_ENTITY_ID],
            ir_command,
            context=call.context,
        )

    async def async_send_z906(call: ServiceCall) -> None:
        """Send a Logitech Z906 command."""
        ir_command = NECCommand(
            address=Z906_ADDRESS,
            command=Z906_COMMANDS[call.data["command"]],
            modulation=Z906_MODULATION,
            repeat_count=call.data["repeat_count"],
        )

        await infrared.async_send_command(
            hass,
            call.data[CONF_ENTITY_ID],
            ir_command,
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

    return True

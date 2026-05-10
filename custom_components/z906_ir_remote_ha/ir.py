"""Infrared command helpers for the Z906 IR Remote HA integration."""

from __future__ import annotations

from homeassistant.components import infrared
from homeassistant.core import Context, HomeAssistant

from infrared_protocols import NECCommand

from .const import Z906_ADDRESS, Z906_COMMANDS, Z906_MODULATION


def parse_int(value: int | str) -> int:
    """Parse decimal or hex values."""
    if isinstance(value, int):
        return value
    return int(value, 0)


async def async_send_nec(
    hass: HomeAssistant,
    emitter_entity_id: str,
    address: int,
    command: int,
    modulation: int,
    repeat_count: int = 0,
    context: Context | None = None,
) -> None:
    """Send a NEC / extended NEC command through an infrared emitter entity."""
    ir_command = NECCommand(
        address=address,
        command=command,
        modulation=modulation,
        repeat_count=repeat_count,
    )

    await infrared.async_send_command(
        hass,
        emitter_entity_id,
        ir_command,
        context=context,
    )


async def async_send_z906(
    hass: HomeAssistant,
    emitter_entity_id: str,
    command_name: str,
    repeat_count: int = 0,
    context: Context | None = None,
) -> None:
    """Send a known Logitech Z906 command through an infrared emitter entity."""
    await async_send_nec(
        hass,
        emitter_entity_id,
        Z906_ADDRESS,
        Z906_COMMANDS[command_name],
        Z906_MODULATION,
        repeat_count=repeat_count,
        context=context,
    )

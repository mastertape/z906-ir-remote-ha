"""Constants for the Z906 IR Remote HA integration."""

from __future__ import annotations

DOMAIN = "z906_ir_remote_ha"

CONF_EMITTER_ENTITY_ID = "emitter_entity_id"
CONF_INITIAL_MUTE_STATE = "initial_mute_state"
CONF_INITIAL_POWER_STATE = "initial_power_state"
CONF_SOURCES = "sources"

DEFAULT_NAME = "Logitech Z906"
DEFAULT_EMITTER = "infrared.xiao_smart_ir_mate_ir_proxy_transmitter"
DEFAULT_INITIAL_MUTE_STATE = "off"
DEFAULT_INITIAL_POWER_STATE = "on"

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

Z906_SOURCE_COMMANDS: dict[str, str] = {
    "input_1": "INPUT 1",
    "input_2": "INPUT 2",
    "input_3": "OPTICAL 1",
    "input_4": "OPTICAL 2",
    "input_5": "COAX 1",
    "aux": "AUX 1",
}

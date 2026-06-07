"""Configuration helpers for Logitech Z906 IR Remote."""

from __future__ import annotations

from homeassistant.const import CONF_NAME

from .const import (
    CONF_EMITTER_ENTITY_ID,
    CONF_INITIAL_MUTE_STATE,
    CONF_INITIAL_POWER_STATE,
    CONF_SOURCES,
    DEFAULT_EMITTER,
    DEFAULT_INITIAL_MUTE_STATE,
    DEFAULT_INITIAL_POWER_STATE,
    DEFAULT_NAME,
)


def build_config(data: dict) -> dict:
    """Build a complete Z906 runtime config from partial user data."""
    return {
        CONF_EMITTER_ENTITY_ID: data.get(CONF_EMITTER_ENTITY_ID, DEFAULT_EMITTER),
        CONF_INITIAL_MUTE_STATE: data.get(
            CONF_INITIAL_MUTE_STATE, DEFAULT_INITIAL_MUTE_STATE
        ),
        CONF_INITIAL_POWER_STATE: data.get(
            CONF_INITIAL_POWER_STATE, DEFAULT_INITIAL_POWER_STATE
        ),
        CONF_NAME: data.get(CONF_NAME, DEFAULT_NAME),
        CONF_SOURCES: data.get(CONF_SOURCES, {}),
    }

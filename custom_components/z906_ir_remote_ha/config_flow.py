"""Config flow for Logitech Z906 IR Remote."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.infrared import DOMAIN as INFRARED_DOMAIN
from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_EMITTER_ENTITY_ID,
    CONF_INITIAL_MUTE_STATE,
    CONF_INITIAL_POWER_STATE,
    CONF_SOURCES,
    DEFAULT_EMITTER,
    DEFAULT_INITIAL_MUTE_STATE,
    DEFAULT_INITIAL_POWER_STATE,
    DEFAULT_NAME,
    DOMAIN,
    Z906_SOURCE_COMMANDS,
)

SOURCE_FIELD_PREFIX = "source_"
UNIQUE_ID = "logitech_z906"


def _infrared_entity_id(value: str) -> str:
    """Validate an infrared entity ID."""
    entity_id = cv.entity_id(value)
    if entity_id.split(".", 1)[0] != INFRARED_DOMAIN:
        raise vol.Invalid("Entity must be an infrared entity")
    return entity_id


def _source_field(command: str) -> str:
    """Return the config-flow field name for a source command."""
    return f"{SOURCE_FIELD_PREFIX}{command}"


def _schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    """Return the config-flow data schema."""
    defaults = defaults or {}
    sources = defaults.get(CONF_SOURCES, {})

    schema: dict[Any, Any] = {
        vol.Optional(CONF_NAME, default=defaults.get(CONF_NAME, DEFAULT_NAME)): str,
        vol.Required(
            CONF_EMITTER_ENTITY_ID,
            default=defaults.get(CONF_EMITTER_ENTITY_ID, DEFAULT_EMITTER),
        ): _infrared_entity_id,
        vol.Optional(
            CONF_INITIAL_POWER_STATE,
            default=defaults.get(
                CONF_INITIAL_POWER_STATE, DEFAULT_INITIAL_POWER_STATE
            ),
        ): vol.In(("on", "off")),
        vol.Optional(
            CONF_INITIAL_MUTE_STATE,
            default=defaults.get(CONF_INITIAL_MUTE_STATE, DEFAULT_INITIAL_MUTE_STATE),
        ): vol.In(("on", "off")),
    }

    for command, label in Z906_SOURCE_COMMANDS.items():
        schema[
            vol.Optional(_source_field(command), default=sources.get(command, label))
        ] = str

    return vol.Schema(schema)


def _normalize_input(user_input: dict[str, Any]) -> dict[str, Any]:
    """Normalize UI or YAML-import input into config entry data."""
    sources = dict(user_input.get(CONF_SOURCES, {}))
    for command in Z906_SOURCE_COMMANDS:
        field = _source_field(command)
        if field in user_input:
            sources[command] = user_input[field]

    return {
        CONF_NAME: user_input.get(CONF_NAME, DEFAULT_NAME),
        CONF_EMITTER_ENTITY_ID: user_input.get(CONF_EMITTER_ENTITY_ID, DEFAULT_EMITTER),
        CONF_INITIAL_POWER_STATE: user_input.get(
            CONF_INITIAL_POWER_STATE, DEFAULT_INITIAL_POWER_STATE
        ),
        CONF_INITIAL_MUTE_STATE: user_input.get(
            CONF_INITIAL_MUTE_STATE, DEFAULT_INITIAL_MUTE_STATE
        ),
        CONF_SOURCES: sources,
    }


class Z906ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Logitech Z906 IR Remote config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle manual setup from the UI."""
        if user_input is not None:
            return await self._async_create_or_update_entry(_normalize_input(user_input))

        return self.async_show_form(step_id="user", data_schema=_schema())

    async def async_step_import(
        self, user_input: dict[str, Any]
    ) -> config_entries.ConfigFlowResult:
        """Import YAML configuration."""
        return await self._async_create_or_update_entry(_normalize_input(user_input))

    async def _async_create_or_update_entry(
        self, data: dict[str, Any]
    ) -> config_entries.ConfigFlowResult:
        """Create the single config entry or update it from YAML import."""
        await self.async_set_unique_id(UNIQUE_ID)
        self._abort_if_unique_id_configured(updates=data)

        return self.async_create_entry(title=data[CONF_NAME], data=data)

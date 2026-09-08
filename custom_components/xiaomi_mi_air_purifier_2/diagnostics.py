"""Diagnostics for Xiaomi Mi Air Purifier 2."""

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_TOKEN, DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return redacted diagnostics."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    status = coordinator.data
    properties = getattr(status, "data", None) or getattr(status, "_data", None)
    return {
        "config_entry": async_redact_data(dict(entry.data), {CONF_TOKEN}),
        "device_info": str(coordinator.device_info_data),
        "status": dict(properties) if isinstance(properties, dict) else str(status),
    }

"""Xiaomi Mi Air Purifier 2 integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from miio import AirPurifier

from .const import CONF_TOKEN, DOMAIN, PLATFORMS
from .coordinator import XiaomiAirPurifierCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Xiaomi Mi Air Purifier 2 from a config entry."""
    device = AirPurifier(entry.data[CONF_HOST], entry.data[CONF_TOKEN])
    coordinator = XiaomiAirPurifierCoordinator(hass, entry, device)
    await coordinator.async_initialize()
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)
    return unloaded

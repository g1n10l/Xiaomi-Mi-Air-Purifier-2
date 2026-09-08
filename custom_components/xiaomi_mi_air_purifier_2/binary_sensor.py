"""Binary sensors for Xiaomi Mi Air Purifier 2."""

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import status_value
from .entity import XiaomiAirPurifierEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up purifier binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [XiaomiAirPurifierFilterWarning(coordinator, entry.entry_id, "filter_warning")]
    )


class XiaomiAirPurifierFilterWarning(XiaomiAirPurifierEntity, BinarySensorEntity):
    """Report when the filter has reached the end of its life."""

    _attr_translation_key = "filter_warning"
    _attr_icon = "mdi:air-filter"

    @property
    def is_on(self) -> bool | None:
        """Return whether the filter needs replacement."""
        life = status_value(self.coordinator.data, "filter_life_remaining")
        return None if life is None else int(life) <= 0

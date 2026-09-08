"""Number entities for Xiaomi Mi Air Purifier 2."""

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import status_value
from .entity import XiaomiAirPurifierEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up purifier number entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    if status_value(coordinator.data, "favorite_level") is not None:
        async_add_entities(
            [
                XiaomiAirPurifierFavoriteLevel(
                    coordinator, entry.entry_id, "favorite_level"
                )
            ]
        )


class XiaomiAirPurifierFavoriteLevel(XiaomiAirPurifierEntity, NumberEntity):
    """Set the favorite mode fan level."""

    _attr_translation_key = "favorite_level"
    _attr_icon = "mdi:fan-chevron-up"
    _attr_native_min_value = 1
    _attr_native_max_value = 16
    _attr_native_step = 1

    @property
    def native_value(self) -> float | None:
        """Return the favorite level."""
        value = status_value(self.coordinator.data, "favorite_level")
        return None if value is None else float(value)

    async def async_set_native_value(self, value: float) -> None:
        """Set the favorite level."""
        await self.coordinator.async_command(
            self.coordinator.device.set_favorite_level, int(value)
        )

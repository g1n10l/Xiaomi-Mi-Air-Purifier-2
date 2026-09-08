"""Select entities for Xiaomi Mi Air Purifier 2."""

from typing import ClassVar

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from miio.integrations.airpurifier.zhimi.airpurifier import LedBrightness

from .const import DOMAIN
from .coordinator import status_value
from .entity import XiaomiAirPurifierEntity

OPTIONS = {
    "Bright": LedBrightness.Bright,
    "Dim": LedBrightness.Dim,
    "Off": LedBrightness.Off,
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up purifier selects."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    if (
        hasattr(coordinator.device, "set_led_brightness")
        and status_value(coordinator.data, "led_brightness") is not None
    ):
        async_add_entities(
            [
                XiaomiAirPurifierLedBrightness(
                    coordinator, entry.entry_id, "led_brightness"
                )
            ]
        )


class XiaomiAirPurifierLedBrightness(XiaomiAirPurifierEntity, SelectEntity):
    """Select the LED brightness."""

    _attr_translation_key = "led_brightness"
    _attr_icon = "mdi:brightness-6"
    _attr_options: ClassVar[list[str]] = list(OPTIONS)

    @property
    def current_option(self) -> str | None:
        """Return the selected LED brightness."""
        value = status_value(self.coordinator.data, "led_brightness")
        raw = getattr(value, "value", value)
        for option, enum_value in OPTIONS.items():
            if value == enum_value or raw == enum_value.value:
                return option
        return None

    async def async_select_option(self, option: str) -> None:
        """Set LED brightness."""
        await self.coordinator.async_command(
            self.coordinator.device.set_led_brightness, OPTIONS[option]
        )

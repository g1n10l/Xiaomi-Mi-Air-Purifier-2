"""Switches for Xiaomi Mi Air Purifier 2."""

from dataclasses import dataclass

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import XiaomiAirPurifierCoordinator, status_value
from .entity import XiaomiAirPurifierEntity


@dataclass(frozen=True, kw_only=True)
class PurifierSwitchDescription(SwitchEntityDescription):
    """Describe a purifier switch."""

    status_key: str
    command_name: str


SWITCHES = (
    PurifierSwitchDescription(
        key="buzzer",
        translation_key="buzzer",
        status_key="buzzer",
        command_name="set_buzzer",
    ),
    PurifierSwitchDescription(
        key="child_lock",
        translation_key="child_lock",
        status_key="child_lock",
        command_name="set_child_lock",
    ),
    PurifierSwitchDescription(
        key="led", translation_key="led", status_key="led", command_name="set_led"
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up purifier switches."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        XiaomiAirPurifierSwitch(coordinator, entry.entry_id, description)
        for description in SWITCHES
        if hasattr(coordinator.device, description.command_name)
        and status_value(coordinator.data, description.status_key) is not None
    )


class XiaomiAirPurifierSwitch(XiaomiAirPurifierEntity, SwitchEntity):
    """Control one purifier setting."""

    entity_description: PurifierSwitchDescription

    def __init__(
        self,
        coordinator: XiaomiAirPurifierCoordinator,
        entry_id: str,
        description: PurifierSwitchDescription,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, entry_id, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool:
        """Return the setting state."""
        return bool(
            status_value(
                self.coordinator.data, self.entity_description.status_key, False
            )
        )

    async def async_turn_on(self, **kwargs: object) -> None:
        """Enable the setting."""
        command = getattr(self.coordinator.device, self.entity_description.command_name)
        await self.coordinator.async_command(command, True)

    async def async_turn_off(self, **kwargs: object) -> None:
        """Disable the setting."""
        command = getattr(self.coordinator.device, self.entity_description.command_name)
        await self.coordinator.async_command(command, False)

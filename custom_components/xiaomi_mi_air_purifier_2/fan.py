"""Fan entity for Xiaomi Mi Air Purifier 2."""

from typing import ClassVar

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from miio.integrations.airpurifier.zhimi.airpurifier import OperationMode

from .const import DOMAIN
from .coordinator import status_value
from .entity import XiaomiAirPurifierEntity

PRESET_TO_MODE = {
    "Auto": OperationMode.Auto,
    "Silent": OperationMode.Silent,
    "Favorite": OperationMode.Favorite,
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the fan entity."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([XiaomiAirPurifierFan(coordinator, entry.entry_id, "fan")])


class XiaomiAirPurifierFan(XiaomiAirPurifierEntity, FanEntity):
    """Control the purifier as a fan."""

    _attr_translation_key = "air_purifier"
    _attr_supported_features = (
        FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_ON
        | FanEntityFeature.TURN_OFF
    )
    _attr_preset_modes: ClassVar[list[str]] = list(PRESET_TO_MODE)
    _attr_speed_count = 16

    @property
    def is_on(self) -> bool:
        """Return whether the purifier is on."""
        is_on = status_value(self.coordinator.data, "is_on")
        if is_on is not None:
            return bool(is_on)
        return status_value(self.coordinator.data, "power") == "on"

    @property
    def percentage(self) -> int | None:
        """Return the favorite level as a percentage."""
        level = status_value(self.coordinator.data, "favorite_level")
        return None if level is None else round(max(1, min(16, int(level))) / 16 * 100)

    @property
    def preset_mode(self) -> str | None:
        """Return the current operating mode."""
        mode = status_value(self.coordinator.data, "mode")
        if mode is None:
            return None
        raw = getattr(mode, "value", mode)
        for preset, operation_mode in PRESET_TO_MODE.items():
            if mode == operation_mode or raw == operation_mode.value:
                return preset
        return str(raw).title()

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: object,
    ) -> None:
        """Turn on the purifier."""
        commands = [(self.coordinator.device.on, ())]
        if preset_mode is not None:
            if preset_mode not in PRESET_TO_MODE:
                raise ValueError(f"Unsupported preset mode: {preset_mode}")
            commands.append(
                (self.coordinator.device.set_mode, (PRESET_TO_MODE[preset_mode],))
            )
        elif percentage is not None:
            level = self._percentage_to_level(percentage)
            commands.extend(
                (
                    (self.coordinator.device.set_favorite_level, (level,)),
                    (self.coordinator.device.set_mode, (OperationMode.Favorite,)),
                )
            )
        await self.coordinator.async_execute_commands(commands)

    async def async_turn_off(self, **kwargs: object) -> None:
        """Turn off the purifier."""
        await self.coordinator.async_command(self.coordinator.device.off)

    async def async_set_percentage(self, percentage: int) -> None:
        """Set favorite fan level from a Home Assistant percentage."""
        if percentage == 0:
            await self.async_turn_off()
            return
        level = self._percentage_to_level(percentage)
        await self.coordinator.async_execute_commands(
            (
                (self.coordinator.device.set_favorite_level, (level,)),
                (self.coordinator.device.set_mode, (OperationMode.Favorite,)),
            )
        )

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the operating mode."""
        if preset_mode not in PRESET_TO_MODE:
            raise ValueError(f"Unsupported preset mode: {preset_mode}")
        await self.coordinator.async_command(
            self.coordinator.device.set_mode, PRESET_TO_MODE[preset_mode]
        )

    @staticmethod
    def _percentage_to_level(percentage: int) -> int:
        """Convert a Home Assistant percentage to a favorite level."""
        return max(1, min(16, round(percentage * 16 / 100)))

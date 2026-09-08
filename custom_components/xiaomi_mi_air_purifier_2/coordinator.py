"""Data coordinator for Xiaomi Mi Air Purifier 2."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable, Sequence
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from miio import AirPurifier, DeviceException

from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)
DeviceCommand = tuple[Callable[..., Any], tuple[Any, ...]]


def status_value(status: Any, name: str, default: Any = None) -> Any:
    """Read a python-miio status value across library versions."""
    value = getattr(status, name, default)
    return value() if callable(value) else value


class XiaomiAirPurifierCoordinator(DataUpdateCoordinator[Any]):
    """Coordinate device polling and commands."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, device: AirPurifier
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
            always_update=False,
        )
        self.device = device
        self.device_info_data: Any | None = None
        self._command_lock = asyncio.Lock()

    async def async_initialize(self) -> None:
        """Read static device information."""
        try:
            self.device_info_data = await self.hass.async_add_executor_job(
                self.device.info
            )
        except DeviceException as err:
            _LOGGER.debug("Could not read device information: %s", err)

    async def _async_update_data(self) -> Any:
        """Fetch the latest device status."""
        try:
            async with self._command_lock:
                return await self.hass.async_add_executor_job(self.device.status)
        except DeviceException as err:
            raise UpdateFailed(
                f"Unable to communicate with the air purifier: {err}"
            ) from err

    async def async_execute_commands(self, commands: Sequence[DeviceCommand]) -> None:
        """Run device commands serially and refresh state once."""
        try:
            async with self._command_lock:
                for command, args in commands:
                    await self.hass.async_add_executor_job(command, *args)
        except DeviceException as err:
            raise HomeAssistantError(
                f"The air purifier did not accept the command: {err}"
            ) from err
        await self.async_request_refresh()

    async def async_command(self, command: Callable[..., Any], *args: Any) -> None:
        """Run one device command and refresh state."""
        await self.async_execute_commands(((command, args),))

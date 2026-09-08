"""Base entity for Xiaomi Mi Air Purifier 2."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, NAME
from .coordinator import XiaomiAirPurifierCoordinator


class XiaomiAirPurifierEntity(CoordinatorEntity[XiaomiAirPurifierCoordinator]):
    """Base coordinator entity."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: XiaomiAirPurifierCoordinator, entry_id: str, key: str
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        info = coordinator.device_info_data
        model = getattr(info, "model", None) or NAME
        mac = getattr(info, "mac_address", None) or getattr(info, "mac", None)
        identifier = str(mac or entry_id).lower()
        self._attr_unique_id = f"{identifier}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, identifier)},
            manufacturer=MANUFACTURER,
            model=model,
            name=NAME,
            sw_version=getattr(info, "firmware_version", None),
            hw_version=getattr(info, "hardware_version", None),
        )

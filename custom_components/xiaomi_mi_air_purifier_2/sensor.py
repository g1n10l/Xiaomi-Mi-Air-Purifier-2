"""Sensors for Xiaomi Mi Air Purifier 2."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import XiaomiAirPurifierCoordinator, status_value
from .entity import XiaomiAirPurifierEntity


@dataclass(frozen=True, kw_only=True)
class PurifierSensorDescription(SensorEntityDescription):
    """Describe a purifier sensor."""

    value_fn: Callable[[Any], Any]


SENSORS = (
    PurifierSensorDescription(
        key="aqi",
        translation_key="aqi",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.PM25,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda status: status_value(status, "aqi"),
    ),
    PurifierSensorDescription(
        key="temperature",
        translation_key="temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda status: status_value(status, "temperature"),
    ),
    PurifierSensorDescription(
        key="humidity",
        translation_key="humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda status: status_value(status, "humidity"),
    ),
    PurifierSensorDescription(
        key="filter_life_remaining",
        translation_key="filter_life_remaining",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda status: status_value(status, "filter_life_remaining"),
    ),
    PurifierSensorDescription(
        key="filter_hours_used",
        translation_key="filter_hours_used",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda status: status_value(status, "filter_hours_used"),
    ),
    PurifierSensorDescription(
        key="motor_speed",
        translation_key="motor_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda status: status_value(status, "motor_speed"),
    ),
    PurifierSensorDescription(
        key="use_time",
        translation_key="use_time",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda status: status_value(status, "use_time"),
    ),
    PurifierSensorDescription(
        key="purify_volume",
        translation_key="purify_volume",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda status: status_value(status, "purify_volume"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up purifier sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        XiaomiAirPurifierSensor(coordinator, entry.entry_id, description)
        for description in SENSORS
        if description.value_fn(coordinator.data) is not None
    )


class XiaomiAirPurifierSensor(XiaomiAirPurifierEntity, SensorEntity):
    """Represent one purifier measurement."""

    entity_description: PurifierSensorDescription

    def __init__(
        self,
        coordinator: XiaomiAirPurifierCoordinator,
        entry_id: str,
        description: PurifierSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry_id, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        """Return the current measurement."""
        return self.entity_description.value_fn(self.coordinator.data)

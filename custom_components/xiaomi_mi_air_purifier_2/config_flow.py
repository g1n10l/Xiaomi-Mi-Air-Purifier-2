"""Config flow for Xiaomi Mi Air Purifier 2."""

from __future__ import annotations

import re
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from miio import AirPurifier, DeviceException

from .const import CONF_TOKEN, DOMAIN, NAME, SUPPORTED_MODELS

TOKEN_PATTERN = re.compile(r"^[0-9a-fA-F]{32}$")


async def _validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, str]:
    """Connect to the purifier and return identifying data."""
    device = AirPurifier(data[CONF_HOST], data[CONF_TOKEN])
    try:
        info = await hass.async_add_executor_job(device.info)
        await hass.async_add_executor_job(device.status)
    except DeviceException as err:
        raise CannotConnect from err
    model = getattr(info, "model", None) or "unknown"
    if model not in SUPPORTED_MODELS:
        raise UnsupportedModel(model)
    mac = getattr(info, "mac_address", None) or getattr(info, "mac", None)
    return {"title": NAME, "unique_id": str(mac or data[CONF_HOST]).lower()}


class XiaomiMiAirPurifier2ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the integration config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial setup step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            if not TOKEN_PATTERN.fullmatch(user_input[CONF_TOKEN]):
                errors[CONF_TOKEN] = "invalid_token"
            else:
                try:
                    result = await _validate_input(self.hass, user_input)
                except CannotConnect:
                    errors["base"] = "cannot_connect"
                except UnsupportedModel:
                    errors["base"] = "unsupported_model"
                except Exception:  # noqa: BLE001
                    errors["base"] = "unknown"
                else:
                    await self.async_set_unique_id(result["unique_id"])
                    self._abort_if_unique_id_configured(updates=user_input)
                    return self.async_create_entry(
                        title=result["title"], data=user_input
                    )
        schema = vol.Schema(
            {vol.Required(CONF_HOST): str, vol.Required(CONF_TOKEN): str}
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)


class CannotConnect(Exception):
    """Raised when the device cannot be reached."""


class UnsupportedModel(Exception):
    """Raised when the connected model is not an Air Purifier 2 variant."""

"""Config flow for HyperVoice TTS integration."""

from __future__ import annotations

from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY

from .const import API_BASE_URL, DOMAIN

USER_STEP_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
    }
)


async def _validate_api_key(hass, api_key: str) -> None:
    """Validate the API key by listing voices."""
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{API_BASE_URL}/voices",
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as resp:
            if resp.status in (401, 403):
                raise InvalidAuth
            if resp.status != 200:
                raise CannotConnect


class HyperVoiceConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HyperVoice TTS."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            api_key = user_input[CONF_API_KEY].strip()
            await self.async_set_unique_id(api_key)
            self._abort_if_unique_id_configured()

            try:
                await _validate_api_key(self.hass, api_key)
            except InvalidAuth:
                errors["base"] = "invalid_api_key"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="HyperVoice TTS",
                    data={CONF_API_KEY: api_key},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=USER_STEP_SCHEMA,
            errors=errors,
        )


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""

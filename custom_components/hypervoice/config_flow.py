"""Config flow for HyperVoice TTS integration."""

from __future__ import annotations

from typing import Any

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
    """Validate the API key by calling the TTS endpoint with empty text."""
    import aiohttp

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "text": "test",
        "voice_name": "emma",
        "speaking_rate": 15,
        "context_aware": True,
    }

    session = aiohttp.ClientSession()
    try:
        async with session.post(
            f"{API_BASE_URL}/text-to-speech",
            json=payload,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as resp:
            if resp.status == 401 or resp.status == 403:
                raise InvalidAuth
            if resp.status != 200:
                raise CannotConnect
    finally:
        session.close()


class HyperVoiceConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HyperVoice TTS."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_API_KEY])
            self._abort_if_unique_id_configured()

            try:
                await _validate_api_key(self.hass, user_input[CONF_API_KEY])
            except InvalidAuth:
                errors["base"] = "invalid_api_key"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="HyperVoice TTS",
                    data=user_input,
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

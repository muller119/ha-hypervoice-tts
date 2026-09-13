"""The HyperVoice TTS integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant

from .const import API_BASE_URL, DOMAIN

PLATFORMS = [Platform.TTS]


@dataclass(kw_only=True, slots=True)
class HyperVoiceData:
    """Runtime data for HyperVoice TTS."""

    api_key: str


type HyperVoiceConfigEntry = ConfigEntry[HyperVoiceData]


async def async_setup_entry(hass: HomeAssistant, entry: HyperVoiceConfigEntry) -> bool:
    """Set up HyperVoice TTS from a config entry."""
    entry.runtime_data = HyperVoiceData(api_key=entry.data[CONF_API_KEY])
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: HyperVoiceConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

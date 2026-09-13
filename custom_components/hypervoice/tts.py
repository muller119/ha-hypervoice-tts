"""HyperVoice TTS platform."""

from __future__ import annotations

from typing import Any

import aiohttp

from homeassistant.components.tts import (
    TextToSpeechEntity,
    TtsAudioType,
    Voice,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import HyperVoiceConfigEntry
from .const import (
    API_BASE_URL,
    CONF_SPEED,
    CONF_VOICE,
    DEFAULT_SPEED,
    DEFAULT_VOICE,
    DOMAIN,
    VOICES,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HyperVoiceConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up HyperVoice TTS entities from config entry."""
    async_add_entities([HyperVoiceTTSEntity(config_entry)])


class HyperVoiceTTSEntity(TextToSpeechEntity):
    """HyperVoice TTS entity."""

    _attr_supported_languages = ["en"]
    _attr_default_language = "en"
    _attr_supported_options = ["voice", "speed"]
    _attr_default_options = {
        CONF_VOICE: DEFAULT_VOICE,
        CONF_SPEED: DEFAULT_SPEED,
    }
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, config_entry: HyperVoiceConfigEntry) -> None:
        """Initialize the entity."""
        self._api_key = config_entry.runtime_data.api_key
        self._attr_unique_id = config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            manufacturer="TaskAGI",
            model="HyperVoice V5",
            name="HyperVoice TTS",
            entry_type=DeviceEntryType.SERVICE,
        )

    @callback
    def async_get_supported_voices(self, language: str) -> list[Voice] | None:
        """Return supported voices."""
        return [Voice(voice_id=vid, name=name) for vid, name in VOICES]

    async def async_get_tts_audio(
        self,
        message: str,
        language: str,
        options: dict[str, Any],
    ) -> TtsAudioType:
        """Generate TTS audio from HyperVoice V5 API."""
        voice = options.get(CONF_VOICE, DEFAULT_VOICE)
        speed = options.get(CONF_SPEED, DEFAULT_SPEED)

        payload: dict[str, Any] = {
            "text": message,
            "voice": voice,
            "speed": speed,
            "format": "mp3",
        }

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_BASE_URL}/tts",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise HomeAssistantError(
                        f"HyperVoice API error {resp.status}: {text}"
                    )
                data = await resp.json()

        if not data.get("success"):
            raise HomeAssistantError(
                f"HyperVoice API returned success=false: {data}"
            )

        audio_url = data.get("audio_url")
        if not audio_url:
            raise HomeAssistantError("HyperVoice API returned no audio_url")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                audio_url,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:
                if resp.status != 200:
                    raise HomeAssistantError(
                        f"Failed to download audio from {audio_url}: {resp.status}"
                    )
                audio_data = await resp.read()

        return "mp3", audio_data

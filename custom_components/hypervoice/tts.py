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
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import HyperVoiceConfigEntry
from .const import (
    API_BASE_URL,
    CONF_CONTEXT_AWARE,
    CONF_SPEAKING_RATE,
    CONF_VOICE_NAME,
    DEFAULT_SPEAKING_RATE,
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
    _attr_supported_options = ["voice", "speaking_rate", "context_aware"]
    _attr_default_options = {
        CONF_VOICE_NAME: DEFAULT_VOICE,
        CONF_SPEAKING_RATE: DEFAULT_SPEAKING_RATE,
        CONF_CONTEXT_AWARE: True,
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
            model="HyperVoice V4",
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
        """Generate TTS audio from HyperVoice API."""
        voice_name = options.get(CONF_VOICE_NAME, DEFAULT_VOICE)
        speaking_rate = options.get(CONF_SPEAKING_RATE, DEFAULT_SPEAKING_RATE)
        context_aware = options.get(CONF_CONTEXT_AWARE, True)

        payload: dict[str, Any] = {
            "text": message,
            "voice_name": voice_name,
            "speaking_rate": speaking_rate,
            "context_aware": context_aware,
        }

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_BASE_URL}/text-to-speech",
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

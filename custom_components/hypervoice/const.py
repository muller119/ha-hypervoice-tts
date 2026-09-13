"""Constants for the HyperVoice TTS integration."""

DOMAIN = "hypervoice"
CONF_VOICE_NAME = "voice_name"
CONF_SPEAKING_RATE = "speaking_rate"
CONF_CONTEXT_AWARE = "context_aware"

DEFAULT_VOICE = "emma"
DEFAULT_SPEAKING_RATE = 15

API_BASE_URL = "https://taskagi.net/api/hypervoice/v4"

VOICES = [
    ("emma", "Emma"),
    ("peter", "Peter"),
    ("V3_af_alloy", "Alloy (V3)"),
    ("V3_af_aoede", "Aoede (V3)"),
    ("V3_af_bella", "Bella (V3)"),
    ("V3_af_jessica", "Jessica (V3)"),
    ("V3_af_kore", "Kore (V3)"),
    ("V3_af_nicole", "Nicole (V3)"),
    ("V3_af_nova", "Nova (V3)"),
    ("V3_af_river", "River (V3)"),
    ("V3_af_sarah", "Sarah (V3)"),
    ("V3_af_sky", "Sky (V3)"),
    ("V3_am_adam", "Adam (V3)"),
    ("V3_am_echo", "Echo (V3)"),
]

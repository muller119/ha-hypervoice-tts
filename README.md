# HyperVoice TTS for Home Assistant

[![hacs][hacsbadge]][hacs]

Gebruik de [HyperVoice V4 API](https://github.com/TaskAGI/HyperVoice) van TaskAGI voor text-to-speech in Home Assistant.

[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg
[hacs]: https://github.com/hacs/integration

## Kenmerken

- 14 voices: Emma, Peter, en 12 V3 varianten
- Context-aware emotieaanpassing (standaard aan)
- Spreeksnelheid instelbaar
- Config flow UI voor eenvoudige installatie

## Installatie

### Via HACS (aanbevolen)

1. Open HACS in Home Assistant
2. Ga naar **Integraties**
3. Zoek **HyperVoice TTS**
4. Klik op **Downloaden**
5. Herstart Home Assistant

### Handmatig

1. Download deze repository
2. Kopieer de `custom_components/hypervoice` map naar je Home Assistant `config/custom_components/` directory
3. Herstart Home Assistant

## Configuratie

1. Ga naar **Instellingen > Integraties > Toevoegen**
2. Zoek **HyperVoice TTS**
3. Voer je TaskAGI API key in

### API Key

Vrij uw API key aan bij [TaskAGI](https://taskagi.net).

## Gebruik

### Via de UI

Ga naar **Instellingen > Apparaten & Diensten > HyperVoice TTS** om de TTS entity te vinden.

### Via een service call

```yaml
action: tts.speak
target:
  entity_id: tts.hypervoice_tts
data:
  message: "Hallo, welkom thuis!"
  media_player_entity_id: media_player.living_room
```

### In een automatisering

```yaml
automation:
  - alias: Welkomsbericht
    trigger:
      - platform: state
        entity_id: group.family
        to: "home"
    actions:
      - action: tts.speak
        target:
          entity_id: tts.hypervoice_tts
        data:
          message: "{{ trigger.to_state.name }} is thuis gekomen!"
          media_player_entity_id: media_player.living_room
```

## Options

| Optie | Standaard | Beschrijving |
|-------|-----------|--------------|
| `voice` | `emma` | De voice die gebruikt wordt |
| `speaking_rate` | `15` | Spreeksnelheid (hoger = sneller) |
| `context_aware` | `true` | Automatische emotieaanpassing |

### Beschikbare Voices

| Voice ID | Naam |
|----------|------|
| `emma` | Emma |
| `peter` | Peter |
| `V3_af_alloy` | Alloy (V3) |
| `V3_af_aoede` | Aoede (V3) |
| `V3_af_bella` | Bella (V3) |
| `V3_af_jessica` | Jessica (V3) |
| `V3_af_kore` | Kore (V3) |
| `V3_af_nicole` | Nicole (V3) |
| `V3_af_nova` | Nova (V3) |
| `V3_af_river` | River (V3) |
| `V3_af_sarah` | Sarah (V3) |
| `V3_af_sky` | Sky (V3) |
| `V3_am_adam` | Adam (V3) |
| `V3_am_echo` | Echo (V3) |

## Debugging

Voeg dit toe aan je `configuration.yaml` voor debug logging:

```yaml
logger:
  logs:
    custom_components.hypervoice: debug
```

## Licentie

[MIT License](LICENSE)

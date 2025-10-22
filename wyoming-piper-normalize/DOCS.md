# Home Assistant Add-on: Wyoming Piper Normalize

## Installation

Follow these steps to get the add-on installed on your system:

1. Navigate in your Home Assistant frontend to **Settings** -> **Add-ons** -> **Add-on store**.
2. Find the "Piper RUNorm" add-on and click it.
3. Click on the "INSTALL" button.

## How to use

After this add-on is installed and running, it will be automatically discovered by the Wyoming integration in
Home Assistant. To finish the setup, click the following my button:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=wyoming)

Alternatively, you can install the Wyoming integration manually, see the
[Wyoming integration documentation](https://www.home-assistant.io/integrations/wyoming/)
for more information.

## Configuration

### Option: `voice`

[Listen to voice samples](https://rhasspy.github.io/piper-samples/)

Name of the Piper voice to use, such as `ru_RU-irina-medium` (the default).
Only Russian-language models are listed, as Russian text normalization is used. If you plan to use voice models in
other languages, please use the original add-on.
Voice models are automatically downloaded from https://huggingface.co/rhasspy/piper-voices/tree/main

Original voices are named according to the following scheme: `<language>_<REGION>-<name>-<quality>`
The `<name>` portion comes from the dataset used to train the voice or the speaker's name if it was provided.

A voice's quality comes in 4 different levels:

- `x_low` - 16Khz, smallest/fastest
- `low` - 16Khz, fast
- `medium` - 22.05Khz, slower but better sounding
- `high` - 22.05Khz, slowest but best sounding

On a Raspberry Pi 4, up to the `medium` models will run with usable speed. If audio quality is not a priority, prefer the `low` or `x-low` voices as they will be noticeably faster than `medium`.

### Option: `speaker`

Speaker number to use if the voice supports multiple speakers, such as [`en-us-libritts-high`](https://rhasspy.github.io/piper-samples/#en-us-libritts-high).

By default, the first speaker (speaker 0) will be used.

### Option: `volume`

Makes the voice quieter or louder. A value of 1.0 means to use the default volume level, with < 1.0 being quieter and > 1.0 being louder.

### Option: `length_scale`

Speeds up or slows down the voice. A value of 1.0 means to use the voice's default speaking rate, with < 1.0 being faster and > 1.0 being slower.

### Option: `noise_scale`

Controls the variability of audio by adding noise during audio generation. The effect highly depends on the voice itself, but in general a value of 0 removes variability and values above 1 will start to degrade audio.

### Option: `noise_w`

Controls the variability of speaking cadence (phoneme widths). The effect highly depends on the voice itself, but in general a value of 0 removes variability and values above 1 produce extreme stutters and pauses.

### Option: `streaming`

Enable support for streaming audio. This breaks apart text at sentence boundaries and streams the audio as its being produced. Requires at least HA 2025.7.

### Option: `update_voices`

Download the list of new voices automatically every time the add-on starts. You must also reload the Wyoming integration for Piper in Home Assistant to see new voices.

### Option: `debug_logging`

Print DEBUG level messages to the add-on's log.
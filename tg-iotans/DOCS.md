# Home Assistant Add-on: TG Iotans

This Home Assistant add-on runs a lightweight Telegram client that automatically retrieves available water meter
readings from the [MyIotansBot](https://t.me/MyIotansBot).
It is designed to integrate these readings into your Home Assistant environment for further automation, monitoring, and
analytics.

## Features

- Connects to Telegram using your personal API credentials
- Authenticates via a local session token
- Communicates with [MyIotansBot](https://t.me/MyIotansBot) to fetch available water meter data
- Runs continuously inside Home Assistant as an isolated add-on
- Publishes data to MQTT topics for integration with Home Assistant sensors
- Provides a foundation for creating sensors, automations, and dashboards

## Requirements

Before running the add-on, you must prepare two things:
1. **Telegram API credentials** 
   - `api_id`
   - `api_hash`

    These are obtained from [official Telegram developer portal](https://my.telegram.org/apps)

2. **Telegram session token**
   
    This token is generated locally using the `tg_iotans` Python module.

## Generating the Session Token

The add-on does not perform Telegram login directly.
You must authenticate once on your local machine to generate a reusable session token.

### Steps:

1. Run the module `tg_iotans` to start the login process
   ```
   python -m tg_iotans --api-id 00000 --api-hash xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

2. Follow the interactive prompts:
   - Enter your **phone number**
   - Enter the **SMS** or **Telegram code**
   - Enter your **cloud password** (if your account has one)

3. After successful authentication, the tool will generate a **session token**
4. Copy this token into the add-on configuration in Home Assistant

## Installation

Follow these steps to get the add-on installed on your system:

1. Navigate in your Home Assistant frontend to **Settings** -> **Add-ons** -> **Add-on store**.
2. Find the "TG Iotans" add-on and click it.
3. Click on the "INSTALL" button.

## Configuration

### Option: `api_id`

Telegram App Api ID from [official Telegram developer portal](https://my.telegram.org/apps)

### Option: `api_hash`

Telegram App Api Hash from [official Telegram developer portal](https://my.telegram.org/apps)

### Option: `session`

Session token generated using `tg_iotans`. See [Generating the Session Token](#generating-the-session-token)

### Option: `interval`

Polling frequency in minutes.

By default, 240 minutes (4 hours).

### Option: `debug`

Print DEBUG level messages to the add-on's log.
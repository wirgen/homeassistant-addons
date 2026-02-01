#!/usr/bin/env python3
"""TG IoT Sensors addon for Home Assistant."""
import argparse
import asyncio
import json
import logging

import paho.mqtt.publish as publish
from tg_iotans import get_data

_LOGGER = logging.getLogger(__name__)


def clean_mac_for_topic(mac: str):
    """Clean MAC address to be used as MQTT topic."""
    return ''.join(c if c.isalnum() else '_' for c in mac.lower())


async def main():
    """Main entrypoint for the addon."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-id",
        type=int,
        help="Telegram App Api ID",
    )
    parser.add_argument(
        "--api-hash",
        type=str,
        help="Telegram App Api Hash",
    )
    parser.add_argument(
        "--session",
        type=str,
        help="Session Token",
    )
    #
    parser.add_argument(
        "--mqtt-host",
        type=str,
        help="MQTT Host",
    )
    parser.add_argument(
        "--mqtt-port",
        type=int,
        help="MQTT Port",
    )
    parser.add_argument(
        "--mqtt-username",
        type=str,
        help="MQTT Username",
    )
    parser.add_argument(
        "--mqtt-password",
        type=str,
        help="MQTT Password",
    )
    #
    parser.add_argument(
        "--interval",
        type=int,
        default=240,
        help="Polling frequency in minutes",
    )
    #
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO
    )

    mqtt_host = args.mqtt_host
    mqtt_port = int(args.mqtt_port)
    mqtt_auth = None if args.mqtt_username is None or args.mqtt_password is None else \
        {
            "username": args.mqtt_username,
            "password": args.mqtt_password,
        }

    while True:
        try:
            meters = await get_data(args.api_id, args.api_hash, args.session)
            _LOGGER.debug(meters)

            prefix = "tg_iotans"

            publish.single(
                "homeassistant/sensor/tg_iotans_addon/version/config",
                payload=json.dumps({
                    "name": "Version",
                    "unique_id": "tg_iotans_addon_version",
                    "state_topic": f"{prefix}/addon/state",
                    "value_template": "{{ value_json.version }}",
                    "icon": "mdi:access-point-network",
                    "device": {
                        "identifiers": ["tg_iotans_addon"],
                        "manufacturer": "TG Iotans",
                        "model": "Addon",
                        "name": "TG Iotans Addon",
                        "sw_version": "1.0.0",
                    },
                }),
                retain=True,
                hostname=mqtt_host,
                port=mqtt_port,
                auth=mqtt_auth,
            )

            publish.single(
                f"{prefix}/addon/state",
                payload=json.dumps({
                    "version": "1.0.0",
                }),
                retain=True,
                hostname=mqtt_host,
                port=mqtt_port,
                auth=mqtt_auth,
            )

            for meter in meters:
                mac_cleaned = clean_mac_for_topic(meter['mac'])
                device_id = f"{prefix}_{mac_cleaned}"

                # Meter configs
                publish.single(
                    f"homeassistant/sensor/{device_id}/water/config",
                    payload=json.dumps({
                        "unique_id": f"{device_id}_water",
                        "device_class": "water",
                        "state_topic": f"{prefix}/{mac_cleaned}/state",
                        "state_class": "total_increasing",
                        "unit_of_measurement": "m³",
                        "value_template": "{{ value_json.value | float }}",
                        "json_attributes_topic": f"{prefix}/{mac_cleaned}/state",
                        "device": {
                            "identifiers": [device_id],
                            "name": f"Water Meter {meter['mac']}",
                            "serial_number": meter['mac'],
                            "via_device": "tg_iotans_addon"
                        },
                        "availability_topic": f"{prefix}/{mac_cleaned}/availability"
                    }),
                    hostname=mqtt_host,
                    port=mqtt_port,
                    auth=mqtt_auth,
                )
                publish.single(
                    f"homeassistant/sensor/{device_id}/status/config",
                    payload=json.dumps({
                        "name": "Status",
                        "unique_id": f"{device_id}_status",
                        "state_topic": f"{prefix}/{mac_cleaned}/state",
                        "value_template": "{{ value_json.status }}",
                        "icon": "mdi:information-outline",
                        "device": {
                            "identifiers": [device_id],
                        },
                        "availability_topic": f"{prefix}/{mac_cleaned}/availability"
                    }),
                    hostname=mqtt_host,
                    port=mqtt_port,
                    auth=mqtt_auth,
                )
                publish.single(
                    f"homeassistant/sensor/{device_id}/last_update/config",
                    payload=json.dumps({
                        "name": "Last Update",
                        "unique_id": f"{device_id}_last_update",
                        "device_class": "timestamp",
                        "state_topic": f"{prefix}/{mac_cleaned}/state",
                        "value_template": "{{ value_json.last_update }}",
                        "device": {
                            "identifiers": [device_id],
                        },
                        "availability_topic": f"{prefix}/{mac_cleaned}/availability"
                    }),
                    hostname=mqtt_host,
                    port=mqtt_port,
                    auth=mqtt_auth,
                )

                # Publish availability
                publish.single(
                    f"{prefix}/{mac_cleaned}/availability",
                    payload="online",
                    hostname=mqtt_host,
                    port=mqtt_port,
                    auth=mqtt_auth
                )

                # Publish state
                publish.single(
                    f"{prefix}/{mac_cleaned}/state",
                    payload=json.dumps({
                        "value": meter['value'],
                        "type": meter['type'],
                        "status": meter['status'],
                        "location": meter['location'],
                        "last_update": meter['datetime'].isoformat(),
                    }),
                    hostname=mqtt_host,
                    port=mqtt_port,
                    auth=mqtt_auth
                )

                _LOGGER.debug(f"Published water meter data for {meter['mac']}: {meter['value']} m³")

            await asyncio.sleep(args.interval * 60)

        except Exception as e:
            _LOGGER.error(f"Error in main loop: {e}")
            import traceback
            traceback.print_exc()
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())

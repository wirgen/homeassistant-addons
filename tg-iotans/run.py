#!/usr/bin/env python3
"""TG IoT Sensors addon for Home Assistant."""
import argparse
import asyncio
import logging
# import os
# import sys
# from types import SimpleNamespace
#
# import paho.mqtt.publish as publish

_LOGGER = logging.getLogger(__name__)


def clean_mac_for_topic(mac: str):
    """Clean MAC address to be used as MQTT topic."""
    return ''.join(c if c.isalnum() else '_' for c in mac.lower())


async def main():
    """Main entrypoint for the addon."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-id",
        type=str,
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
        type=int,
        help="MQTT Username",
    )
    parser.add_argument(
        "--mqtt-password",
        type=int,
        help="MQTT Password",
    )
    #
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO, format=args.log_format
    )

    _LOGGER.debug(args)

    # while True:
    #     try:
    #         from tg_iotans import main as tg_main_async
    #
    #         args = SimpleNamespace(
    #             api_id=api_id,
    #             api_hash=api_hash,
    #             session=session
    #         )
    #
    #         meters = await tg_main_async(args, debug=debug)
    #
    #         for meter in meters:
    #             mac_cleaned = clean_mac_for_topic(meter['mac'])
    #
    #             device_id = f"tg_iotans_{mac_cleaned}"
    #             device_name = f"TG Water Meter {meter['mac']}"
    #             sensor_name = None
    #
    #             if meter['type'] == 'hot':
    #                 sensor_name = f"{device_name} (Hot)"
    #
    #             if meter['type'] == 'cold':
    #                 sensor_name = f"{device_name} (Cold)"
    #
    #             if sensor_name is None:
    #                 continue
    #
    #             state_topic = f"homeassistant/sensor/{device_id}_water_meter/state"
    #             config_topic = f"homeassistant/sensor/{device_id}_water_meter/config"
    #
    #             sensor_config = {
    #                 "name": sensor_name,
    #                 "state_topic": state_topic,
    #                 "unit_of_measurement": "m³",
    #                 "value_template": "{{ value_json.value }}",
    #                 "device": {
    #                     "identifiers": [device_id],
    #                     "manufacturer": "TG Iotans Sensors",
    #                     "name": device_name,
    #                     "model": "Water Meter"
    #                 },
    #                 "availability_topic": f"homeassistant/sensor/{device_id}_water_meter/availability",
    #                 "payload_available": "online",
    #                 "payload_not_available": "offline"
    #             }
    #
    #             publish.single(
    #                 config_topic,
    #                 payload=json.dumps(sensor_config),
    #                 hostname=mqtt_host,
    #                 port=mqtt_port,
    #                 auth=mqtt_auth
    #             )
    #
    #             publish.single(
    #                 f"homeassistant/sensor/{device_id}_water_meter/availability",
    #                 payload="online",
    #                 hostname=mqtt_host,
    #                 port=mqtt_port,
    #                 auth=mqtt_auth
    #             )
    #
    #             state_payload = {
    #                 "value": round(float(meter['value']), 3),
    #                 "status": meter['status'],
    #                 "location": meter['location'],
    #                 "datetime": meter['datetime'].isoformat() if hasattr(meter['datetime'], 'isoformat') else str(meter['datetime'])
    #             }
    #
    #             publish.single(
    #                 state_topic,
    #                 payload=json.dumps(state_payload),
    #                 hostname=mqtt_host,
    #                 port=mqtt_port,
    #                 auth=mqtt_auth
    #             )
    #
    #             _LOGGER.info(f"Published water meter data for {meter['mac']}: {meter['value']} m³")
    #
    #         await asyncio.sleep(interval * 60)
    #
    #     except Exception as e:
    #         _LOGGER.error(f"Error in main loop: {e}")
    #         import traceback
    #         traceback.print_exc()
    #         await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
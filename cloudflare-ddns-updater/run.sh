#!/usr/bin/with-contenv bashio

# Export CONFIG environment variable for Python
DDCLIENT_CONFIG=$(bashio::config 'config')
export CONFIG="$DDCLIENT_CONFIG"

# Start Python script
python3 /ddns_updater.py

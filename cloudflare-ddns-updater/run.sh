#!/usr/bin/with-contenv bashio

# Export CONFIG environment variables for Python
export ZONE="$(bashio::config 'zone')"
export TOKEN="$(bashio::config 'token')"
export CHECK_INTERVAL="$(bashio::config 'check_interval')"
export DOMAINS="$(bashio::config 'domains')"

# Start Python script
python3 /ddns_updater.py

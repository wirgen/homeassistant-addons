#!/usr/bin/with-contenv bashio
# vim: ft=bash
# shellcheck shell=bash
# ==============================================================================
# Cloudflare IPv6 DDNS Updater
# ==============================================================================

flags=()
if bashio::config.true 'debug'; then
    flags+=('--debug')
fi

# Write config to JSON file for Python to read
bashio::options --json > /tmp/config.json

# Start Python script
exec python3 /ddns_updater.py --config /tmp/config.json ${flags[@]}

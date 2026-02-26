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

# Start Python script
exec python3 /ddns_updater.py --config /data/options.json ${flags[@]}

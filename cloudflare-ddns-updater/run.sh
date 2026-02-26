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
cat > /tmp/config.json <<EOF
{
  "zone": "$(bashio::config 'zone')",
  "token": "$(bashio::config 'token')",
  "check_interval": $(bashio::config 'check_interval'),
  "debug": $(bashio::config 'debug'),
  "domains": $(bashio::config 'domains' --json)
}
EOF

# Start Python script
exec python3 /ddns_updater.py --config /tmp/config.json ${flags[@]}

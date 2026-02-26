#!/usr/bin/env python3
"""Cloudflare IPv6 DDNS Updater with EUI-64 support."""

import ipaddress
import json
import logging
import os
import signal
import sys
import time
from typing import Dict, List, Optional, Tuple, Any

import requests

# Global flag for graceful shutdown
shutdown_requested = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def signal_handler(signum, frame) -> None:
    """Handle shutdown signals gracefully."""
    global shutdown_requested
    shutdown_requested = True
    logger.info(f"Received signal {signum}, shutting down gracefully...")


def load_config() -> Optional[Dict[str, Any]]:
    """Load configuration from environment variables.

    Returns:
        Optional[Dict[str, Any]]: Parsed configuration dict or None if invalid.
    """
    logger.debug("Loading configuration from environment variables...")

    zone = os.getenv('ZONE')
    token = os.getenv('TOKEN')
    check_interval_str = os.getenv('CHECK_INTERVAL', '10')
    domains_str = os.getenv('DOMAINS', '[]')

    logger.debug(f"ZONE env variable set: {zone is not None}")
    logger.debug(f"TOKEN env variable set: {token is not None}")
    logger.debug(f"CHECK_INTERVAL: {check_interval_str}")
    logger.debug(f"DOMAINS raw: {domains_str[:100] if len(domains_str) > 100 else domains_str}")

    try:
        check_interval = int(check_interval_str)
        domains = json.loads(domains_str)
        logger.debug(f"Parsed check_interval: {check_interval}")
        logger.debug(f"Parsed domains: {len(domains)} domain(s)")
        if logger.isEnabledFor(logging.DEBUG):
            for i, domain in enumerate(domains):
                logger.debug(f"  Domain {i}: {domain}")
    except ValueError as e:
        logger.error(f"Failed to parse check_interval: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse domains JSON: {e}")
        logger.error(f"Raw domains value: {domains_str}")
        return None

    config = {
        'zone': zone,
        'token': token,
        'check_interval': check_interval,
        'domains': domains,
    }
    logger.info(f"Loaded config: zone='{zone}', check_interval={check_interval}, domains={len(domains)}")
    return config


def validate_config(config: Optional[Dict[str, Any]]) -> bool:
    """Validate configuration structure.

    Args:
        config: Configuration dict to validate.

    Returns:
        bool: True if config is valid, False otherwise.
    """
    if not isinstance(config, dict):
        logger.error("Config must be a dict")
        return False

    if 'zone' not in config or not config['zone']:
        logger.error("Config missing 'zone' field")
        return False

    if 'token' not in config or not config['token']:
        logger.error("Config missing 'token' field")
        return False

    domains = config.get('domains', [])
    if not isinstance(domains, list):
        logger.error("'domains' must be a list")
        return False

    for j, domain in enumerate(domains):
        if not isinstance(domain, dict):
            logger.error(f"Domain at index {j} must be a dict")
            return False

        if 'name' not in domain or not domain['name']:
            logger.error(f"Domain at index {j} missing 'name' field")
            return False

        if 'mac' not in domain or not domain['mac']:
            logger.error(f"Domain {domain.get('name', j)} missing 'mac' field")
            return False

    return True


def mac_to_eui64(mac: str) -> str:
    """Convert MAC address to EUI-64 format.

    Args:
        mac: MAC address string (with or without separators).

    Returns:
        str: EUI-64 formatted string.

    Raises:
        ValueError: If MAC address is invalid.
    """
    # Remove any separators and validate length
    mac_clean = mac.replace(':', '').replace('-', '').lower()
    if len(mac_clean) != 12:
        raise ValueError(f"Invalid MAC address: {mac}")

    # Split into first and second half (6 bytes each)
    first_half = mac_clean[:6]
    second_half = mac_clean[6:]

    # Invert the 7th bit of the first byte
    first_byte = int(first_half[0:2], 16)
    first_byte = first_byte ^ 0x02
    first_half = f"{first_byte:02x}{first_half[2:6]}"

    # Insert FFFE in the middle
    eui64 = f"{first_half}fffe{second_half}"
    return eui64


def extract_ipv6_prefix(ipv6: str, prefix_len: int = 64) -> Optional[str]:
    """Extract IPv6 prefix from full address using ipaddress module.

    Args:
        ipv6: IPv6 address string.
        prefix_len: Prefix length to extract (default: 64).

    Returns:
        Optional[str]: IPv6 prefix string or None if extraction fails.
    """
    try:
        # Remove brackets if present
        ipv6 = ipv6.strip('[]')

        # Parse and extract prefix using ipaddress module
        net = ipaddress.ip_network(f"{ipv6}/{prefix_len}", strict=False)
        return str(network_to_prefix(str(net), prefix_len)).lower()
    except ValueError as e:
        logger.error(f"Failed to extract prefix from {ipv6}: {e}")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Traceback:", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Unexpected error extracting prefix from {ipv6}: {e}")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Traceback:", exc_info=True)
        return None


def network_to_prefix(network: str, prefix_len: int = 64) -> str:
    """Convert ipaddress network to prefix string format.

    Args:
        network: Network string (e.g., '2001:db8::/64').
        prefix_len: Prefix length to use.

    Returns:
        str: Prefix in hextet format (e.g., '2001:db8:0:0').
    """
    # Remove the /prefix part
    addr = network.split('/')[0]

    # Convert to IPv6Address object
    ipv6_obj = ipaddress.IPv6Address(addr)

    # Get the network address (prefix only)
    network_int = int(ipv6_obj) & ((1 << 128) - (1 << (128 - prefix_len)))
    prefix_obj = ipaddress.IPv6Address(network_int)

    # Return prefix as compressed string
    return str(prefix_obj)


def get_ipv6_address(api_urls: Optional[List[str]] = None) -> Optional[str]:
    """Get current public IPv6 address with fallback APIs.

    Args:
        api_urls: List of API URLs to try (default: ipify, ident.me).

    Returns:
        Optional[str]: IPv6 address string or None if all APIs fail.
    """
    if api_urls is None:
        api_urls = [
            "https://api64.ipify.org",
            "https://v6.ident.me/",
            "https://ifconfig.me/ip"
        ]

    for api_url in api_urls:
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            ipv6 = response.text.strip()
            # Validate it's a valid IPv6 address
            ipaddress.IPv6Address(ipv6)
            return ipv6
        except (requests.RequestException, ValueError) as e:
            logger.warning(f"Failed to get IPv6 from {api_url}: {e}")
            continue

    logger.error("Failed to get IPv6 address from all APIs")
    return None


def get_zone_id(zone: str, token: str) -> Optional[str]:
    """Get Cloudflare zone ID from zone name.

    Args:
        zone: Zone name (e.g., 'example.com').
        token: Cloudflare API token.

    Returns:
        Optional[str]: Zone ID or None if not found.
    """
    url = "https://api.cloudflare.com/client/v4/zones"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {"name": zone}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('success'):
            logger.error(f"Cloudflare API error for zone {zone}: {data.get('errors')}")
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"Traceback:", exc_info=True)
            return None

        zones = data.get('result', [])
        if not zones:
            logger.error(f"Zone not found: {zone}")
            return None

        return zones[0]['id']
    except requests.RequestException as e:
        logger.error(f"Failed to get zone ID for {zone}: {e}")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Traceback:", exc_info=True)
        return None


def get_dns_record(zone_id: str, name: str, token: str) -> Optional[Tuple[str, str]]:
    """Get DNS record ID and current value for a domain.

    Args:
        zone_id: Cloudflare zone ID.
        name: Full domain name (e.g., 'www.example.com').
        token: Cloudflare API token.

    Returns:
        Optional[Tuple[str, str]]: Tuple of (record_id, current_value) or None if not found.
    """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {"name": name, "type": "AAAA"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('success'):
            logger.error(f"Cloudflare API error for DNS record {name}: {data.get('errors')}")
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"Traceback:", exc_info=True)
            return None

        records = data.get('result', [])
        if not records:
            logger.warning(f"DNS record not found: {name}")
            return None

        record_id = records[0]['id']
        current_value = records[0].get('content', '')
        return record_id, current_value
    except requests.RequestException as e:
        logger.error(f"Failed to get DNS record ID for {name}: {e}")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Traceback:", exc_info=True)
        return None


def update_dns_record(zone_id: str, record_id: str, name: str,
                      ipv6: str, token: str) -> bool:
    """Update DNS record with new IPv6 address.

    Args:
        zone_id: Cloudflare zone ID.
        record_id: DNS record ID.
        name: Full domain name.
        ipv6: New IPv6 address to set.
        token: Cloudflare API token.

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "AAAA",
        "name": name,
        "content": ipv6,
        "ttl": 1  # Automatic TTL
    }

    try:
        response = requests.put(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('success'):
            logger.error(f"Cloudflare API error updating {name}: {data.get('errors')}")
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"Traceback:", exc_info=True)
            return False

        logger.info(f"Updated {name} -> {ipv6}")
        return True
    except requests.RequestException as e:
        logger.error(f"Failed to update DNS record {name}: {e}")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Traceback:", exc_info=True)
        return False


def update_zone(zone: str, token: str, domains: List[Dict],
                ipv6_prefix: str, zone_cache: Dict[str, Optional[str]]) -> None:
    """Update all domains for a zone.

    Args:
        zone: Zone name.
        token: Cloudflare API token.
        domains: List of domain configuration dicts.
        ipv6_prefix: IPv6 prefix to use.
        zone_cache: Cache of zone name -> zone ID mappings.
    """
    # Get zone ID (cached if available)
    if zone not in zone_cache:
        zone_id = get_zone_id(zone, token)
        if not zone_id:
            return
        zone_cache[zone] = zone_id
    else:
        zone_id = zone_cache[zone]
        if zone_id is None:
            return

    for domain_config in domains:
        name = domain_config.get('name')
        mac = domain_config.get('mac')

        if not name or not mac:
            logger.warning(f"Zone {zone}: Skipping invalid domain config: {domain_config}")
            continue

        try:
            # Generate EUI-64 from MAC
            eui64_suffix = mac_to_eui64(mac)
            full_ipv6 = f"{ipv6_prefix}:{eui64_suffix}"

            # Get record ID and current value
            record_info = get_dns_record(zone_id, name, token)
            if not record_info:
                continue

            record_id, current_value = record_info

            # Check if update is needed
            if current_value == full_ipv6:
                logger.info(f"Zone {zone}: {name} already has correct IP {full_ipv6}, skipping update")
                continue

            logger.info(f"Zone {zone}: Updating {name} from {current_value} to {full_ipv6}")
            update_dns_record(zone_id, record_id, name, full_ipv6, token)

        except ValueError as e:
            logger.error(f"Zone {zone}: Error processing {name}: {e}")
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"Traceback:", exc_info=True)
        except Exception as e:
            logger.error(f"Zone {zone}: Unexpected error for {name}: {e}")
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"Traceback:", exc_info=True)


def main() -> None:
    """Main entry point.

    Sets up signal handlers, validates config, and runs the update loop.
    """
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Apply debug mode before loading config
    debug_enabled = os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes')
    if debug_enabled:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
        logger.debug(f"Environment variables: ZONE={bool(os.getenv('ZONE'))}, TOKEN={bool(os.getenv('TOKEN'))}")

    config = load_config()

    if not config:
        logger.warning("No configuration provided, exiting")
        return

    # Validate configuration
    if not validate_config(config):
        logger.error("Configuration validation failed, exiting")
        sys.exit(1)

    # Track current prefix and zone cache
    current_prefix: Optional[str] = None
    zone_cache: Dict[str, Optional[str]] = {}

    # Get check interval from config, default to 10 seconds
    check_interval = config.get('check_interval', 10)

    zone = config.get('zone')
    token = config.get('token')
    domains = config.get('domains', [])

    logger.info(f"Starting Cloudflare IPv6 DDNS Updater for zone: {zone}")
    logger.info(f"Monitoring {len(domains)} domain(s)")
    logger.debug(f"Debug mode: {debug_enabled}")
    logger.debug(f"Check interval: {check_interval} seconds")

    # Force first update on startup
    logger.info("Performing initial update on startup...")
    first_run = True

    while not shutdown_requested:
        # Get current IPv6 address
        ipv6 = get_ipv6_address()
        if not ipv6:
            logger.warning("Failed to get IPv6 address, retrying in 30s")
            time.sleep(30)
            continue

        logger.debug(f"Retrieved IPv6 address: {ipv6}")

        # Extract prefix
        new_prefix = extract_ipv6_prefix(ipv6)
        if not new_prefix:
            logger.warning("Failed to extract IPv6 prefix, retrying in 30s")
            time.sleep(30)
            continue

        logger.debug(f"Extracted IPv6 prefix: {new_prefix}")

        # Check if prefix changed or first run
        if new_prefix != current_prefix or first_run:
            if first_run:
                logger.info("First run - forcing DNS update")
                current_prefix = new_prefix
            else:
                logger.info(f"IPv6 prefix changed from {current_prefix} to {new_prefix}")
                current_prefix = new_prefix

            # Update configured zone
            if not zone or not token:
                logger.warning(f"Skipping invalid zone config")
                continue

            logger.debug(f"Calling update_zone with prefix: {new_prefix}")
            update_zone(zone, token, domains, new_prefix, zone_cache)
            first_run = False

        logger.debug(f"Next check in {check_interval} seconds")

        # Sleep in small increments to check for shutdown signal
        sleep_end = time.time() + check_interval
        while time.time() < sleep_end and not shutdown_requested:
            time.sleep(1)

    logger.info("Cloudflare IPv6 DDNS Updater stopped")


if __name__ == "__main__":
    main()

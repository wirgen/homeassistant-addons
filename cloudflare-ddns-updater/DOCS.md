# Home Assistant Add-on: Cloudflare IPv6 DDNS

This Home Assistant add-on updates Cloudflare DNS AAAA records with IPv6 addresses generated using EUI-64 format from
MAC addresses. When your IPv6 prefix changes (e.g., due to ISP reassignment), all configured domains are automatically
updated with the new addresses. This is useful for maintaining reliable access to devices on networks with dynamic IPv6
prefixes.

## Features

- Automatically detects IPv6 prefix changes and updates all configured domains
- Generates IPv6 addresses using standard EUI-64 format from MAC addresses
- Supports multiple Cloudflare zones/domains in a single configuration
- Configurable check interval (10-86400 seconds)
- Includes zone ID caching to reduce API calls
- Graceful shutdown handling with signal support

## Requirements

Before running the add-on, you must have:

- A Cloudflare account with API access
- A domain name setup to use Cloudflare as the DNS provider
- IPv6 connectivity with SLAAC/EUI-64 addressing
- Existing AAAA DNS records in Cloudflare for each domain you want to update

## Installation

Follow these steps to get the add-on installed on your system:

1. Navigate in your Home Assistant frontend to **Settings** -> **Add-ons** -> **Add-on store**.
2. Find the "Cloudflare IPv6 DDNS" add-on and click it.
3. Click on the "INSTALL" button.

## Configuration

### Option: `config`

The `config` option is a list of zone configurations. Each zone configuration contains the settings for a specific
Cloudflare zone/domain.

```yaml
config:
  - zone: example.com
    token: <your-cloudflare-api-token>
    check_interval: 60
    domains:
      - name: host1.example.com
        mac: "aa:bb:cc:dd:ee:ff"
      - name: host2.example.com
        mac: "11:22:33:44:55:66"
  - zone: another-domain.com
    token: <another-cloudflare-api-token>
    check_interval: 120
    domains:
      - name: www.another-domain.com
        mac: "aa:aa:aa:aa:aa:aa"
```

### Option: `zone`

Cloudflare zone/domain name (e.g., `example.com`).

### Option: `token`

Cloudflare API token with permissions to edit DNS records.

The token is an Account API token from Cloudflare. Create it under:
**Manage Account** -> **Account API Tokens** -> **Create Token**

It must have the following permissions:

- Zone - DNS - Edit
- Zone - Zone - Read
- The Zone resources must be "Include - All" (or your specific account)

### Option: `check_interval`

IPv6 check interval in seconds.

By default, 60 seconds. Minimum: 10, Maximum: 86400 (24 hours).

### Option: `domains`

List of domains to update within the zone. Each domain entry contains:

- `name`: Full domain/subdomain to update (e.g., `host1.example.com`)
- `mac`: MAC address used for EUI-64 IPv6 generation (e.g., `aa:bb:cc:dd:ee:ff`)

Note: The AAAA DNS records must already exist in Cloudflare. This add-on only updates existing records; it does not
create new ones.

## How it works

1. The add-on periodically checks the public IPv6 address of the host using external APIs
2. It extracts the /64 prefix from the address
3. If the prefix has changed from the previous check:
    - For each configured domain in each zone:
        - Generates full IPv6 using EUI-64: prefix + modified(MAC)
        - Updates the AAAA DNS record via Cloudflare API
4. The process repeats with the configured interval

## EUI-64 Format

The IPv6 addresses are generated using standard EUI-64 format defined in RFC 4291:

1. MAC address is split into two 6-byte halves
2. FFFE is inserted between the halves
3. The 7th bit (U/L bit) of the first byte is inverted

Example:

- MAC: `aa:bb:cc:dd:ee:ff`
- EUI-64 suffix: `a8bb:ccff:fedd:eeff`
- Full address: `2001:db8:a8bb:ccff:fedd:eeff`

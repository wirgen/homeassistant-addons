# Home Assistant Add-on: Cloudflare IPv6 DDNS

This Home Assistant add-on updates Cloudflare DNS AAAA records with IPv6 addresses generated using EUI-64 format from
MAC addresses. When your IPv6 prefix changes (e.g., due to ISP reassignment), all configured domains are automatically
updated with the new addresses. This is useful for maintaining reliable access to devices on networks with dynamic IPv6
prefixes.

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[Source](https://github.com/wirgen/tg-iotans)

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
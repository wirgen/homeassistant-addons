# Home Assistant add-on repository

Use button

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fwirgen%2Fhomeassistant-addons)

or go to the Add-on Store and manually add a new repository `https://github.com/wirgen/homeassistant-addons`
using the "Repositories" option in the top-right corner.

## Add-ons

This repository contains the following add-ons

### [Cloudflare IPv6 DDNS](./cloudflare-ddns-updater)

![Supports aarch64 Architecture][aarch64-yes-shield]
![Supports amd64 Architecture][amd64-yes-shield]
![Supports armhf Architecture][armhf-no-shield]
![Supports armv7 Architecture][armv7-no-shield]
![Supports i386 Architecture][i386-no-shield]

_This Home Assistant add-on updates Cloudflare DNS AAAA records with IPv6 addresses generated using EUI-64 format from
MAC addresses. When your IPv6 prefix changes (e.g., due to ISP reassignment), all configured domains are automatically
updated with the new addresses. This is useful for maintaining reliable access to devices on networks with dynamic IPv6
prefixes._

### [TG Iotans](./tg-iotans)

![Supports aarch64 Architecture][aarch64-yes-shield]
![Supports amd64 Architecture][amd64-yes-shield]
![Supports armhf Architecture][armhf-no-shield]
![Supports armv7 Architecture][armv7-no-shield]
![Supports i386 Architecture][i386-no-shield]

_This Home Assistant add-on runs a lightweight Telegram client that automatically retrieves available water meter
readings from the [MyIotansBot](https://t.me/MyIotansBot).
It is designed to integrate these readings into your Home Assistant environment for further automation, monitoring, and
analytics._

### [Wyoming Piper Normalize](./wyoming-piper-normalize)

![Supports aarch64 Architecture][aarch64-yes-shield]
![Supports amd64 Architecture][amd64-yes-shield]
![Supports armhf Architecture][armhf-no-shield]
![Supports armv7 Architecture][armv7-no-shield]
![Supports i386 Architecture][i386-no-shield]

_[Wyoming protocol](https://github.com/rhasspy/wyoming) server for the [Piper](https://github.com/rhasspy/piper/)
text-to-speech system, featuring Russian text normalization via [RUNorm](https://github.com/Den4ikAI/runorm)._

<!--

Notes to developers after forking or using the github template feature:
- While developing comment out the 'image' key from 'example/config.yaml' to make the supervisor build the addon
  - Remember to put this back when pushing up your changes.
- When you merge to the 'main' branch of your repository a new build will be triggered.
  - Make sure you adjust the 'version' key in 'example/config.yaml' when you do that.
  - Make sure you update 'example/CHANGELOG.md' when you do that.
  - The first time this runs you might need to adjust the image configuration on github container registry to make it public
  - You may also need to adjust the github Actions configuration (Settings > Actions > General > Workflow > Read & Write)
- Adjust the 'image' key in 'example/config.yaml' so it points to your username instead of 'home-assistant'.
  - This is where the build images will be published to.
- Rename the example directory.
  - The 'slug' key in 'example/config.yaml' should match the directory name.
- Adjust all keys/url's that points to 'home-assistant' to now point to your user/fork.
- Share your repository on the forums https://community.home-assistant.io/c/projects/9
- Do awesome stuff!
 -->

[aarch64-yes-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-yes-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-yes-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-yes-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-yes-shield]: https://img.shields.io/badge/i386-yes-green.svg
[aarch64-no-shield]: https://img.shields.io/badge/aarch64-no-red.svg
[amd64-no-shield]: https://img.shields.io/badge/amd64-no-red.svg
[armhf-no-shield]: https://img.shields.io/badge/armhf-no-red.svg
[armv7-no-shield]: https://img.shields.io/badge/armv7-no-red.svg
[i386-no-shield]: https://img.shields.io/badge/i386-no-red.svg

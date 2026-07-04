# Syncleo (Rusclimate/Polaris) WiFi (UDP) Integration for Home Assistant
[![GitHub Release][releases-shield]][releases]
[![Downloads][download-latest-shield]](Downloads)
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

Integration to control devices using Syncleo IoT (Rusclimate/Polaris) UDP protocol.  
Integration **doesn't** use MQTT

## Supported models (by device type)
- (8) Electrolux Fusion EVO DC, Electrolux Atrium DC, Electrolux Arctic Air DC, Zanussi Siena DC, Ballu Lagoon DC, Royal Thermo Siena DC, Climber Dresden, Climer Dresden Cki 24, ONE AIR MASTER
- (46) Electrolux Air Gate, Electrolux Rapid, Ballu Apollo, Ballu Evolution, Electrolux Brilliant Marble, Electrolux ECH/AG, Electrolux ECH/AG2, Electrolux ECH/AT, Electrolux ECH/BM

## Installation

### Install from HACS
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DeKaN&repository=ha-syncleo&category=Integration)

Or
1. Have [HACS][hacs] installed, this will allow you to easily manage and track updates.
1. Search for "Syncleo".
1. Click Install below the found integration.

Then add device via these steps:
1. Wait for autodiscovery.
1. Paste "Share URL" from mobile app at adding device.
1. Fix Vendor/Model if needed.

<!---->
[hacs]: https://github.com/hacs/integration
[releases-shield]: https://img.shields.io/github/v/release/DeKaN/ha-syncleo?style=for-the-badge
[releases]: https://github.com/DeKaN/ha-syncleo/releases
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/DeKaN/ha-syncleo.svg?style=for-the-badge
[download-latest-shield]: https://img.shields.io/github/downloads/DeKaN/ha-syncleo/latest/total?style=for-the-badge

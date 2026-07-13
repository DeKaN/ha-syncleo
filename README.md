# Syncleo (Rusclimate/Polaris) WiFi (UDP) Integration for Home Assistant
[![GitHub Release][releases-shield]][releases]
[![Downloads][download-latest-shield]](Downloads)
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

Integration to control devices using Syncleo IoT (Rusclimate/Polaris) UDP protocol.  
Integration **doesn't** use MQTT, but your device should be visible in mDNS.

## FAQ
Q: How to get "Share URL"?  
A: Open device settings in mobile app, go to "Access control" screen and press "Share" button. You can see QR code on new screen, press "Share" button to get "Share URL" as text.

Q: How to find device type for my device?  
A: Look at your "Share URL", it has a specific format: `rusklimat://device-share/rusclimate/<DEVICE_TYPE>/<MAC_ADDRESS>>?token=<TOKEN>&name=<DEVICE_NAME>&deviceLocation=<LOCATION_NAME>&<DEVICE_ATTRIBUTES>`.


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

## Supported models (by device type)
| Vendor | Device Type | Supported Models |
| :--- | :--- | :--- |
| Rusclimate | 2 | Electrolux SI (SE/BE) EEC, Electrolux Smartinverter, Electrolux Smartinverter PRO, Electrolux Smartinverter PRO 2.0, Electrolux Smartinverter Enamel |
| Rusclimate | 6 | (Transformer DI 3.0) Electrolux Air Gate, Electrolux Rapid, Ballu Apollo, Ballu Evolution, Electrolux Brilliant Marble |
| Rusclimate | 7 | Zanussi Azurro PRO WiFi, Zanussi Artendo WiFi |
| Rusclimate | 8 | Electrolux Fusion EVO DC, Electrolux Atrium DC, Electrolux Arctic Air DC, Zanussi Siena DC, Ballu Lagoon DC, Royal Thermo Siena DC, Climber Dresden, Climer Dresden Cki 24, ONE AIR MASTER |
| Rusclimate | 9 | (Transformer DI 3.0 S) Electrolux Air Gate, Electrolux Rapid, Ballu Apollo, Ballu Evolution, Electrolux Brilliant Marble |
| Rusclimate | 11 | Ballu Rapid |
| Rusclimate | 12 | Electrolux Centurio IQ 2.0, Electrolux Maximus WiFi |
| Rusclimate | 14 | (Transformer DI) Electrolux Air Gate, Electrolux Rapid, Ballu Evolution, Electrolux Air Plinth PRO |
| Rusclimate | 16 | Ballu Smart WiFi |
| Rusclimate | 17 | Wi-Fi Convection Heater |
| Rusclimate | 18 | Electrolux Maximus, Zanussi Artendo PRO-C WiFi, Electrolux Megapolis WiFi, Zanussi Splendore XP 2.0 |
| Rusclimate | 19 | Electrolux Regency |
| Rusclimate | 28 | (Transformer DI 4.0) Electrolux Air Gate, Electrolux Rapid, Ballu Apollo, Ballu Evolution, Electrolux Brilliant Marble, Electrolux ECH/AG, Electrolux ECH/AG2, Electrolux ECH/AT, Electrolux ECH/BM |
| Rusclimate | 31 | (Transformer 4.0) Electrolux Air Gate, Electrolux Rapid, Ballu Apollo, Ballu Evolution, Electrolux Brilliant Marble, Electrolux ECH/AG2, Electrolux ECH/AT, Electrolux EIH/R, Electrolux EIH/S, Ballu Plaza |
| Rusclimate | 33 | Electrolux Centurio IQ 3.0 |
| Rusclimate | 42 | (Transformer DI 3.0 XS) Electrolux Air Gate, Electrolux Rapid, Ballu Apollo, Ballu Evolution, Electrolux Brilliant Marble |
| Rusclimate | 44 | Royal Thermo Aqua Inverter, Royal Thermo Aqua Inox Inverter |
| Rusclimate | 46 | (Transformer DI 4.0) Electrolux Air Gate, Electrolux Rapid, Ballu Apollo, Ballu Evolution, Electrolux Brilliant Marble, Electrolux ECH/AG, Electrolux ECH/AG2, Electrolux ECH/AT, Electrolux ECH/BM |
| Rusclimate | 47 | Wi-Fi Convection Heater |
| Rusclimate | 49 | (Transformer 4.0) Electrolux Air Gate, Electrolux Rapid, Ballu Apollo, Ballu Evolution, Electrolux Brilliant Marble, Electrolux ECH/AG2, Electrolux ECH/AT, Electrolux EIH/R, Electrolux EIH/S, Ballu Plaza |
| Rusclimate | 68 | Ballu iGreen Pro, Electrolux Loft DC, Zanussi Moderno DC, Electrolux Slide DC, Electrolux Arctic Air Wi-Fi, Shuft Asgard Black DC, Ballu Platinum Black DC, Ballu Platinum DC Inverter |
| Rusclimate | 71 | (Transformer DI 4.0) Electrolux Air Gate, Electrolux Rapid, Ballu Apollo, Ballu Evolution, Electrolux Brilliant Marble, Electrolux ECH/AG, Electrolux ECH/AG2, Electrolux ECH/AT, Electrolux ECH/BM |
| Rusclimate | 74 | Aurus S |
| Rusclimate | 76 | Ballu Artendo Inverter, Electrolux Royal Flash, Electrolux Centurio IQ Inverter |
| Rusclimate | 77 | Royal Thermo Major Inverter, Royal Thermo Smalto Inverter |
| Rusclimate | 80 | Aurus F |
| Rusclimate | 89 | Aurus PF |
| Rusclimate | 90 | Ballu Cetrion Inverter, Ballu Cetrion Inox Inverter |
| Rusclimate | 91 | Royal Thermo Regency |
| Rusclimate | 93 | Electrolux SI (SE/BE) EEC, Electrolux Smartinverter, Electrolux Smartinverter PRO, Electrolux Smartinverter PRO 2.0, Electrolux Smartinverter Enamel |
| Rusclimate | 109 | Aurus S |
| Rusclimate | 119 | Electrolux SI (SE/BE) EEC, Electrolux Smartinverter, Electrolux Smartinverter PRO, Electrolux Smartinverter PRO 2.0, Electrolux Smartinverter Enamel |

<!---->
[hacs]: https://github.com/hacs/integration
[releases-shield]: https://img.shields.io/github/v/release/DeKaN/ha-syncleo?style=for-the-badge
[releases]: https://github.com/DeKaN/ha-syncleo/releases
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/DeKaN/ha-syncleo.svg?style=for-the-badge
[download-latest-shield]: https://img.shields.io/github/downloads/DeKaN/ha-syncleo/latest/total?style=for-the-badge

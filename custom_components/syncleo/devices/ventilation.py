"""Ventilation profiles.

Planned: EPVS types 34/36 (climate), Shuft types 98/100 (fan),
ASV-60 type 124 (valve, cover pending verification), and type 27 (controls).
The fan-based VentilationProfile is part of the separate breezer refactor."""

from .profiles import DeviceBaseProfile

PROFILES: list[DeviceBaseProfile] = []

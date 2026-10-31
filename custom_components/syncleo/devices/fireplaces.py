"""Fireplace profiles. Planned: decorative type 50; climate type 112."""

from .profiles import ClimateProfile, FireplaceProfile

PROFILES: list[ClimateProfile | FireplaceProfile] = []

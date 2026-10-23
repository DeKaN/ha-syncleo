"""Workarounds for pysyncleo limitations (imports only pysyncleo and stdlib)."""

from pysyncleo.commands import CmdBacklight

_PATCH_MARKER = "_syncleo_raw_patched"


def ensure_backlight_raw_payload() -> None:
    """Make CmdBacklight keep the raw payload next to its bool value (idempotent).

    The stock deserializer keeps only ``bool(payload[0])``, which drops the
    brightness levels and colours of the 8-byte backlight register.
    """
    original = CmdBacklight.deserialize
    if getattr(original, _PATCH_MARKER, False):
        return

    def deserialize(self: CmdBacklight, payload: bytes) -> None:
        original(self, payload)
        self.raw = bytes(payload)

    setattr(deserialize, _PATCH_MARKER, True)
    CmdBacklight.deserialize = deserialize  # type: ignore[method-assign]

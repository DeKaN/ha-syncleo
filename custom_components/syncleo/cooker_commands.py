"""Raw MULTI_STEP frames for Syncleo cookers.

Reverse-engineered from a Polaris PMC-0528WIFI (devtype 48) by recording the frames the
device echoes when a program is started in the app:

    MULTI_STEP payload = flags(0) total_steps(1) step(0) program temp 0x00 time_lo time_hi 0x00 0x00

`program` is the program code, `temp` the target temperature in °C and the two time bytes a
little-endian duration in seconds. The all-zero frame stops the current program.

These classes are duck-typed (not UdpCommand subclasses) on purpose: subclassing would
register them in `UdpCommand.COMMAND_REGISTRY` and break parsing of incoming MULTI_STEP
frames, which the select entity needs for reading the running program.
"""

from __future__ import annotations

from pysyncleo.enums import UdpCommandType

PROGRAM_FRAME_PREFIX = 0x00
PROGRAM_FRAME_STEPS = 0x01


class CookerProgramCommand:
    """Start a cooking program on a Syncleo cooker."""

    command_type = UdpCommandType.MULTI_STEP

    def __init__(self, code: int, temperature: int, seconds: int) -> None:
        self.code = int(code) & 0xFF
        self.temperature = int(temperature) & 0xFF
        self.seconds = max(0, int(seconds))

    def serialize(self) -> bytes:
        return (
            bytes(
                (
                    PROGRAM_FRAME_PREFIX,
                    PROGRAM_FRAME_STEPS,
                    0x00,
                    self.code,
                    self.temperature,
                    0x00,
                )
            )
            + self.seconds.to_bytes(2, "little")
            + b"\x00\x00"
        )

    def __repr__(self) -> str:
        return (
            f"CookerProgramCommand(code=0x{self.code:02x}, "
            f"temperature={self.temperature}, seconds={self.seconds})"
        )


class CookerStopCommand:
    """Stop whatever the cooker is doing (all-zero MULTI_STEP frame)."""

    command_type = UdpCommandType.MULTI_STEP

    def serialize(self) -> bytes:
        return bytes(10)

    def __repr__(self) -> str:
        return "CookerStopCommand()"


def parse_program_frame(raw_tail: bytes) -> tuple[int, int, int] | None:
    """Decode a MULTI_STEP raw tail into (code, temperature, seconds); None when idle."""
    if len(raw_tail) < 5 or raw_tail[0] == 0:
        return None
    return raw_tail[0], raw_tail[1], int.from_bytes(raw_tail[3:5], "little")

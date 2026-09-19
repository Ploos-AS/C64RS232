#!/usr/bin/env python3
"""Qualify the frozen C64 User Port signal-label contract in the M1.9 schematic."""
from pathlib import Path
import re

SCH = Path(__file__).resolve().parents[1] / "hardware/C64RS232_M1.kicad_sch"
text = SCH.read_text()

def labels_at(x, y):
    return re.findall(
        rf'\(label "([^"]+)"\s+\(at {re.escape(x)} {re.escape(y)} 0\)',
        text,
    )

# The legacy C64_USERPORT symbol is drawn with its pin labels on x=33.02.
# B and C are intentionally both RXD in the established C64 RS-232 contract.
expected = {
    "83.82": {"GND"},
    "86.36": {"C64_RXD"},
    "88.90": {"C64_RXD"},
    "91.44": {"C64_RTS"},
    "93.98": {"C64_DTR"},
    "96.52": {"C64_RI"},
    "99.06": {"C64_DCD"},
    "104.14": {"C64_CTS"},
    "106.68": {"C64_DSR"},
    "109.22": {"C64_TXD"},
    "111.76": {"GND"},
}

for y, want in expected.items():
    got = set(labels_at("33.02", y))
    if got != want:
        raise SystemExit(
            f"M2.3 FAIL: J1 schematic coordinate 33.02,{y}: "
            f"expected {sorted(want)}, got {sorted(got)}"
        )

for name in ("C64_TXD", "C64_RXD", "C64_RTS", "C64_CTS",
             "C64_DTR", "C64_DSR", "C64_DCD", "C64_RI"):
    if text.count(f'(label "{name}"') < 1:
        raise SystemExit(f"M2.3 FAIL: missing {name}")

print("M2.3 C64 USER PORT CONTRACT PASS")
print("  verified schematic coordinates: B/C=RXD, M=TXD, D=RTS,")
print("  E=DTR, F=RI, H=DCD, K=CTS, L=DSR")
print("  GND anchors verified; J1 coordinate model matches the legacy symbol")

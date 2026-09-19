#!/usr/bin/env python3
"""Check the frozen C64 User Port RS-232 pin contract in the M1.10 schematic."""
from pathlib import Path
import re

SCH = Path(__file__).resolve().parents[1] / "hardware/C64RS232_M1.kicad_sch"
text = SCH.read_text()

def label_at(x, y):
    m = re.search(rf'\(label "([^"]+)"\s+\(at {re.escape(x)} {re.escape(y)} 0\)', text)
    return m.group(1) if m else None

expected = {
    ("33.02","109.22"): "GND", ("33.02","104.14"): "C64_RXD",
    ("33.02","101.60"): "C64_RTS", ("33.02","99.06"): "C64_DTR",
    ("33.02","96.52"): "C64_RI", ("33.02","93.98"): "C64_DCD",
    ("33.02","88.90"): "C64_CTS", ("33.02","86.36"): "C64_DSR",
    ("33.02","83.82"): "C64_TXD", ("33.02","81.28"): "GND",
    ("58.42","109.22"): "GND", ("58.42","106.68"): "+5V",
    ("58.42","104.14"): "RESET", ("58.42","101.60"): "CNT1",
    ("58.42","99.06"): "SP1", ("58.42","96.52"): "CNT2",
    ("58.42","93.98"): "SP2", ("58.42","91.44"): "PC2",
    ("58.42","88.90"): "ATN", ("58.42","81.28"): "GND",
}
for (x,y), want in expected.items():
    got = label_at(x,y)
    if got != want:
        raise SystemExit(f"M2.3 FAIL: J1 pin at {x},{y}: expected {want}, got {got}")

for x,y in (("58.42","86.36"),("58.42","83.82"),("33.02","106.68"),("33.02","91.44")):
    if not re.search(rf'\(no_connect \(at {re.escape(x)} {re.escape(y)}\)', text):
        raise SystemExit(f"M2.3 FAIL: J1 unused pin at {x},{y} is not explicitly no-connect")

for name in ("C64_TXD","C64_RXD","C64_RTS","C64_CTS","C64_DTR","C64_DSR","C64_DCD","C64_RI"):
    if text.count(f'(label "{name}"') < 1:
        raise SystemExit(f"M2.3 FAIL: missing {name}")

print("M2.3 C64 USER PORT CONTRACT PASS")
print("  C64 RS-232 signals mapped to M/C/D/K/E/L/H/F respectively")
print("  power/ground and unused User Port pins explicitly constrained")

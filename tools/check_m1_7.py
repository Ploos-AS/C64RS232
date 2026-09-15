#!/usr/bin/env python3
"""Static guard for the C64RS232 M1.7 electrical wiring contract."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "hardware" / "M1_7_WIRING_SPEC.md"
NATIVE = ROOT / "hardware" / "C64RS232_M1.kicad_sch"

required = [
    "C64_TXD", "C64_RTS", "C64_DTR", "C64_RXD", "C64_CTS",
    "C64_DSR", "C64_DCD", "C64_RI", "RS232_TXD", "RS232_RTS",
    "RS232_DTR", "RS232_RXD", "RS232_CTS", "RS232_DSR", "RS232_DCD",
    "RS232_RI", "FORCEON", "FORCEOFF", "R2OUTB", "INVALID", "9 VAC",
]

errors = []
if not SPEC.is_file():
    errors.append(f"missing wiring specification: {SPEC}")
else:
    text = SPEC.read_text(encoding="utf-8")
    for token in required:
        if token not in text:
            errors.append(f"wiring specification missing token: {token}")

if not NATIVE.is_file() or NATIVE.stat().st_size == 0:
    errors.append(f"native schematic missing or empty: {NATIVE}")
else:
    prefix = NATIVE.read_text(encoding="utf-8", errors="strict")[:256]
    if "(kicad_sch" not in prefix:
        errors.append("native schematic is not recognizable KiCad schematic text")

if errors:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    raise SystemExit(1)

print("M1.7 CONTRACT CHECK PASS")
print(f"spec: {SPEC.relative_to(ROOT)}")
print(f"native: {NATIVE.relative_to(ROOT)}")
print("NOTE: this guard validates the contract and native-file presence; M1.8 will assert exported electrical nets.")

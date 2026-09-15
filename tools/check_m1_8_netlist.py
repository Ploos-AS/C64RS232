#!/usr/bin/env python3
"""M1.8 exported-netlist assertions for C64RS232.

This deliberately checks the KiCad-exported netlist rather than merely looking
for labels in the schematic source.  It is the first M1.8 electrical gate.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
NETLIST = ROOT / "build" / "kicad" / "m1_8" / "C64RS232_M1.net"

# M1.1/M1.7 frozen functional nets. Power/charge-pump nets are handled by ERC
# classification in the next M1.8 increment because KiCad may auto-name them.
REQUIRED_NETS = {
    "C64_TXD", "C64_RTS", "C64_DTR", "C64_RXD", "C64_CTS", "C64_DSR",
    "C64_DCD", "C64_RI", "RS232_TXD", "RS232_RTS", "RS232_DTR",
    "RS232_RXD", "RS232_CTS", "RS232_DSR", "RS232_DCD", "RS232_RI",
}

errors = []
if not NETLIST.is_file() or NETLIST.stat().st_size == 0:
    errors.append(f"missing or empty exported netlist: {NETLIST}")
else:
    text = NETLIST.read_text(encoding="utf-8", errors="replace")
    # KiCad S-expression netlists contain '(name "...")'; tolerate unquoted
    # simple names as well so the checker remains useful across KiCad versions.
    names = set(re.findall(r'\(name\s+"([^"\n]+)"\)', text))
    names.update(re.findall(r'\(name\s+([A-Za-z0-9_+./:-]+)\)', text))
    missing = sorted(REQUIRED_NETS - names)
    if missing:
        errors.append("exported netlist missing frozen functional nets: " + ", ".join(missing))

if errors:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    raise SystemExit(1)

print("M1.8 NETLIST ASSERTIONS PASS")
print(f"netlist: {NETLIST.relative_to(ROOT)}")
print(f"functional nets asserted: {len(REQUIRED_NETS)}")

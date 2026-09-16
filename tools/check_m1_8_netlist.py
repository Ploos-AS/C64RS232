#!/usr/bin/env python3
"""M1.8 exported-netlist assertions for C64RS232.

Check the KiCad-exported netlist rather than merely looking for labels in the
schematic source. KiCad 9's default `sch export netlist` output is XML, while
older/alternate exporters may use S-expressions, so accept both formats.
"""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NETLIST = ROOT / "build" / "kicad" / "m1_8" / "C64RS232_M1.net"

REQUIRED_NETS = {
    "C64_TXD", "C64_RTS", "C64_DTR", "C64_RXD", "C64_CTS", "C64_DSR",
    "C64_DCD", "C64_RI", "RS232_TXD", "RS232_RTS", "RS232_DTR",
    "RS232_RXD", "RS232_CTS", "RS232_DSR", "RS232_DCD", "RS232_RI",
}

errors = []
names = set()
if not NETLIST.is_file() or NETLIST.stat().st_size == 0:
    errors.append(f"missing or empty exported netlist: {NETLIST}")
else:
    text = NETLIST.read_text(encoding="utf-8", errors="replace")
    # KiCad 9 default netlist: <net code="..." name="/C64_TXD">. Local labels
    # on the root sheet are exported with a leading '/', so normalize that
    # sheet-path prefix before comparing with the frozen logical contract.
    try:
        root = ET.fromstring(text)
        names.update(net.get("name") for net in root.findall(".//net") if net.get("name"))
    except ET.ParseError:
        pass
    # Also tolerate S-expression netlists from other KiCad exporters/versions.
    names.update(re.findall(r'\(name\s+"([^"\n]+)"\)', text))
    names.update(re.findall(r'\(name\s+([A-Za-z0-9_+./:-]+)\)', text))

    logical_names = set(names)
    logical_names.update(name[1:] for name in names if name.startswith("/") and len(name) > 1)
    missing = sorted(REQUIRED_NETS - logical_names)
    if missing:
        errors.append("exported netlist missing frozen functional nets: " + ", ".join(missing))
        if names:
            errors.append("exported net names seen: " + ", ".join(sorted(names)))

if errors:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    raise SystemExit(1)

print("M1.8 NETLIST ASSERTIONS PASS")
print(f"netlist: {NETLIST.relative_to(ROOT)}")
print(f"functional nets asserted: {len(REQUIRED_NETS)}")

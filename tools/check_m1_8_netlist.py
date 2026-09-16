#!/usr/bin/env python3
"""M1.8c exported-netlist assertions for C64RS232.

Verify both the frozen functional net names and their exact component/pin
membership in the KiCad-exported XML netlist.  S-expression netlists remain
supported for the older name-presence M1.8a check, but exact M1.8c pin
qualification requires KiCad XML because it carries node ref/pin data.
"""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NETLIST = ROOT / "build" / "kicad" / "m1_8" / "C64RS232_M1.net"

EXPECTED = {
    "C64_TXD": {("J1", "M"), ("U1", "14")},
    "C64_RTS": {("J1", "D"), ("U1", "13")},
    "C64_DTR": {("J1", "E"), ("U1", "12")},
    "C64_RXD": {("J1", "B"), ("J1", "C"), ("U1", "19")},
    "C64_CTS": {("J1", "K"), ("U1", "18")},
    "C64_DSR": {("J1", "L"), ("U1", "17")},
    "C64_DCD": {("J1", "H"), ("U1", "16")},
    "C64_RI": {("J1", "F"), ("U1", "15")},
    "RS232_TXD": {("U1", "9"), ("J2", "3")},
    "RS232_RTS": {("U1", "10"), ("J2", "7")},
    "RS232_DTR": {("U1", "11"), ("J2", "4")},
    "RS232_RXD": {("U1", "4"), ("J2", "2")},
    "RS232_CTS": {("U1", "5"), ("J2", "8")},
    "RS232_DSR": {("U1", "6"), ("J2", "6")},
    "RS232_DCD": {("U1", "7"), ("J2", "1")},
    "RS232_RI": {("U1", "8"), ("J2", "9")},
}
REQUIRED_NETS = set(EXPECTED)


def logical_name(name):
    return name[1:] if name.startswith("/") and len(name) > 1 else name


def fmt_nodes(nodes):
    return ", ".join(f"{ref}.{pin}" for ref, pin in sorted(nodes)) or "<none>"


errors = []
names = set()
xml_root = None
if not NETLIST.is_file() or NETLIST.stat().st_size == 0:
    errors.append(f"missing or empty exported netlist: {NETLIST}")
else:
    text = NETLIST.read_text(encoding="utf-8", errors="replace")
    try:
        xml_root = ET.fromstring(text)
        names.update(net.get("name") for net in xml_root.findall(".//net") if net.get("name"))
    except ET.ParseError:
        pass

    # Preserve compatibility with alternate/older exporters for M1.8a names.
    names.update(re.findall(r'\(name\s+"([^"\n]+)"\)', text))
    names.update(re.findall(r'\(name\s+([A-Za-z0-9_+./:-]+)\)', text))

    logical_names = {logical_name(name) for name in names}
    missing = sorted(REQUIRED_NETS - logical_names)
    if missing:
        errors.append("exported netlist missing frozen functional nets: " + ", ".join(missing))
        if names:
            errors.append("exported net names seen: " + ", ".join(sorted(names)))

    if xml_root is None:
        errors.append("M1.8c exact pin qualification requires a KiCad XML netlist")
    else:
        actual = {}
        for net in xml_root.findall(".//net"):
            raw_name = net.get("name")
            if not raw_name:
                continue
            name = logical_name(raw_name)
            if name not in EXPECTED:
                continue
            nodes = {(node.get("ref", ""), node.get("pin", "")) for node in net.findall("node")}
            actual.setdefault(name, set()).update(nodes)

        for name in sorted(EXPECTED):
            expected = EXPECTED[name]
            got = actual.get(name, set())
            if got != expected:
                missing_nodes = expected - got
                extra_nodes = got - expected
                detail = [f"{name} pin membership mismatch"]
                if missing_nodes:
                    detail.append("missing: " + fmt_nodes(missing_nodes))
                if extra_nodes:
                    detail.append("unexpected: " + fmt_nodes(extra_nodes))
                detail.append("actual: " + fmt_nodes(got))
                errors.append("; ".join(detail))

if errors:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    raise SystemExit(1)

print("M1.8c EXACT PIN CONNECTIVITY PASS")
print(f"netlist: {NETLIST.relative_to(ROOT)}")
print(f"functional nets asserted: {len(REQUIRED_NETS)}")
print(f"exact pin memberships asserted: {sum(len(nodes) for nodes in EXPECTED.values())}")

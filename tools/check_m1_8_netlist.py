#!/usr/bin/env python3
"""M1.8d exported-netlist assertions for C64RS232.

Verify frozen functional, power, control, and charge-pump nets and their exact
component/pin membership in KiCad-exported XML netlists.  S-expression parsing
is retained for functional compatibility, but exact M1.8d qualification is
based on the same ref/pin membership model.
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
    "RAW_5V": {("J1", "2"), ("F1", "1")},
    "+5V": {("F1", "2"), ("U1", "23"), ("U1", "26"), ("C5", "1"), ("#FLG0101", "1")},
    "GND": {("J1", "1"), ("J1", "12"), ("J1", "A"), ("J1", "N"), ("U1", "22"), ("U1", "25"), ("J2", "5"), ("C3", "2"), ("C4", "2"), ("C5", "2")},
    "C1_PLUS": {("C1", "1"), ("U1", "28")},
    "C1_MINUS": {("C1", "2"), ("U1", "24")},
    "C2_PLUS": {("C2", "1"), ("U1", "1")},
    "C2_MINUS": {("C2", "2"), ("U1", "2")},
    "VPLUS": {("C3", "1"), ("U1", "27")},
    "VMINUS": {("C4", "1"), ("U1", "3")},
}
FUNCTIONAL_NETS = {name for name in EXPECTED if name.startswith("C64_") or name.startswith("RS232_")}
POWER_NETS = set(EXPECTED) - FUNCTIONAL_NETS

# Pins intentionally left electrically unconnected by the M1 freeze.
FORBIDDEN_CONNECTED = {
    ("U1", "20"), ("U1", "21"),
    ("J1", "3"), ("J1", "4"), ("J1", "5"), ("J1", "6"), ("J1", "7"),
    ("J1", "8"), ("J1", "9"), ("J1", "10"), ("J1", "11"), ("J1", "J"),
}


def logical_name(name):
    return name[1:] if name.startswith("/") and len(name) > 1 else name


def fmt_nodes(nodes):
    return ", ".join(f"{ref}.{pin}" for ref, pin in sorted(nodes)) or "<none>"


def parse_sexpr_netlist(text):
    actual = {}
    current = None
    net_re = re.compile(r'^\s*\(net\s+\(code\s+"[^"]+"\)\s+\(name\s+"([^"]+)"\)')
    node_re = re.compile(r'^\s*\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)')
    for line in text.splitlines():
        match = net_re.match(line)
        if match:
            current = logical_name(match.group(1))
            actual.setdefault(current, set())
            continue
        match = node_re.match(line)
        if current is not None and match:
            actual[current].add((match.group(1), match.group(2)))
    return actual


errors = []
actual = {}
if not NETLIST.is_file() or NETLIST.stat().st_size == 0:
    errors.append(f"missing or empty exported netlist: {NETLIST}")
else:
    text = NETLIST.read_text(encoding="utf-8", errors="replace")
    try:
        xml_root = ET.fromstring(text)
    except ET.ParseError:
        xml_root = None

    if xml_root is not None:
        for net in xml_root.findall(".//net"):
            raw_name = net.get("name")
            if not raw_name:
                continue
            name = logical_name(raw_name)
            nodes = {(node.get("ref", ""), node.get("pin", "")) for node in net.findall("node")}
            actual.setdefault(name, set()).update(nodes)
    else:
        actual = parse_sexpr_netlist(text)

    missing = sorted(set(EXPECTED) - set(actual))
    if missing:
        errors.append("exported netlist missing frozen nets: " + ", ".join(missing))

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

    connected = set().union(*actual.values()) if actual else set()
    bad_nc = FORBIDDEN_CONNECTED & connected
    if bad_nc:
        errors.append("pins frozen NC are present on exported nets: " + fmt_nodes(bad_nc))

if errors:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    raise SystemExit(1)

print("M1.8d POWER/CHARGE/NC CONNECTIVITY PASS")
print(f"netlist: {NETLIST.relative_to(ROOT)}")
print(f"functional nets asserted: {len(FUNCTIONAL_NETS)}")
print(f"power/control/charge nets asserted: {len(POWER_NETS)}")
print(f"exact pin memberships asserted: {sum(len(nodes) for nodes in EXPECTED.values())}")
print(f"NC pins asserted absent from nets: {len(FORBIDDEN_CONNECTED)}")

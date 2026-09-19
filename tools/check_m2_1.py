#!/usr/bin/env python3
"""Structural qualification for the M2.1 native PCB mechanical baseline."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "hardware/C64RS232.kicad_pcb"
text = PCB.read_text() if PCB.is_file() else ""

def require(ok, msg):
    if not ok:
        raise SystemExit(f"M2.1 FAIL: {msg}")

require(text.startswith("(kicad_pcb"), "missing native KiCad PCB")
require('(general (thickness 1.57))' in text, "PCB thickness is not 1.57 mm")
require('(0 "F.Cu" signal)' in text and '(31 "B.Cu" signal)' in text, "expected two copper layers")
require(text.count('"F.Cu" signal') == 1 and text.count('"B.Cu" signal') == 1, "unexpected copper-layer definition")

expected = {
    "J1": "C64RS232:C64_User_Port_Edge",
    "J2": "C64RS232:TE_5747844-4",
    "U1": "Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm",
    "F1": "Fuse:Fuse_1206_3216Metric_Pad1.42x1.75mm_HandSolder",
    **{f"C{i}": "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder" for i in range(1, 6)},
}
fps = re.findall(r'\(footprint "([^"]+)".*?\(at ([0-9.]+) ([0-9.]+)\).*?\(property "Reference" "([^"]+)"', text, re.S)
by_ref = {}
for name, x, y, ref in fps:
    require(ref not in by_ref, f"duplicate footprint reference {ref}")
    by_ref[ref] = (name, float(x), float(y))
require(set(by_ref) == set(expected), f"expected exactly {sorted(expected)}, got {sorted(by_ref)}")
for ref, name in expected.items():
    require(by_ref[ref][0] == name, f"{ref} footprint regression: {by_ref[ref][0]}")

m = re.search(r'\(gr_rect \(start ([0-9.]+) ([0-9.]+)\) \(end ([0-9.]+) ([0-9.]+)\).*?\(layer "Edge.Cuts"\)\)', text, re.S)
require(m is not None, "closed rectangular Edge.Cuts missing")
x1, y1, x2, y2 = map(float, m.groups())
require(x2 > x1 and y2 > y1, "invalid board outline")
require(abs(by_ref["J1"][2] - y1) < 0.001, "J1 insertion datum is not anchored to top board edge")
# TE footprint connector-front datum is local y=-8.08; with J2 at 77.08 this is y=69.00.
require(abs((by_ref["J2"][2] - 8.08) - 69.00) < 0.001, "J2 connector-front datum moved")
require(y2 > by_ref["J2"][2], "J2 is not placed at the opposite end of the board")

print("M2.1 PCB STRUCTURAL QUALIFICATION PASS")
print("  native KiCad PCB; 2 copper layers; 1.57 mm")
print("  9 frozen footprints exactly once")
print("  closed provisional Edge.Cuts; J1/J2 mechanical anchors retained")
print("  later M2 copper is permitted; M2.1 checks only its frozen structural contract")

#!/usr/bin/env python3
"""Static M1.10 audit for C64RS232 frozen physical parts and footprints."""
from pathlib import Path
import re
import sys

FP = Path("hardware/C64RS232.pretty/C64_User_Port_Edge.kicad_mod")
BOM = Path("hardware/BOM_M1.csv")
GATE = Path("hardware/M1_10_FOOTPRINT_GATE.md")
SCH = Path("hardware/C64RS232_M1.sch")
EXPECTED = [str(i) for i in range(1, 13)] + list("ABCDEFHJKLMN")
PITCH = 3.96


def fail(msg: str) -> None:
    print(f"M1.10 FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)

if not FP.is_file(): fail(f"missing footprint: {FP}")
text = FP.read_text(encoding="utf-8")
pads = re.findall(r'\(pad\s+"([^"]+)"\s+connect\s+roundrect\s+\(at\s+([-0-9.]+)\s+([-0-9.]+)\)', text)
if len(pads) != 24: fail(f"expected 24 edge pads, found {len(pads)}")
names = [p[0] for p in pads]
if sorted(names) != sorted(EXPECTED): fail(f"pad set mismatch: {names}")
by_name = {name: (float(x), float(y)) for name, x, y in pads}
for side in ([str(i) for i in range(1, 13)], list("ABCDEFHJKLMN")):
    xs = [by_name[name][0] for name in side]
    for a, b in zip(xs, xs[1:]):
        if abs((b-a)-PITCH) > 1e-6: fail(f"bad pitch {b-a:.4f} mm")
if abs(by_name["12"][0]-by_name["1"][0]-43.56) > 1e-6: fail("bad contact-centre span")
if 'layers "F.Cu" "F.Mask"' not in text or 'layers "B.Cu" "B.Mask"' not in text: fail("both copper/mask sides required")
if "PCB EDGE" not in text: fail("PCB edge datum marker missing")

for path in (GATE, BOM, SCH):
    if not path.is_file(): fail(f"missing required file: {path}")
gate = GATE.read_text(encoding="utf-8")
bom = BOM.read_text(encoding="utf-8")
sch = SCH.read_text(encoding="utf-8")
for required in ("5747844-4", "1206L010/30WR", "100 mA", "250 mA", "30 V", "1.57 mm"):
    if required not in gate: fail(f"gate document missing: {required}")
if "MAX3243EIPWR" not in bom: fail("BOM lost MAX3243EIPWR")

assignments = {
    "J1": "C64RS232:C64_User_Port_Edge",
    "U1": "Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm",
    "J2": "Connector_Dsub:DSUB-9_Female_Horizontal_P2.77x2.84mm_EdgePinOffset9.40mm_Housed_MountingHolesOffset11.32mm",
    "F1": "Fuse:Fuse_1206_3216Metric_Pad1.42x1.75mm_HandSolder",
    "C1": "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder",
    "C2": "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder",
    "C3": "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder",
    "C4": "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder",
    "C5": "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder",
}
for ref, footprint in assignments.items():
    pos = sch.find(f'F 0 "{ref}"')
    end = sch.find('$EndComp', pos)
    if pos < 0 or end < 0: fail(f"component {ref} missing")
    if f'F 2 "{footprint}"' not in sch[pos:end]: fail(f"{ref} footprint not frozen to {footprint}")
for value in ("MAX3243EIPWR", "5747844-4", "1206L010/30WR"):
    if value not in sch: fail(f"schematic missing frozen value {value}")

print("M1.10 FOOTPRINT ASSIGNMENT AUDIT PASS")
print("  J1: project-local C64 User Port footprint")
print("  U1: TSSOP-28 PW")
print("  J2: frozen horizontal female DE-9 footprint")
print("  F1: 1206 PPTC footprint")
print("  C1-C5: 0805 footprints")
print("NOTE: J1 pad length/width, insertion depth, bevel and final edge geometry remain mechanical verification gates.")
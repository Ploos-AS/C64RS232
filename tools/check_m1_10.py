#!/usr/bin/env python3
"""Static M1.10 audit for the C64 User Port and frozen physical parts."""
from pathlib import Path
import csv
import re
import sys

FP = Path("hardware/C64RS232.pretty/C64_User_Port_Edge.kicad_mod")
BOM = Path("hardware/BOM_M1.csv")
GATE = Path("hardware/M1_10_FOOTPRINT_GATE.md")
EXPECTED = [str(i) for i in range(1, 13)] + list("ABCDEFHJKLMN")
PITCH = 3.96


def fail(msg: str) -> None:
    print(f"M1.10 FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


if not FP.is_file():
    fail(f"missing footprint: {FP}")

text = FP.read_text(encoding="utf-8")
pads = re.findall(r'\(pad\s+"([^"]+)"\s+connect\s+roundrect\s+\(at\s+([-0-9.]+)\s+([-0-9.]+)\)', text)
if len(pads) != 24:
    fail(f"expected 24 edge pads, found {len(pads)}")

names = [p[0] for p in pads]
if sorted(names) != sorted(EXPECTED):
    fail(f"pad set mismatch: {names}")

by_name = {name: (float(x), float(y)) for name, x, y in pads}
for side in ([str(i) for i in range(1, 13)], list("ABCDEFHJKLMN")):
    xs = [by_name[name][0] for name in side]
    for a, b in zip(xs, xs[1:]):
        if abs((b - a) - PITCH) > 1e-6:
            fail(f"bad pitch {b-a:.4f} mm; expected {PITCH:.2f} mm")

for name in [str(i) for i in range(1, 13)]:
    if by_name[name][1] >= 0:
        fail(f"numeric contact {name} is not on front side row")
for name in list("ABCDEFHJKLMN"):
    if by_name[name][1] <= 0:
        fail(f"letter contact {name} is not on back side row")

if 'layers "F.Cu" "F.Mask"' not in text or 'layers "B.Cu" "B.Mask"' not in text:
    fail("both copper/mask sides must be present")
if "PCB EDGE" not in text:
    fail("PCB edge datum marker missing")

span = by_name["12"][0] - by_name["1"][0]
if abs(span - 43.56) > 1e-6:
    fail(f"contact-centre span is {span:.2f} mm; expected 43.56 mm")

if not GATE.is_file():
    fail(f"missing gate document: {GATE}")
gate = GATE.read_text(encoding="utf-8")
for required in (
    "5747844-4",
    "1206L010/30WR",
    "100 mA",
    "250 mA",
    "30 V",
    "1.57 mm",
):
    if required not in gate:
        fail(f"gate document missing frozen part datum: {required}")

if not BOM.is_file():
    fail(f"missing BOM: {BOM}")
with BOM.open(encoding="utf-8", newline="") as fh:
    bom_text = fh.read()
if "MAX3243EIPWR" not in bom_text:
    fail("BOM lost frozen MAX3243EIPWR baseline")

print("M1.10 PHYSICAL-PART AUDIT PASS")
print("  J1 contacts: 24 (12 front + 12 back)")
print("  J1 pitch: 3.96 mm; centre span: 43.56 mm")
print("  J2 frozen: TE Connectivity 5747844-4")
print("  F1 frozen: Littelfuse 1206L010/30WR (100 mA hold / 250 mA trip / 30 V)")
print("NOTE: J1 pad length/width, insertion depth, bevel and final edge geometry remain mechanical verification gates.")
print("NOTE: J2/F1 KiCad land-pattern assignment remains required before M1.10 completion.")

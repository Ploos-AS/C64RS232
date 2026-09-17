#!/usr/bin/env python3
"""Static M1.10 audit for the project-local C64 User Port footprint."""
from pathlib import Path
import re
import sys

FP = Path("hardware/C64RS232.pretty/C64_User_Port_Edge.kicad_mod")
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

print("M1.10 USER PORT FOOTPRINT STATIC PASS")
print("  contacts: 24 (12 front + 12 back)")
print("  pitch: 3.96 mm")
print("  contact-centre span: 43.56 mm")
print("  numbering: 1-12 / A-F,H,J-N")
print("NOTE: pad length/width, insertion depth, bevel and key/notch remain mechanical verification gates.")

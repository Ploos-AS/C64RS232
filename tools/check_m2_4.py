#!/usr/bin/env python3
"""Qualify the frozen M2.4 mechanical footprint baseline."""
from pathlib import Path
import re

PCB = Path(__file__).resolve().parents[1] / "hardware/C64RS232.kicad_pcb"
text = PCB.read_text()

def require(ok, msg):
    if not ok:
        raise SystemExit("M2.4 FAIL: " + msg)

# The generator currently places the frozen mechanical anchors at these
# board-relative positions. Keep this gate numeric and independent of
# whitespace/serialization details.
require('(gr_rect (start 28.00 20.00) (end 80.44 85.16)' in text,
        "board outline does not match the frozen 52.44 x 65.16 mm envelope")

# J1 insertion edge is deliberately coincident with the top board edge.
require('(footprint "C64_User_Port_Edge"' in text, "C64 User Port footprint missing")
require('(at 32.44 20.00)' in text, "C64 User Port mechanical anchor moved")
require('PCB EDGE / INSERTION' in text, "C64 insertion-edge marking missing")

# TE 5747844-4 footprint includes the two manufacturer boardlock holes.
require('(footprint "TE_5747844-4"' in text, "TE 5747844-4 footprint missing")
require('(at 54.22 77.08)' in text, "DE-9 mechanical anchor moved")
require('(pad "MP1" thru_hole circle' in text and '(pad "MP2" thru_hole circle' in text,
        "DE-9 boardlock mounting holes missing")
require('(drill 3.18)' in text, "DE-9 boardlock drill size missing")

# Keep the manufacturer drawing identity visible in the native footprint.
require('TE 5747844-4 / DRAWING 5747844 REV P' in text,
        "DE-9 manufacturer drawing reference missing")

# Frozen J1 pad pitch / contact geometry is 3.96 mm.
j1 = text[text.find('(footprint "C64_User_Port_Edge"'):text.find('(footprint "TE_5747844-4"')]
require(j1.count('(pad "') == 24, "C64 User Port must expose 24 contacts")
require('(at 3.96 3.81)' in j1, "C64 User Port 3.96 mm pitch anchor missing")

print("M2.4 MECHANICAL BASELINE PASS")
print("  board envelope, J1 insertion edge, J2 boardlocks and frozen connector geometry verified")

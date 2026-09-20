#!/usr/bin/env python3
"""Qualify the frozen M2.4 mechanical footprint baseline."""
from pathlib import Path
import re
import pcbnew

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
board = pcbnew.LoadBoard(str(PCB))
refs = {fp.GetReference(): fp for fp in board.GetFootprints()}
j1p = refs["J1"].GetPosition()
require(abs(pcbnew.ToMM(j1p.x) - 32.44) < 0.001 and abs(pcbnew.ToMM(j1p.y) - 20.0) < 0.001,
        "C64 User Port mechanical anchor moved")
require('PCB EDGE / INSERTION' in text, "C64 insertion-edge marking missing")

# TE 5747844-4 footprint includes the two manufacturer boardlock holes.
require('(footprint "TE_5747844-4"' in text, "TE 5747844-4 footprint missing")
j2p = refs["J2"].GetPosition()
require(abs(pcbnew.ToMM(j2p.x) - 54.22) < 0.001 and abs(pcbnew.ToMM(j2p.y) - 77.08) < 0.001,
        "DE-9 mechanical anchor moved")
require('(pad "MP1" thru_hole circle' in text and '(pad "MP2" thru_hole circle' in text,
        "DE-9 boardlock mounting holes missing")
require('(drill 3.18)' in text, "DE-9 boardlock drill size missing")

# Keep the manufacturer drawing identity visible in the native footprint.
require('TE 5747844-4 / DRAWING 5747844 REV P' in text,
        "DE-9 manufacturer drawing reference missing")

# Frozen J1 pad inventory / pitch is verified from KiCad's parsed geometry.
j1pads = list(refs["J1"].Pads())
require(len(j1pads) == 24, "C64 User Port must expose 24 contacts")
padpos = {p.GetNumber(): p.GetPosition() for p in j1pads}
p1, p2 = padpos["1"], padpos["2"]
require(abs((pcbnew.ToMM(p2.x) - pcbnew.ToMM(p1.x)) - 3.96) < 0.001,
        "C64 User Port 3.96 mm pitch anchor missing")
require({p.GetNumber() for p in j1pads} == set([str(n) for n in range(1,13)] + list("ABCDEFHJKLMN")),
        "C64 User Port contact identifiers changed")

print("M2.4 MECHANICAL BASELINE PASS")
print("  board envelope, J1 insertion edge, J2 boardlocks and frozen connector geometry verified")

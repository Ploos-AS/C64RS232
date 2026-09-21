#!/usr/bin/env python3
"""Structural qualification for the M2.1 native PCB mechanical baseline."""
from pathlib import Path
import re
import pcbnew

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
    "J1": "C64_User_Port_Edge",
    "J2": "TE_5747844-4",
    "U1": "TSSOP-28_4.4x9.7mm_P0.65mm",
    "F1": "Fuse_1206_3216Metric_Pad1.42x1.75mm_HandSolder",
    **{f"C{i}": "C_0805_2012Metric_Pad1.18x1.45mm_HandSolder" for i in range(1, 6)},
}
board = pcbnew.LoadBoard(str(PCB))
footprints = list(board.GetFootprints())
by_ref = {}
for fp in footprints:
    ref = str(fp.GetReference())
    require(ref not in by_ref, f"duplicate footprint reference {ref}")
    by_ref[ref] = (str(fp.GetFPID().GetLibItemName()), float(fp.GetPosition().x), float(fp.GetPosition().y))
require(set(by_ref) == set(expected), f"expected exactly {sorted(expected)}, got {sorted(by_ref)}")
for ref, name in expected.items():
    require(by_ref[ref][0] == name, f"{ref} footprint regression: {by_ref[ref][0]}")


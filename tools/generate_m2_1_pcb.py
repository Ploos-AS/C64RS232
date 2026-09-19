#!/usr/bin/env python3
"""Generate a deterministic native KiCad M2.1 PCB skeleton.

M2.1 is a mechanical/placement gate. Connectivity/routing remains qualified
from the schematic and is intentionally deferred to later M2 stages.
"""
from pathlib import Path
import os
import pcbnew

ROOT = Path(__file__).resolve().parents[1]
HW = ROOT / "hardware"
PCB = HW / "C64RS232.kicad_pcb"
PROJECT_LIB = HW / "C64RS232.pretty"
SYSTEM_LIB = Path(os.environ.get("KICAD9_FOOTPRINT_DIR", "/usr/share/kicad/footprints"))

footprints = [
    ("J1", "C64RS232:C64_User_Port_Edge", 54.22, 20.00),
    ("F1", "Fuse:Fuse_1206_3216Metric_Pad1.42x1.75mm_HandSolder", 54.22, 32.00),
    ("U1", "Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm", 54.22, 48.00),
    ("C1", "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 45.00, 45.00),
    ("C2", "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 45.00, 49.00),
    ("C3", "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 63.00, 45.00),
    ("C4", "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 63.00, 49.00),
    ("C5", "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 54.22, 56.00),
    ("J2", "C64RS232:TE_5747844-4", 54.22, 77.08),
]

def footprint_file(name):
    lib, item = name.split(":", 1)
    if lib == "C64RS232":
        return PROJECT_LIB / f"{item}.kicad_mod"
    return SYSTEM_LIB / f"{lib}.pretty" / f"{item}.kicad_mod"

def fp(ref, name, x, y):
    path = footprint_file(name)
    if not path.is_file():
        raise SystemExit(f"missing footprint: {path}")
    loaded = pcbnew.FootprintLoad(str(path.parent), path.stem)
    if loaded is None:
        raise SystemExit(f"KiCad could not load footprint: {path}")
    loaded.SetReference(ref)
    loaded.SetPosition(pcbnew.VECTOR2I_MM(x, y))
    # Serialize the actual KiCad footprint, including pads and geometry.
    tmp = HW / f".{ref}.kicad_mod"\n    if not pcbnew.FootprintSave(str(tmp), loaded):\n        raise SystemExit(f"KiCad could not serialize footprint: {path}")\n    serialized = tmp.read_text()\n    tmp.unlink()\n    # FootprintSave writes the positioned/reference-updated native footprint.\n    return serialized


body = """(kicad_pcb
  (version 20240108)
  (generator pcbnew)
  (general (thickness 1.57))
  (paper "A4")
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (36 "B.SilkS" user "b.silkscreen")
    (37 "F.SilkS" user "f.silkscreen")
    (44 "Edge.Cuts" user)
  )
  (setup (pad_to_mask_clearance 0))\n  (net 0 "")\n  (net 1 "RAW_5V")\n  (net 2 "+5V")\n  (net 3 "GND")\n  (net 4 "C1_PLUS")\n  (net 5 "C1_MINUS")\n  (net 6 "C2_PLUS")\n  (net 7 "C2_MINUS")\n  (net 8 "VPLUS")\n  (net 9 "VMINUS")\n  (net 10 "C64_TXD")\n  (net 11 "C64_RXD")\n  (net 12 "C64_RTS")\n  (net 13 "C64_CTS")\n  (net 14 "C64_DTR")\n  (net 15 "C64_DSR")\n  (net 16 "C64_DCD")\n  (net 17 "C64_RI")\n  (net 18 "RS232_TXD")\n  (net 19 "RS232_RXD")\n  (net 20 "RS232_RTS")\n  (net 21 "RS232_CTS")\n  (net 22 "RS232_DTR")\n  (net 23 "RS232_DSR")\n  (net 24 "RS232_DCD")\n  (net 25 "RS232_RI")
""" + "\n".join(fp(*x) for x in footprints) + """
  (segment (start 54.22 27.00) (end 54.22 32.00) (width 0.60) (layer "F.Cu") (net 1))
  (segment (start 54.22 32.00) (end 54.22 39.00) (width 0.60) (layer "F.Cu") (net 2))
  (segment (start 54.22 39.00) (end 54.22 43.00) (width 0.40) (layer "F.Cu") (net 2))
  (segment (start 54.22 43.00) (end 54.22 45.00) (width 0.30) (layer "F.Cu") (net 2))
  (segment (start 54.22 45.00) (end 54.22 46.00) (width 0.30) (layer "F.Cu") (net 2))
  (segment (start 49.00 45.00) (end 50.50 46.00) (width 0.25) (layer "F.Cu") (net 4))
  (segment (start 49.00 49.00) (end 50.50 50.00) (width 0.25) (layer "F.Cu") (net 5))
  (segment (start 59.44 45.00) (end 58.00 46.00) (width 0.25) (layer "F.Cu") (net 6))
  (segment (start 59.44 49.00) (end 58.00 50.00) (width 0.25) (layer "F.Cu") (net 7))
  (segment (start 54.22 52.00) (end 54.22 56.00) (width 0.30) (layer "F.Cu") (net 3))
  (segment (start 36.00 34.00) (end 48.00 44.00) (width 0.25) (layer "F.Cu") (net 10))
  (segment (start 36.00 36.00) (end 48.00 46.00) (width 0.25) (layer "F.Cu") (net 11))
  (segment (start 36.00 38.00) (end 48.00 48.00) (width 0.25) (layer "F.Cu") (net 12))
  (segment (start 36.00 40.00) (end 48.00 50.00) (width 0.25) (layer "F.Cu") (net 13))
  (segment (start 36.00 42.00) (end 48.00 52.00) (width 0.25) (layer "F.Cu") (net 14))
  (segment (start 38.00 44.00) (end 48.00 54.00) (width 0.25) (layer "F.Cu") (net 15))
  (segment (start 38.00 46.00) (end 48.00 56.00) (width 0.25) (layer "F.Cu") (net 16))
  (segment (start 38.00 48.00) (end 48.00 58.00) (width 0.25) (layer "F.Cu") (net 17))
  (segment (start 60.00 44.00) (end 70.00 66.00) (width 0.25) (layer "F.Cu") (net 18))
  (segment (start 60.00 46.00) (end 70.00 68.00) (width 0.25) (layer "F.Cu") (net 19))
  (segment (start 60.00 48.00) (end 70.00 70.00) (width 0.25) (layer "F.Cu") (net 20))
  (segment (start 60.00 50.00) (end 70.00 72.00) (width 0.25) (layer "F.Cu") (net 21))
  (segment (start 60.00 52.00) (end 70.00 74.00) (width 0.25) (layer "F.Cu") (net 22))
  (segment (start 60.00 54.00) (end 68.00 76.00) (width 0.25) (layer "F.Cu") (net 23))
  (segment (start 60.00 56.00) (end 66.00 78.00) (width 0.25) (layer "F.Cu") (net 24))
  (segment (start 60.00 58.00) (end 64.00 80.00) (width 0.25) (layer "F.Cu") (net 25))
  (zone (net 3) (net_name "GND") (layer "B.Cu")
    (hatch edge 0.5)
    (connect_pads (clearance 0.3))
    (min_thickness 0.25)
    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.3))
    (polygon (pts (xy 28.50 20.50) (xy 79.94 20.50) (xy 79.94 84.66) (xy 28.50 84.66))))
  (gr_rect (start 28.00 20.00) (end 80.44 85.16)
    (stroke (width 0.2) (type default)) (fill none) (layer "Edge.Cuts"))
)
"""
PCB.write_text(body)
print(f"M2.1 deterministic native PCB skeleton generated: {PCB}")
print("  M2.3 baseline: 16 functional signal routes plus B.Cu GND plane")

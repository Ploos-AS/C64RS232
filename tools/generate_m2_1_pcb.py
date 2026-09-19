#!/usr/bin/env python3
"""Generate a deterministic native KiCad M2.1 PCB skeleton.

M2.1 is a mechanical/placement gate. Connectivity/routing remains qualified
from the schematic and is intentionally deferred to later M2 stages.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HW = ROOT / "hardware"
PCB = HW / "C64RS232.kicad_pcb"

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

def fp(ref, name, x, y):
    return f'''  (footprint "{name}" (layer "F.Cu") (at {x:.2f} {y:.2f})
    (property "Reference" "{ref}" (at 0 -3 0) (layer "F.SilkS"))
    (property "Value" "{name.split(":")[-1]}" (at 0 3 0) (layer "F.Fab") hide)
  )'''

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
  (setup (pad_to_mask_clearance 0))\n  (net 0 "")\n  (net 1 "RAW_5V")\n  (net 2 "+5V")\n  (net 3 "GND")\n  (net 4 "C1_PLUS")\n  (net 5 "C1_MINUS")\n  (net 6 "C2_PLUS")\n  (net 7 "C2_MINUS")\n  (net 8 "VPLUS")\n  (net 9 "VMINUS")
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
  (gr_rect (start 28.00 20.00) (end 80.44 85.16)
    (stroke (width 0.2) (type default)) (fill none) (layer "Edge.Cuts"))
)
"""
PCB.write_text(body)
print(f"M2.1 deterministic native PCB skeleton generated: {PCB}")
print("  M2.2 baseline: protected power spine plus compact charge-pump/bypass copper")

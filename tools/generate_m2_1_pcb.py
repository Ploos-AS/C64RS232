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
    ("J1", "C64RS232:C64_User_Port_Edge", 32.44, 20.00),
    ("F1", "Fuse:Fuse_1206_3216Metric_Pad1.42x1.75mm_HandSolder", 54.22, 32.00),
    ("U1", "Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm", 54.22, 48.00),
    ("C1", "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 61.00, 45.00),
    ("C2", "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 47.00, 44.10),
    ("C3", "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 61.00, 42.50),
    ("C4", "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 47.00, 46.50),
    ("C5", "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 61.00, 47.50),
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
    pad_nets = {
        "J1": {"2":"RAW_5V","A":"GND","N":"GND","B":"C64_RXD","C":"C64_RXD","D":"C64_RTS","E":"C64_DTR","F":"C64_RI","H":"C64_DCD","K":"C64_CTS","L":"C64_DSR","M":"C64_TXD"},
        "J2": {"1":"RS232_DCD","2":"RS232_RXD","3":"RS232_TXD","4":"RS232_DTR","5":"GND","6":"RS232_DSR","7":"RS232_RTS","8":"RS232_CTS","9":"RS232_RI"},
        "F1": {"1":"RAW_5V","2":"+5V"},
        "U1": {"1":"C2_PLUS","2":"C2_MINUS","3":"VMINUS","4":"RS232_RXD","5":"RS232_CTS","6":"RS232_DSR","7":"RS232_DCD","8":"RS232_RI",
               "9":"RS232_TXD","10":"RS232_RTS","11":"RS232_DTR","12":"C64_DTR","13":"C64_RTS","14":"C64_TXD","15":"C64_RI","16":"C64_DCD",
               "17":"C64_DSR","18":"C64_CTS","19":"C64_RXD","22":"+5V","23":"+5V","24":"C1_MINUS","25":"GND","26":"+5V","27":"VPLUS","28":"C1_PLUS"},
        "C1": {"1":"C1_PLUS","2":"C1_MINUS"},
        "C2": {"1":"C2_PLUS","2":"C2_MINUS"},
        "C3": {"1":"VPLUS","2":"GND"},
        "C4": {"1":"VMINUS","2":"GND"},
        "C5": {"1":"+5V","2":"GND"},
    }
    # Inject net attributes after serialization; net IDs are frozen by the board header.
    net_ids = {"RAW_5V":1,"+5V":2,"GND":3,"C1_PLUS":4,"C1_MINUS":5,"C2_PLUS":6,"C2_MINUS":7,"VPLUS":8,"VMINUS":9,"C64_TXD":10,"C64_RXD":11,"C64_RTS":12,"C64_CTS":13,"C64_DTR":14,"C64_DSR":15,"C64_DCD":16,"C64_RI":17,
               "RS232_TXD":18,"RS232_RXD":19,"RS232_RTS":20,"RS232_CTS":21,"RS232_DTR":22,"RS232_DSR":23,"RS232_DCD":24,"RS232_RI":25}
    board = pcbnew.BOARD()
    board.Add(loaded)
    tmp = HW / f".{ref}.kicad_pcb"
    pcbnew.SaveBoard(str(tmp), board)
    serialized_board = tmp.read_text()
    tmp.unlink()
    start = serialized_board.index("(footprint ")
    depth = 0
    end = None
    for pos in range(start, len(serialized_board)):
        ch = serialized_board[pos]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                end = pos + 1
                break
    if end is None:
        raise SystemExit(f"could not extract serialized footprint: {path}")
    serialized = serialized_board[start:end]
    for pin, net in pad_nets.get(ref, {}).items():
        marker = f'(pad "{pin}" '
        pos = serialized.find(marker)
        if pos < 0:
            raise SystemExit(f"missing {ref}/{pin} while assigning {net}")
        # Add the native pad net attribute before the pad closes; KiCad accepts it in pad scope.
        depth = 0
        pend = None
        for p in range(pos, len(serialized)):
            if serialized[p] == "(":
                depth += 1
            elif serialized[p] == ")":
                depth -= 1
                if depth == 0:
                    pend = p
                    break
        if pend is None:
            raise SystemExit(f"could not parse {ref}/{pin}")
        attr = f'\n\t\t(net {net_ids[net]} "{net}")'
        serialized = serialized[:pend] + attr + serialized[pend:]
    return serialized

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
  (segment (start 36.40 23.81) (end 52.7325 32.00) (width 0.60) (layer "F.Cu") (net 1))
  (segment (start 55.7075 32.00) (end 60.0000 38.0000) (width 0.60) (layer "F.Cu") (net 2))
  (segment (start 60.0000 38.0000) (end 60.0000 41.0000) (width 0.40) (layer "F.Cu") (net 2))
  (segment (start 60.0000 41.0000) (end 66.5000 41.0000) (width 0.40) (layer "F.Cu") (net 2))
  (segment (start 66.5000 41.0000) (end 66.5000 48.5000) (width 0.40) (layer "F.Cu") (net 2))
  (segment (start 57.0825 45.0750) (end 58.5000 45.0750) (width 0.25) (layer "F.Cu") (net 2))\n  (via (at 58.5000 45.0750) (size 0.7) (drill 0.35) (layers "F.Cu" "B.Cu") (net 2))
  (segment (start 57.0825 47.0250) (end 58.5000 47.0250) (width 0.25) (layer "F.Cu") (net 2))\n  (via (at 58.5000 47.0250) (size 0.7) (drill 0.35) (layers "F.Cu" "B.Cu") (net 2))
  (segment (start 57.0825 47.6750) (end 59.0000 48.3000) (width 0.25) (layer "F.Cu") (net 2))\n  (via (at 59.0000 48.3000) (size 0.7) (drill 0.35) (layers "F.Cu" "B.Cu") (net 2))
  (via (at 59.9625 47.5000) (size 0.7) (drill 0.35) (layers "F.Cu" "B.Cu") (net 2))\n  (segment (start 58.5000 45.0750) (end 66.5000 45.0750) (width 0.30) (layer "B.Cu") (net 2))\n  (segment (start 58.5000 47.0250) (end 66.5000 47.0250) (width 0.30) (layer "B.Cu") (net 2))\n  (segment (start 59.0000 48.3000) (end 66.5000 48.3000) (width 0.30) (layer "B.Cu") (net 2))\n  (segment (start 66.5000 45.0750) (end 66.5000 48.3000) (width 0.30) (layer "B.Cu") (net 2))
  (via (at 66.5000 41.0000) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 2))
  (segment (start 66.5000 41.0000) (end 66.5000 45.0750) (width 0.40) (layer "B.Cu") (net 2))
  (segment (start 58.5000 45.0750) (end 58.5000 40.0000) (width 0.30) (layer "B.Cu") (net 2))
  (segment (start 58.5000 47.0250) (end 57.5000 40.0000) (width 0.30) (layer "B.Cu") (net 2))
  (segment (start 59.0000 48.3000) (end 56.5000 40.0000) (width 0.30) (layer "B.Cu") (net 2))
  (segment (start 59.9625 47.5000) (end 55.5000 40.0000) (width 0.30) (layer "B.Cu") (net 2))
  (segment (start 55.5000 40.0000) (end 66.5000 40.0000) (width 0.30) (layer "B.Cu") (net 2))
  (segment (start 57.0825 43.7750) (end 59.0000 43.7750) (width 0.20) (layer "F.Cu") (net 4))
  (segment (start 59.0000 43.7750) (end 59.9625 45.0000) (width 0.20) (layer "F.Cu") (net 4))
  (segment (start 57.0825 46.3750) (end 60.0000 46.3750) (width 0.20) (layer "F.Cu") (net 5))
  (segment (start 60.0000 46.3750) (end 62.0375 45.0000) (width 0.20) (layer "F.Cu") (net 5))
  (segment (start 51.3575 43.7750) (end 49.5000 43.7750) (width 0.20) (layer "F.Cu") (net 6))
  (segment (start 49.5000 43.7750) (end 45.9625 44.1000) (width 0.20) (layer "F.Cu") (net 6))
  (segment (start 51.3575 44.4250) (end 49.5000 44.4250) (width 0.20) (layer "F.Cu") (net 7))
  (segment (start 49.5000 44.4250) (end 48.0375 44.1000) (width 0.20) (layer "F.Cu") (net 7))
  (segment (start 57.0825 44.4250) (end 59.0000 44.4250) (width 0.20) (layer "F.Cu") (net 8))
  (segment (start 59.0000 44.4250) (end 59.9625 42.5000) (width 0.20) (layer "F.Cu") (net 8))
  (segment (start 51.3575 45.0750) (end 49.5000 45.0750) (width 0.20) (layer "F.Cu") (net 9))
  (segment (start 49.5000 45.0750) (end 45.9625 46.5000) (width 0.20) (layer "F.Cu") (net 9))
  (segment (start 57.0825 45.7250) (end 58.2000 45.7250) (width 0.25) (layer "F.Cu") (net 3))
  (via (at 58.2000 45.7250) (size 0.7) (drill 0.35) (layers "F.Cu" "B.Cu") (net 3))
  (segment (start 58.2000 45.7250) (end 57.0825 45.7250) (width 0.25) (layer "F.Cu") (net 3))
  (via (at 62.0375 42.5000) (size 0.7) (drill 0.35) (layers "F.Cu" "B.Cu") (net 3))
  (via (at 62.0375 47.5000) (size 0.7) (drill 0.35) (layers "F.Cu" "B.Cu") (net 3))
  (segment (start 62.0375 47.5000) (end 64.0375 47.5000) (width 0.25) (layer "F.Cu") (net 3))
  (segment (start 64.0375 47.5000) (end 64.0375 45.0000) (width 0.25) (layer "F.Cu") (net 3))
  (via (at 45.9625 46.5000) (size 0.7) (drill 0.35) (layers "F.Cu" "B.Cu") (net 9))
  (segment (start 48.0375 46.5000) (end 57.0825 45.7250) (width 0.20) (layer "F.Cu") (net 3))
  (segment (start 59.7064 75.6576) (end 62.0375 47.5000) (width 0.25) (layer "B.Cu") (net 3))
  (via (at 62.0375 47.5000) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 3))
  (via (at 62.0375 42.5000) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 3))
  (segment (start 32.4400 23.8100) (end 30.5000 23.8100) (width 0.30) (layer "B.Cu") (net 3))
  (segment (start 30.5000 23.8100) (end 30.5000 60.0000) (width 0.30) (layer "B.Cu") (net 3))
  (segment (start 30.5000 60.0000) (end 62.0375 42.5000) (width 0.30) (layer "B.Cu") (net 3))
  (segment (start 76.0000 23.8100) (end 78.0000 23.8100) (width 0.30) (layer "B.Cu") (net 3))
  (segment (start 78.0000 23.8100) (end 78.0000 60.0000) (width 0.30) (layer "B.Cu") (net 3))
  (segment (start 78.0000 60.0000) (end 62.0375 42.5000) (width 0.30) (layer "B.Cu") (net 3))
  (segment (start 72.0400 23.8100) (end 72.0400 39.0000) (width 0.25) (layer "B.Cu") (net 10))
  (segment (start 72.0400 39.0000) (end 49.0000 52.2250) (width 0.25) (layer "B.Cu") (net 10))
  (segment (start 49.0000 52.2250) (end 51.3575 52.2250) (width 0.25) (layer "F.Cu") (net 10))
  (segment (start 36.4000 23.8100) (end 36.4000 33.0000) (width 0.25) (layer "B.Cu") (net 11))
  (segment (start 40.3600 23.8100) (end 40.3600 33.0000) (width 0.25) (layer "B.Cu") (net 11))
  (segment (start 36.4000 33.0000) (end 40.3600 33.0000) (width 0.25) (layer "B.Cu") (net 11))
  (segment (start 40.3600 33.0000) (end 62.0000 49.6250) (width 0.25) (layer "B.Cu") (net 11))
  (segment (start 62.0000 49.6250) (end 57.0825 49.6250) (width 0.25) (layer "F.Cu") (net 11))
  (segment (start 44.3200 23.8100) (end 44.3200 34.0000) (width 0.25) (layer "B.Cu") (net 12))
  (segment (start 44.3200 34.0000) (end 48.0000 51.5750) (width 0.25) (layer "B.Cu") (net 12))
  (segment (start 48.0000 51.5750) (end 51.3575 51.5750) (width 0.25) (layer "F.Cu") (net 12))
  (segment (start 64.1200 23.8100) (end 64.1200 35.0000) (width 0.25) (layer "B.Cu") (net 13))
  (segment (start 64.1200 35.0000) (end 63.0000 50.2750) (width 0.25) (layer "B.Cu") (net 13))
  (segment (start 63.0000 50.2750) (end 57.0825 50.2750) (width 0.25) (layer "F.Cu") (net 13))
  (segment (start 48.2800 23.8100) (end 48.2800 35.0000) (width 0.25) (layer "B.Cu") (net 14))
  (segment (start 48.2800 35.0000) (end 47.0000 50.9250) (width 0.25) (layer "B.Cu") (net 14))
  (segment (start 47.0000 50.9250) (end 51.3575 50.9250) (width 0.25) (layer "F.Cu") (net 14))
  (segment (start 68.0800 23.8100) (end 68.0800 36.0000) (width 0.25) (layer "B.Cu") (net 15))
  (segment (start 68.0800 36.0000) (end 64.0000 50.9250) (width 0.25) (layer "B.Cu") (net 15))
  (segment (start 64.0000 50.9250) (end 57.0825 50.9250) (width 0.25) (layer "F.Cu") (net 15))
  (segment (start 56.2000 23.8100) (end 56.2000 36.0000) (width 0.25) (layer "B.Cu") (net 16))
  (segment (start 56.2000 36.0000) (end 65.0000 51.5750) (width 0.25) (layer "B.Cu") (net 16))
  (segment (start 65.0000 51.5750) (end 57.0825 51.5750) (width 0.25) (layer "F.Cu") (net 16))
  (segment (start 52.2400 23.8100) (end 52.2400 37.0000) (width 0.25) (layer "B.Cu") (net 17))
  (segment (start 52.2400 37.0000) (end 66.0000 52.2250) (width 0.25) (layer "B.Cu") (net 17))
  (segment (start 66.0000 52.2250) (end 57.0825 52.2250) (width 0.25) (layer "F.Cu") (net 17))
  (segment (start 51.3575 48.9750) (end 54.2200 53.0000) (width 0.25) (layer "F.Cu") (net 18))\n  (segment (start 54.2200 53.0000) (end 54.2200 75.6576) (width 0.25) (layer "F.Cu") (net 18))
  (segment (start 51.3575 45.7250) (end 46.0000 54.0000) (width 0.25) (layer "F.Cu") (net 19))\n  (segment (start 46.0000 54.0000) (end 46.0000 70.0000) (width 0.25) (layer "F.Cu") (net 19))\n  (segment (start 46.0000 70.0000) (end 51.4768 75.6576) (width 0.25) (layer "F.Cu") (net 19))
  (segment (start 51.3575 49.6250) (end 52.8484 54.5000) (width 0.25) (layer "F.Cu") (net 20))\n  (segment (start 52.8484 54.5000) (end 52.8484 78.5024) (width 0.25) (layer "F.Cu") (net 20))
  (segment (start 51.3575 46.3750) (end 47.0000 55.0000) (width 0.25) (layer "F.Cu") (net 21))\n  (segment (start 47.0000 55.0000) (end 47.0000 70.0000) (width 0.25) (layer "F.Cu") (net 21))\n  (segment (start 47.0000 70.0000) (end 55.5916 78.5024) (width 0.25) (layer "F.Cu") (net 21))
  (segment (start 51.3575 50.2750) (end 56.9632 55.5000) (width 0.25) (layer "F.Cu") (net 22))\n  (segment (start 56.9632 55.5000) (end 56.9632 75.6576) (width 0.25) (layer "F.Cu") (net 22))
  (segment (start 51.3575 47.0250) (end 48.0000 56.0000) (width 0.25) (layer "F.Cu") (net 23))\n  (segment (start 48.0000 56.0000) (end 48.0000 70.0000) (width 0.25) (layer "F.Cu") (net 23))\n  (segment (start 48.0000 70.0000) (end 50.1052 78.5024) (width 0.25) (layer "F.Cu") (net 23))
  (segment (start 51.3575 47.6750) (end 49.0000 57.0000) (width 0.25) (layer "F.Cu") (net 24))\n  (segment (start 49.0000 57.0000) (end 49.0000 70.0000) (width 0.25) (layer "F.Cu") (net 24))\n  (segment (start 49.0000 70.0000) (end 48.7336 75.6576) (width 0.25) (layer "F.Cu") (net 24))
  (segment (start 51.3575 48.3250) (end 58.3348 57.5000) (width 0.25) (layer "F.Cu") (net 25))\n  (segment (start 58.3348 57.5000) (end 58.3348 78.5024) (width 0.25) (layer "F.Cu") (net 25))
  (zone (net 3) (net_name "GND") (layer "B.Cu")
    (hatch edge 0.5)
    (connect_pads (clearance 0.25))
    (min_thickness 0.25)
    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.3))
    (polygon (pts
      (xy 28.50 20.50)
      (xy 79.94 20.50)
      (xy 79.94 84.66)
      (xy 28.50 84.66)
    ))
  )
  (segment (start 64.0375 45.0000) (end 64.0375 49.0000) (width 0.30) (layer "F.Cu") (net 3))
  (segment (start 57.0825 45.7250) (end 64.0375 45.0000) (width 0.30) (layer "F.Cu") (net 3))
  (via (at 57.0825 45.7250) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 3))
  (via (at 64.0375 45.0000) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 3))
  (via (at 64.0375 49.0000) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 3))
  (via (at 49.0000 52.2250) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 10))
  (via (at 62.0000 49.6250) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 11))
  (via (at 48.0000 51.5750) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 12))
  (via (at 63.0000 50.2750) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 13))
  (via (at 47.0000 50.9250) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 14))
  (via (at 64.0000 50.9250) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 15))
  (via (at 65.0000 51.5750) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 16))
  (via (at 66.0000 52.2250) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 17))
  (gr_rect (start 28.00 20.00) (end 80.44 85.16)
    (stroke (width 0.2) (type default)) (fill none) (layer "Edge.Cuts"))
)
"""
PCB.write_text(body)
print(f"M2.1 deterministic native PCB skeleton generated: {PCB}")
print("  M2.3 baseline: 16 functional signal routes plus B.Cu GND plane")

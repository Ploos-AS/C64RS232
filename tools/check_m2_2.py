#!/usr/bin/env python3
"""Qualification for the M2.2 protected-power and charge-pump copper baseline."""
from pathlib import Path
import re

PCB = Path(__file__).resolve().parents[1] / "hardware/C64RS232.kicad_pcb"
text = PCB.read_text() if PCB.is_file() else ""

def require(ok, msg):
    if not ok:
        raise SystemExit(f"M2.2 FAIL: {msg}")

nets = {int(n): name for n, name in re.findall(r'\(net (\d+) "([^"]*)"\)', text)}
expected = {1:"RAW_5V",2:"+5V",3:"GND",4:"C1_PLUS",5:"C1_MINUS",6:"C2_PLUS",7:"C2_MINUS",8:"VPLUS",9:"VMINUS"}
for n, name in expected.items():
    require(nets.get(n) == name, f"net {n} must be {name}")

segments = re.findall(r'\(segment \(start ([0-9.]+) ([0-9.]+)\) \(end ([0-9.]+) ([0-9.]+)\) \(width ([0-9.]+)\) \(layer "([^"]+)"\) \(net (\d+)\)\)', text)
require(len(segments) >= 10, "expected M2.2 copper segments")
by_net = {}
for x1,y1,x2,y2,w,layer,n in segments:
    by_net.setdefault(int(n), []).append((float(x1),float(y1),float(x2),float(y2),float(w),layer))

require(1 in by_net and max(x[4] for x in by_net[1]) >= 0.60, "RAW_5V entry must use >=0.60 mm copper")
require(2 in by_net and max(x[4] for x in by_net[2]) >= 0.60, "protected +5V spine must use >=0.60 mm copper")
for n in (4,5,6,7):
    require(n in by_net, f"{expected[n]} charge-pump copper missing")
    require(all(x[5] == "F.Cu" for x in by_net[n]), f"{expected[n]} must remain on F.Cu in M2.2 baseline")
require(3 in by_net, "local GND/bypass copper missing")
# Later M2 stages may add functional signal nets/routes; this gate only preserves M2.2 copper.\n

print("M2.2 POWER/CHARGE-PUMP QUALIFICATION PASS")
print(f"  {len(segments)} copper segments")
print("  RAW_5V/+5V power spine present; charge-pump and local bypass copper present")
print("  functional C64/RS-232 signal routing remains deferred to M2.3")

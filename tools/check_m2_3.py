#!/usr/bin/env python3
"""Qualify the M2.3 functional signal-routing and B.Cu GND-plane baseline."""
from pathlib import Path
import re

PCB = Path(__file__).resolve().parents[1] / "hardware/C64RS232.kicad_pcb"
text = PCB.read_text() if PCB.is_file() else ""

def require(ok, msg):
    if not ok:
        raise SystemExit("M2.3 FAIL: " + msg)

nets = {int(n): name for n, name in re.findall(r'\(net (\d+) "([^"]+)"\)', text)}
required = {
    "C64_TXD","C64_RXD","C64_RTS","C64_CTS","C64_DTR","C64_DSR","C64_DCD","C64_RI",
    "RS232_TXD","RS232_RXD","RS232_RTS","RS232_CTS","RS232_DTR","RS232_DSR","RS232_DCD","RS232_RI",
}
missing = sorted(required - set(nets.values()))
require(not missing, "missing signal nets: " + ", ".join(missing))

segments = re.findall(r'\(segment \(start [^)]+\) \(end [^)]+\) \(width ([0-9.]+)\) \(layer "([^"]+)"\) \(net (\d+)\)\)', text)
by_name = {}
for width, layer, num in segments:
    name = nets.get(int(num))
    by_name.setdefault(name, []).append((float(width), layer))
for name in sorted(required):
    require(name in by_name, f"{name} has no routed copper")
    require(all(w >= 0.25 for w, _ in by_name[name]), f"{name} trace below 0.25 mm")

zone_start = text.find('(zone (net 3) (net_name "GND") (layer "B.Cu")')
require(zone_start >= 0, "B.Cu GND plane missing")
zone_text = text[zone_start:text.find('(gr_rect', zone_start)]
for x, y in (("28.5","20.5"),("79.94","20.5"),("79.94","84.66"),("28.5","84.66")):
    require(re.search(rf'\(xy {re.escape(x)}0* {re.escape(y)}0*\)', zone_text) is not None,
            f"GND plane corner {x},{y} missing")

print("M2.3 SIGNAL ROUTING/GND QUALIFICATION PASS")
print("  all 16 functional signal nets have >=0.25 mm routed copper")
print("  substantially board-wide B.Cu GND zone is present")

#!/usr/bin/env python3
"""M2.3 routing inventory gate: ensure the complete functional signal set is frozen."""
from pathlib import Path
import re

PCB = Path(__file__).resolve().parents[1] / "hardware/C64RS232.kicad_pcb"
text = PCB.read_text() if PCB.is_file() else ""
nets = {name for _, name in re.findall(r'\(net (\d+) "([^"]+)"\)', text)}
required = {
    "C64_TXD","C64_RXD","C64_RTS","C64_CTS","C64_DTR","C64_DSR","C64_DCD","C64_RI",
    "RS232_TXD","RS232_RXD","RS232_RTS","RS232_CTS","RS232_DTR","RS232_DSR","RS232_DCD","RS232_RI",
}
missing = sorted(required - nets)
if missing:
    raise SystemExit("M2.3 FAIL: missing signal nets: " + ", ".join(missing))
print("M2.3 SIGNAL INVENTORY PASS")
print("  all 16 functional C64/RS-232 signal nets are present")
print("  actual routing and GND plane remain required for M2.3 completion")

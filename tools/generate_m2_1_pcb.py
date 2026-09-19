#!/usr/bin/env python3
"""Generate the M2.1 native PCB placement baseline from the qualified schematic."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCH = ROOT / "hardware/C64RS232_M1.kicad_sch"
PCB = ROOT / "hardware/C64RS232.kicad_pcb"

if not SCH.is_file():
    raise SystemExit(f"missing schematic: {SCH}")

# KiCad 9 can create/update a PCB directly from the schematic while preserving
# the frozen footprint assignments. The generated file is intentionally
# unrouted; M2.1 is a mechanical/placement gate.
subprocess.run([
    "kicad-cli", "pcb", "create-from-schematic",
    "--output", str(PCB), str(SCH)
], check=True)

if not PCB.is_file() or PCB.stat().st_size == 0:
    raise SystemExit("native PCB was not generated")

print(f"M2.1 native PCB baseline generated: {PCB}")

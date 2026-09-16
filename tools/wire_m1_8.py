#!/usr/bin/env python3
"""Deterministically replace M1 floating labels with real pin-attached net labels.

The committed legacy schematic may already contain the M1.8 generated block.
Treat that state as success so CI can regenerate the native KiCad schematic
without failing before conversion.
"""
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "hardware" / "C64RS232_M1.sch"
s = p.read_text()

labels = {
    # C64-side functional nets
    (1300,4300):"C64_TXD", (4500,3900):"C64_TXD",
    (1300,3600):"C64_RTS", (4500,3800):"C64_RTS",
    (1300,3700):"C64_DTR", (4500,3700):"C64_DTR",
    (1300,3500):"C64_RXD", (1300,3400):"C64_RXD", (5900,3500):"C64_RXD",
    (1300,4100):"C64_CTS", (5900,3600):"C64_CTS",
    (1300,4200):"C64_DSR", (5900,3700):"C64_DSR",
    (1300,3900):"C64_DCD", (5900,3800):"C64_DCD",
    (1300,3800):"C64_RI",  (5900,3900):"C64_RI",
    # RS-232 side
    (4500,3400):"RS232_TXD", (8000,3600):"RS232_TXD",
    (4500,3500):"RS232_RTS", (8000,4000):"RS232_RTS",
    (4500,3600):"RS232_DTR", (8000,3700):"RS232_DTR",
    (4500,2900):"RS232_RXD", (8000,3500):"RS232_RXD",
    (4500,3000):"RS232_CTS", (8000,4100):"RS232_CTS",
    (4500,3100):"RS232_DSR", (8000,3900):"RS232_DSR",
    (4500,3200):"RS232_DCD", (8000,3400):"RS232_DCD",
    (4500,3300):"RS232_RI",  (8000,4200):"RS232_RI",
    # Power/control
    (2300,3400):"RAW_5V", (6850,1500):"RAW_5V",
    (7150,1500):"+5V", (5900,2800):"+5V", (5900,3100):"+5V", (5900,1450):"+5V",
    (2300,3300):"GND", (2300,4400):"GND", (1300,3300):"GND", (1300,4400):"GND",
    (5900,2900):"GND", (5900,3200):"GND", (8000,3800):"GND",
    (4900,1750):"GND", (5400,1750):"GND", (5900,1750):"GND",
    # Charge pump
    (3900,1450):"C1_PLUS", (5900,2600):"C1_PLUS",
    (3900,1750):"C1_MINUS", (5900,3000):"C1_MINUS",
    (4400,1450):"C2_PLUS", (4500,2600):"C2_PLUS",
    (4400,1750):"C2_MINUS", (4500,2700):"C2_MINUS",
    (4900,1450):"VPLUS", (5900,2700):"VPLUS",
    (5400,1450):"VMINUS", (4500,2800):"VMINUS",
}

# Idempotent fast path: the generated M1.8 block is already committed.
required = [
    'Rev "M1.8"',
    'Comment3 "M1.8 electrically connected baseline"',
    'Text Label 1300 4300 0 50 ~ 0\nC64_TXD\n',
    'Text Label 8000 4200 0 50 ~ 0\nRS232_RI\n',
    'NoConn ~ 5900 3300\n',
]
if all(token in s for token in required):
    print("M1.8 legacy schematic connectivity already generated")
    raise SystemExit(0)

anchor = "Text Label 2300 3000 0 50 ~ 0\nC64_+5V\n"
if anchor not in s:
    raise SystemExit("ERROR: neither M1 baseline anchor nor complete M1.8 generated block found")
start = s.index(anchor)
end = s.index("Wire Notes Line\n", start)

block = "".join(f"Text Label {x} {y} 0 50 ~ 0\n{name}\n" for (x,y),name in labels.items())
for x,y in [(2300,3500),(2300,3600),(2300,3700),(2300,3800),(2300,3900),(2300,4000),(2300,4100),(2300,4200),(2300,4300),(1300,4000),(5900,3400),(5900,3300)]:
    block += f"NoConn ~ {x} {y}\n"

s = s[:start] + block + s[end:]
s = s.replace('Rev "M1"', 'Rev "M1.8"').replace('Comment3 "M1 schematic baseline"', 'Comment3 "M1.8 electrically connected baseline"')
p.write_text(s)
print("M1.8 legacy schematic connectivity generated")

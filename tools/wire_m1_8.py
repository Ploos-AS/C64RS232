#!/usr/bin/env python3
"""Deterministically generate and normalize the M1.8 electrical baseline."""
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "hardware" / "C64RS232_M1.sch"
s = p.read_text()

# M1.8b: the protection part is the BOM's F1 resettable fuse, not a 1 kOhm
# resistor.  The legacy R graphic is retained temporarily as a generic
# two-terminal symbol, but the reference/value and pin-attached labels are
# corrected.  R1 is rotated, so its actual pins are (7000,1350)/(7000,1650).
s = s.replace('L R R1\nU 1 1 9\nP 7000 1500\nF 0 "R1" V 6793 1500 50 0000 C CNN\nF 1 "1k" V 6884 1500 50 0000 C CNN',
              'L R F1\nU 1 1 9\nP 7000 1500\nF 0 "F1" V 6793 1500 50 0000 C CNN\nF 1 "100mA PTC" V 6884 1500 50 0000 C CNN')
s = s.replace('Text Label 6850 1500 0 50 ~ 0\nRAW_5V\n',
              'Text Label 7000 1350 0 50 ~ 0\nRAW_5V\n')
s = s.replace('Text Label 7150 1500 0 50 ~ 0\n+5V\n',
              'Text Label 7000 1650 0 50 ~ 0\n+5V\n')

# The User Port is the real +5 V source, but the resettable fuse deliberately
# separates RAW_5V from the protected +5V net. KiCad does not propagate a
# power-output ERC driver through a passive component, so mark the protected
# rail with the standard PWR_FLAG semantics. This is an ERC annotation only;
# it adds no physical component to the BOM.
pwr_flag = '''$Comp\nL PWR_FLAG #FLG0101\nU 1 1 10\nP 7500 1650\nF 0 "#FLG0101" H 7500 1725 50 0001 C CNN\nF 1 "PWR_FLAG" H 7500 1823 50 0000 C CNN\n\t1    7500 1650\n\t1    0    0    -1\n$EndComp\n'''
if 'L PWR_FLAG #FLG0101' not in s:
    marker = '$EndSCHEMATC\n'
    if marker not in s:
        raise SystemExit('ERROR: legacy schematic end marker not found')
    s = s.replace(marker, pwr_flag + 'Text Label 7500 1650 0 50 ~ 0\n+5V\n' + marker)

labels = {
    (1300,4300):"C64_TXD", (4500,3900):"C64_TXD",
    (1300,3600):"C64_RTS", (4500,3800):"C64_RTS",
    (1300,3700):"C64_DTR", (4500,3700):"C64_DTR",
    (1300,3500):"C64_RXD", (1300,3400):"C64_RXD", (5900,3500):"C64_RXD",
    (1300,4100):"C64_CTS", (5900,3600):"C64_CTS",
    (1300,4200):"C64_DSR", (5900,3700):"C64_DSR",
    (1300,3900):"C64_DCD", (5900,3800):"C64_DCD",
    (1300,3800):"C64_RI",  (5900,3900):"C64_RI",
    (4500,3400):"RS232_TXD", (8000,3600):"RS232_TXD",
    (4500,3500):"RS232_RTS", (8000,4000):"RS232_RTS",
    (4500,3600):"RS232_DTR", (8000,3700):"RS232_DTR",
    (4500,2900):"RS232_RXD", (8000,3500):"RS232_RXD",
    (4500,3000):"RS232_CTS", (8000,4100):"RS232_CTS",
    (4500,3100):"RS232_DSR", (8000,3900):"RS232_DSR",
    (4500,3200):"RS232_DCD", (8000,3400):"RS232_DCD",
    (4500,3300):"RS232_RI",  (8000,4200):"RS232_RI",
    (2300,3400):"RAW_5V", (7000,1350):"RAW_5V",
    (7000,1650):"+5V", (5900,2800):"+5V", (5900,3100):"+5V", (5900,1450):"+5V",
    (2300,3300):"GND", (2300,4400):"GND", (1300,3300):"GND", (1300,4400):"GND",
    (5900,2900):"GND", (5900,3200):"GND", (8000,3800):"GND",
    (4900,1750):"GND", (5400,1750):"GND", (5900,1750):"GND",
    (3900,1450):"C1_PLUS", (5900,2600):"C1_PLUS",
    (3900,1750):"C1_MINUS", (5900,3000):"C1_MINUS",
    (4400,1450):"C2_PLUS", (4500,2600):"C2_PLUS",
    (4400,1750):"C2_MINUS", (4500,2700):"C2_MINUS",
    (4900,1450):"VPLUS", (5900,2700):"VPLUS",
    (5400,1450):"VMINUS", (4500,2800):"VMINUS",
}

required = [
    'Rev "M1.8"',
    'Comment3 "M1.8 electrically connected baseline"',
    'Text Label 1300 4300 0 50 ~ 0\nC64_TXD\n',
    'Text Label 8000 4200 0 50 ~ 0\nRS232_RI\n',
    'NoConn ~ 5900 3300\n',
]
if all(token in s for token in required):
    p.write_text(s)
    print("M1.8c legacy schematic connectivity normalized")
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
print("M1.8c legacy schematic connectivity generated")

#!/usr/bin/env python3
"""Deterministically generate and normalize the M1.10 electrical/footprint baseline."""
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "hardware" / "C64RS232_M1.sch"
s = p.read_text()

# Normalize values and add legacy KiCad footprint fields. These survive the
# deterministic legacy->native conversion performed by CI.
def set_component(ref, value=None, footprint=None):
    global s
    marker = f'F 0 "{ref}"'
    pos = s.find(marker)
    if pos < 0:
        raise SystemExit(f"ERROR: component {ref} not found")
    end = s.find('$EndComp', pos)
    if end < 0:
        raise SystemExit(f"ERROR: component {ref} has no end marker")
    block = s[pos:end]
    if value is not None:
        import re
        block = re.sub(r'F 1 "[^"]*"[^\n]*', f'F 1 "{value}" H 0 0 50 0000 C CNN', block, count=1)
    if footprint is not None:
        import re
        if re.search(r'\nF 2 "[^"]*"[^\n]*', block):
            block = re.sub(r'\nF 2 "[^"]*"[^\n]*', f'\nF 2 "{footprint}" H 0 0 50 0001 C CNN', block, count=1)
        else:
            f1_end = block.find('\n', block.find('F 1 '))
            block = block[:f1_end] + f'\nF 2 "{footprint}" H 0 0 50 0001 C CNN' + block[f1_end:]
    s = s[:pos] + block + s[end:]

set_component("J1", footprint="C64RS232:C64_User_Port_Edge")
set_component("U1", value="MAX3243EIPWR", footprint="Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm")
set_component("J2", value="5747844-4", footprint="Connector_Dsub:DSUB-9_Female_Horizontal_P2.77x2.84mm_EdgePinOffset9.40mm_Housed_MountingHolesOffset11.32mm")
for ref in ("C1", "C2", "C3", "C4", "C5"):
    set_component(ref, footprint="Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder")
set_component("F1", value="1206L010/30WR", footprint="Fuse:Fuse_1206_3216Metric_Pad1.42x1.75mm_HandSolder")

# Correct electrical baseline.
s = s.replace('Text Label 6850 1500 0 50 ~ 0\nRAW_5V\n', 'Text Label 7000 1350 0 50 ~ 0\nRAW_5V\n')
s = s.replace('Text Label 7150 1500 0 50 ~ 0\n+5V\n', 'Text Label 7000 1650 0 50 ~ 0\n+5V\n')

pwr_flag = '''$Comp\nL PWR_FLAG #FLG0101\nU 1 1 10\nP 7500 1650\nF 0 "#FLG0101" H 7500 1725 50 0001 C CNN\nF 1 "PWR_FLAG" H 7500 1823 50 0000 C CNN\n\t1    7500 1650\n\t1    0    0    -1\n$EndComp\n'''
if 'L PWR_FLAG #FLG0101' not in s:
    marker = '$EndSCHEMATC\n'
    if marker not in s:
        raise SystemExit('ERROR: legacy schematic end marker not found')
    s = s.replace(marker, pwr_flag + 'Text Label 7500 1650 0 50 ~ 0\n+5V\n' + marker)

labels = {
    (1300,4300):"C64_TXD", (4500,3900):"C64_TXD", (1300,3600):"C64_RTS", (4500,3800):"C64_RTS",
    (1300,3700):"C64_DTR", (4500,3700):"C64_DTR", (1300,3500):"C64_RXD", (1300,3400):"C64_RXD", (5900,3500):"C64_RXD",
    (1300,4100):"C64_CTS", (5900,3600):"C64_CTS", (1300,4200):"C64_DSR", (5900,3700):"C64_DSR",
    (1300,3900):"C64_DCD", (5900,3800):"C64_DCD", (1300,3800):"C64_RI", (5900,3900):"C64_RI",
    (4500,3400):"RS232_TXD", (8000,3600):"RS232_TXD", (4500,3500):"RS232_RTS", (8000,4000):"RS232_RTS",
    (4500,3600):"RS232_DTR", (8000,3700):"RS232_DTR", (4500,2900):"RS232_RXD", (8000,3500):"RS232_RXD",
    (4500,3000):"RS232_CTS", (8000,4100):"RS232_CTS", (4500,3100):"RS232_DSR", (8000,3900):"RS232_DSR",
    (4500,3200):"RS232_DCD", (8000,3400):"RS232_DCD", (4500,3300):"RS232_RI", (8000,4200):"RS232_RI",
    (2300,3400):"RAW_5V", (7000,1350):"RAW_5V", (7000,1650):"+5V", (5900,2800):"+5V", (5900,3100):"+5V", (5900,3200):"+5V", (5900,1450):"+5V",
    (2300,3300):"GND", (2300,4400):"GND", (1300,3300):"GND", (1300,4400):"GND", (5900,2900):"GND", (8000,3800):"GND",
    (4900,1750):"GND", (5400,1750):"GND", (5900,1750):"GND", (3900,1450):"C1_PLUS", (5900,2600):"C1_PLUS",
    (3900,1750):"C1_MINUS", (5900,3000):"C1_MINUS", (4400,1450):"C2_PLUS", (4500,2600):"C2_PLUS",
    (4400,1750):"C2_MINUS", (4500,2700):"C2_MINUS", (4900,1450):"VPLUS", (5900,2700):"VPLUS", (5400,1450):"VMINUS", (4500,2800):"VMINUS",
}

# Rebuild label block only when needed.
required = ['Text Label 1300 4300 0 50 ~ 0\nC64_TXD\n', 'Text Label 5900 3200 0 50 ~ 0\n+5V\n', 'NoConn ~ 5900 3300\n']
if not all(token in s for token in required):
    anchor = "Text Label 2300 3000 0 50 ~ 0\nC64_+5V\n"
    start = s.find(anchor)
    if start < 0:
        found = s.find("Text Label 1300 4300 0 50 ~ 0\nC64_TXD\n")
        if found < 0:
            raise SystemExit("ERROR: wiring anchor not found")
        start = found
    end = s.index("Wire Notes Line\n", start)
    block = "".join(f"Text Label {x} {y} 0 50 ~ 0\n{name}\n" for (x,y),name in labels.items())
    for x,y in [(2300,3500),(2300,3600),(2300,3700),(2300,3800),(2300,3900),(2300,4000),(2300,4100),(2300,4200),(2300,4300),(1300,4000),(5900,3400),(5900,3300)]:
        block += f"NoConn ~ {x} {y}\n"
    s = s[:start] + block + s[end:]

s = s.replace('Rev "M1.9"', 'Rev "M1.10"').replace('Comment3 "M1.9 MAX3243E 5V baseline"', 'Comment3 "M1.10 frozen footprint baseline"')
s = s.replace('FORCEON is tied high and FORCEOFF low for normal always-on operation.', 'FORCEON and FORCEOFF are tied high for normal always-on operation.')
p.write_text(s)
print("M1.10 legacy schematic electrical and footprint baseline normalized")
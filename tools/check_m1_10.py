#!/usr/bin/env python3
"""Static M1.10 audit for C64RS232 frozen physical parts and footprints."""
from pathlib import Path
import re, sys
FP=Path("hardware/C64RS232.pretty/C64_User_Port_Edge.kicad_mod"); J2FP=Path("hardware/C64RS232.pretty/TE_5747844-4.kicad_mod"); BOM=Path("hardware/BOM_M1.csv"); GATE=Path("hardware/M1_10_FOOTPRINT_GATE.md"); SCH=Path("hardware/C64RS232_M1.sch")
EXPECTED=[str(i) for i in range(1,13)]+list("ABCDEFHJKLMN"); PITCH=3.96

def fail(msg): print(f"M1.10 FAIL: {msg}",file=sys.stderr); raise SystemExit(1)
if not FP.is_file(): fail(f"missing footprint: {FP}")
text=FP.read_text(encoding="utf-8")
pads=re.findall(r'\(pad\s+"([^"]+)"\s+connect\s+(?:rect|roundrect)\s+\(at\s+([-0-9.]+)\s+([-0-9.]+)\)\s+\(size\s+([-0-9.]+)\s+([-0-9.]+)\)',text)
if len(pads)!=24: fail(f"expected 24 edge pads, found {len(pads)}")
names=[p[0] for p in pads]
if sorted(names)!=sorted(EXPECTED): fail(f"pad set mismatch: {names}")
by={n:(float(x),float(y),float(w),float(h)) for n,x,y,w,h in pads}
for side in ([str(i) for i in range(1,13)],list("ABCDEFHJKLMN")):
    xs=[by[n][0] for n in side]
    for a,b in zip(xs,xs[1:]):
        if abs((b-a)-PITCH)>1e-6: fail(f"bad pitch {b-a:.4f} mm")
if abs(by["12"][0]-by["1"][0]-43.56)>1e-6: fail("bad contact-centre span")
# Opposite-side fingers must occupy the same XY geometry on the PCB tongue.
for front,back in zip([str(i) for i in range(1,13)],list("ABCDEFHJKLMN")):
    if by[front]!=by[back]: fail(f"front/back finger geometry misaligned: {front}/{back}")
for n,(x,y,w,h) in by.items():
    if abs(y-3.81)>1e-6 or abs(w-2.8)>1e-6 or abs(h-7.62)>1e-6: fail(f"{n}: expected 2.8 x 7.62 mm finger from insertion edge")
if 'layers "F.Cu" "F.Mask"' not in text or 'layers "B.Cu" "B.Mask"' not in text: fail("both copper/mask sides required")
if "PCB EDGE / INSERTION" not in text: fail("PCB insertion-edge datum missing")
if "1.57 mm PCB NOMINAL" not in text: fail("nominal PCB thickness annotation missing")
for path in (J2FP,GATE,BOM,SCH):
    if not path.is_file(): fail(f"missing required file: {path}")
j2fp=J2FP.read_text(encoding="utf-8")
for required in ("5747844-4","2.7432","1.4224","12.4968","(drill 1.05)","(drill 3.18)"):
    if required not in j2fp: fail(f"J2 exact footprint missing drawing-derived datum: {required}")
gate=GATE.read_text(encoding="utf-8"); bom=BOM.read_text(encoding="utf-8"); sch=SCH.read_text(encoding="utf-8")
for required in ("5747844-4","1206L010/30WR","100 mA","250 mA","30 V","1.57 mm","2.74 mm","ENG_CD_5747844_P.pdf","25 V","X7R","0805"):
    if required not in gate: fail(f"gate document missing: {required}")
# Parse J2 instead of relying only on marker strings.
j2pads=re.findall(r'\(pad\s+"([^"]+)"\s+(thru_hole|np_thru_hole)\s+circle\s+\(at\s+([-0-9.]+)\s+([-0-9.]+)\).*?\(drill\s+([-0-9.]+)\)', j2fp)
sig={n:(kind,float(x),float(y),float(d)) for n,kind,x,y,d in j2pads if n.isdigit()}
if sorted(sig)!=[str(i) for i in range(1,10)]: fail(f"J2 signal pad set mismatch: {sorted(sig)}")
for n,(kind,x,y,d) in sig.items():
    if kind!="thru_hole" or abs(d-1.05)>1e-6: fail(f"J2 pad {n}: expected 1.05 mm plated drill")
for row in (["1","2","3","4","5"],["6","7","8","9"]):
    xs=[sig[n][1] for n in row]
    for a,b in zip(xs,xs[1:]):
        if abs((b-a)-2.7432)>1e-6: fail(f"J2 bad signal pitch: {b-a:.4f} mm")
if abs(sig["1"][2]+1.4224)>1e-6 or abs(sig["6"][2]-1.4224)>1e-6: fail("J2 row placement mismatch")
if abs((sig["6"][2]-sig["1"][2])-2.8448)>1e-6: fail("J2 row spacing mismatch")
if "Fuse:Fuse_1206_3216Metric_Pad1.42x1.75mm_HandSolder" not in sch: fail("F1 accepted 1206 land pattern missing")
if "1.45 mm × 1.80 mm" not in gate or "4.40 mm overall span" not in gate: fail("F1 manufacturer land-pattern verification missing from gate")

if "MAX3243EIPWR" not in bom: fail("BOM lost MAX3243EIPWR")
for required in ("TE Connectivity 5747844-4","Littelfuse 1206L010/30WR","47nF 25V X7R 0805","330nF 25V X7R 0805","100nF 25V X7R 0805"):
    if required not in bom: fail(f"BOM missing frozen M1.10 item: {required}")
assignments={"J1":"C64RS232:C64_User_Port_Edge","U1":"Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm","J2":"C64RS232:TE_5747844-4","F1":"Fuse:Fuse_1206_3216Metric_Pad1.42x1.75mm_HandSolder","C1":"Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder","C2":"Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder","C3":"Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder","C4":"Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder","C5":"Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder"}
for ref,footprint in assignments.items():
    pos=sch.find(f'F 0 "{ref}"'); end=sch.find('$EndComp',pos)
    if pos<0 or end<0: fail(f"component {ref} missing")
    if f'F 2 "{footprint}"' not in sch[pos:end]: fail(f"{ref} footprint not frozen to {footprint}")
for value in ("MAX3243EIPWR","5747844-4","1206L010/30WR"):
    if value not in sch: fail(f"schematic missing frozen value {value}")
print("M1.10 FOOTPRINT/MECHANICAL AUDIT PASS")
print("  J1: 24 aligned front/back fingers, 3.96 mm pitch, 2.8 x 7.62 mm mating fingers, 1.57 mm nominal PCB")
print("  U1/J2/F1/C1-C5: frozen footprint assignments present")
print("  C1-C5: 0805 X7R >=25 V BOM baseline frozen")
print("  F1: Littelfuse 1206L010/30WR ordering/electrical baseline frozen")
print("  J2: project-local TE_5747844-4 drawing-derived footprint assigned and audited")
print("NOTE: fabrication bevel/chamfer remains a PCB manufacturing specification, not copper-pad geometry.")
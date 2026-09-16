# M1.9 — TI MAX3243E verification

M1.9 locks the C64RS232 transceiver implementation to **Texas Instruments MAX3243EIPWR** (28-pin TSSOP/PW) before PCB footprint work.

## Source baseline

Manufacturer: Texas Instruments
Device family: MAX3243E
Orderable baseline: MAX3243EIPWR
Datasheet: SLLS657E, revised October 2022
Supply: C64 User Port nominal +5 V, protected by F1

## Verified electrical facts

- Supply range: 3 V to 5.5 V.
- Three RS-232 drivers and five RS-232 receivers match the required DTE signal set.
- MAX3243E supports up to 500 kbit/s; this is comfortably above expected C64 serial rates.
- 28-pin DB/DW/PW pinout matches the existing logical mapping: RIN1..5 pins 4..8, DOUT1..3 pins 9..11, DIN3..1 pins 12..14, ROUT5..1 pins 15..19, ROUT2B 20, INVALID 21, FORCEOFF 22, FORCEON 23, C1- 24, GND 25, VCC 26, V+ 27, C1+ 28; C2+ 1, C2- 2, V- 3.
- At 5 V ±0.5 V the datasheet capacitor table specifies C1=0.047 uF and C2/C3/C4=0.33 uF.
- A 0.1 uF local VCC bypass capacitor is retained as C5.
- FORCEOFF low powers off the ordinary drivers/receivers. Therefore the old FORCEOFF-to-GND freeze was incorrect.
- Normal operation with auto-powerdown disabled requires FORCEON=high and FORCEOFF=high. M1.9 ties both pins to protected +5 V.
- INVALID and ROUT2B are not required by the current C64 interface and remain NC.

## Layout implications

- Use the exact TSSOP-28 PW footprint for MAX3243EIPWR.
- Keep C1/C2 charge-pump loops short and place all charge-pump capacitors close to U1.
- Keep C5 immediately at VCC/GND.
- Keep RS-232-side routing separated cleanly from the C64 logic side and maintain a continuous ground reference where practical.

## Gate result

The previous M1.8d topology was electrically self-consistent but its FORCEOFF=GND choice would have commanded shutdown, and its 100 nF charge-pump values were not the TI 5 V baseline. M1.9 corrects both before PCB layout.

M1.9 is complete only when the regenerated native KiCad schematic passes exact netlist assertions and ERC with FORCEON/FORCEOFF both on +5 V and the revised capacitor values preserved.

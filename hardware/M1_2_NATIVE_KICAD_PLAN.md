# C64RS232 M1.2 — Native KiCad implementation plan

M1.2 converts the M1 electrical baseline into a native modern KiCad project suitable for ERC review and subsequent PCB layout.

## Required native files

- `C64RS232.kicad_pro`
- `C64RS232.kicad_sch`
- `C64RS232.kicad_pcb`
- project-local symbols/footprints where required

## Schematic requirements

1. Use explicit net labels for every C64 and RS-232 signal.
2. Represent the C64 User Port as a real edge-connector footprint with verified 3.96 mm / 0.156 in pitch.
3. Use a real orderable MAX3243 symbol and verify the exact package pinout against the selected manufacturer part.
4. Use real capacitor footprints and manufacturer-recommended charge-pump values.
5. Add the +5 V input protection device from the BOM.
6. Add power flags and explicit GND/+5 V power symbols.
7. Mark intentionally unused pins with no-connect markers.
8. Represent the DE-9 connector with the intended mechanical orientation.
9. Keep 9 VAC and RESET electrically isolated from the board power system.
10. Keep RXD available to both PB0 and FLAG2 on the C64 side.

## ERC gate

M1.2 is complete only when the native schematic opens without rescue-symbol warnings and ERC is clean or all remaining exceptions are explicitly documented and intentional.

## Footprint gate

Before PCB placement, verify:

- User Port edge connector pitch, contact geometry, board thickness and keying.
- MAX3243 package and pin numbering.
- DE-9 mechanical footprint and panel/board orientation.
- capacitor package sizes.
- fuse footprint.

## Manufacturing rule

No Gerbers are release artifacts at M1.2. Gerbers require completed PCB routing and DRC in M2.

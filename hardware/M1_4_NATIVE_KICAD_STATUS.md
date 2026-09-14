# C64RS232 M1.4 — Native KiCad status

## Gate

M1.4 requires a real native `C64RS232.kicad_sch`, verified by KiCad, with the frozen M1.1 connectivity represented by actual schematic objects and symbols.

The repository already contains the native project container `C64RS232.kicad_pro`, but the native schematic itself must not be fabricated as plain placeholder text. It must be produced and opened by KiCad before ERC can be claimed.

## Automated gate

`tools/check_kicad_native.sh` checks for the native schematic and, when `kicad-cli` is available, invokes schematic ERC.

Current status:

- Project file: PRESENT
- Native schematic: PENDING
- Native symbol/footprint verification: PENDING
- ERC: PENDING
- PCB layout: NOT STARTED
- DRC: NOT STARTED
- Manufacturing release: NOT READY

This deliberately prevents a text placeholder from being mistaken for a production KiCad design.

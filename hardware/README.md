# C64RS232 hardware

## M1 status

M1 establishes the electrical design for a manufacturable C64 User Port to RS-232 adapter.

### Core device

The baseline transceiver is **MAX3243** rather than MAX232. MAX3243 provides three drivers and five receivers, which allows the board to expose the complete C64 RS-232 signal set: TXD, RXD, RTS, CTS, DTR, DSR, DCD and RI. It operates from the C64's +5 V User Port supply and generates true RS-232 levels with an integrated charge pump.

### Interfaces

- J1: C64 User Port, 3.96 mm / 0.156 in edge connector.
- U1: MAX3243, 28-pin package.
- J2: DE-9 female, DTE pinout.

### Files

- `C64RS232_M1.sch` — KiCad legacy schematic baseline, intentionally kept simple so it can be opened/imported by modern KiCad.
- `C64RS232_M1-cache.lib` — embedded legacy symbol cache used by the schematic.
- `M1_NETLIST.md` — authoritative signal and pin mapping for M1.
- `BOM_M1.csv` — initial bill of materials.

### Important

The legacy schematic is an M1 baseline, not a manufacturing release. Modern KiCad should import it and save a native `.kicad_sch`. ERC/DRC, footprints, board mechanics, and final net connectivity must be completed before Gerbers are considered release-ready.

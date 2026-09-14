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

- `C64RS232_M1.sch` — KiCad legacy schematic baseline.
- `C64RS232_M1-cache.lib` — embedded legacy symbol cache.
- `M1_NETLIST.md` — M1 electrical design and signal mapping.
- `M1_1_CONNECTIONS.md` — authoritative M1.1 logical connection matrix.
- `BOM_M1.csv` — initial bill of materials.

## M1.1 status — connection freeze

The logical connectivity is now frozen before conversion to a native modern KiCad schematic. The M1.1 matrix explicitly defines every User Port, MAX3243 and DE-9 connection, the charge-pump network, enable controls and the protected +5 V entry.

### Important

The legacy schematic is **not yet a manufacturing release**. The next hardware step is to create the native `.kicad_sch`, assign verified footprints and run ERC. PCB routing and DRC follow after that gate. Do not manufacture from the current legacy schematic.

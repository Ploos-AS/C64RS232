# C64RS232 hardware

## M1 status

M1 establishes the electrical design for a manufacturable C64 User Port to RS-232 adapter.

### Core device

The baseline transceiver is **MAX3243** rather than MAX232. MAX3243 provides three drivers and five receivers, allowing the board to expose TXD, RXD, RTS, CTS, DTR, DSR, DCD and RI. It operates from the C64's +5 V User Port supply and generates true RS-232 levels with an integrated charge pump.

### Interfaces

- J1: C64 User Port, 3.96 mm / 0.156 in edge connector.
- U1: MAX3243, 28-pin package.
- J2: DE-9 female, DTE pinout.

### Native KiCad status

`C64RS232.kicad_pro` is now present as the native project container.

The M1 electrical design remains authoritative in:

- `M1_NETLIST.md`
- `M1_1_CONNECTIONS.md`
- `M1_2_NATIVE_KICAD_PLAN.md`
- `BOM_M1.csv`

### M1.3 gate

- native KiCad project container: **PASS**
- native `.kicad_sch`: **PENDING conversion/verification**
- exact orderable footprints: **PENDING verification**
- ERC: **PENDING**
- PCB: **PENDING**
- DRC: **PENDING**
- Gerbers: **NOT RELEASED**

The legacy schematic is **not a manufacturing release**. Do not manufacture from the current baseline. The native schematic must be created/imported and verified with the target KiCad version before PCB routing.

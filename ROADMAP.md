# C64RS232 Roadmap

C64RS232 is an open hardware and software project for connecting a Commodore 64 User Port to a conventional RS-232 interface, with a long-term goal of providing SLIP/IP networking.

## M0 — Architecture baseline — COMPLETE

- Define hardware/software boundaries.
- Target the C64 User Port as the native interface.
- Use a level-shifting RS-232 transceiver between the C64-side logic and DB9 RS-232.
- Keep the design suitable for manufacturable 2-layer PCBs and through-hole-friendly assembly where practical.
- Define a low-level C64 serial driver rather than requiring applications to manipulate CIA registers directly.
- Reserve the software architecture for future SLIP and IP networking.
- Define test and qualification strategy.

## M1 — Hardware schematic — IN PROGRESS

- KiCad project and schematic.
- User Port connector and signal mapping.
- RS-232 transceiver and charge-pump capacitors.
- Power decoupling and protection.
- DB9 interface.
- Optional status LEDs and configuration provisions.
- ERC clean.

### M1.1 — Logical connection freeze — COMPLETE

- Authoritative User Port → MAX3243 mapping defined.
- RXD/FLAG2 dual connection defined.
- MAX3243 → DE-9 DTE mapping defined.
- Charge-pump capacitor connections defined.
- FORCEON/FORCEOFF/unused-control handling defined.
- +5 V protection policy defined.
- 9 VAC explicitly excluded.

### M1.2 — Native KiCad schematic + ERC

- Convert the legacy baseline to native `.kicad_sch`.
- Assign exact manufacturer-verified footprints.
- Complete all physical net wiring.
- Add power flags and design-rule annotations as appropriate.
- Run ERC and resolve all intended warnings/errors.
- Freeze schematic before PCB placement.

## M2 — PCB layout

- 2-layer PCB.
- Manufacturable footprints.
- Routing and grounding review.
- Silkscreen pin/function labels.
- Mounting and enclosure considerations.
- DRC clean.
- Gerber and drill generation.

## M3 — C64 serial driver

- CIA-based serial I/O.
- Configurable baud rates.
- TX/RX buffering.
- Error/status reporting.
- Public driver/API interface.
- C64 test utility.

## M4 — Terminal and interoperability

- Terminal test program.
- Null-modem compatibility.
- Linux/macOS/Windows serial-side testing.
- Sustained transfer tests.

## M5 — SLIP

- SLIP framing and escaping.
- IP packet transport over the serial link.
- Host-side gateway tooling.
- C64-side packet interface.

## M6 — IP applications

- ICMP/ping test.
- UDP support.
- TCP support.
- Telnet/IRC/HTTP experiments.
- Integration candidates for retro BBS/network projects.

## M7 — PPP and advanced networking (optional)

- Evaluate PPP after SLIP is stable.
- Authentication/configuration where useful.
- Better interoperability with standard host networking stacks.

## Qualification

Hardware and C64 runtime qualification are deliberately kept separate from the implementation milestones. Final qualification will cover schematic/PCB checks, electrical loopback, serial interoperability, sustained transfers, and SLIP/IP operation on real hardware.
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

## M1 — Hardware schematic — COMPLETE

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

### M1.2–M1.8 — Native KiCad conversion and electrical net qualification — COMPLETE

- Legacy schematic converted to native KiCad.
- Physical net wiring generated and qualified.
- Frozen functional, power and charge-pump nets checked from exported KiCad netlists.
- ERC error gate enforced in GitHub Actions.

### M1.9 — MAX3243E datasheet/electrical freeze — COMPLETE

- TI MAX3243E 28-pin DB/DW/PW pinout verified.
- Normal/always-on FORCEON/FORCEOFF configuration qualified.
- 5 V charge-pump capacitor baseline verified.
- Exact functional and power/control/charge pin membership qualified.
- Frozen NC pins checked against named electrical nets.
- Native KiCad ERC: zero violations at qualification.

### M1.10 — Footprint and mechanical gate — COMPLETE

- Freeze exact orderable U1 package and KiCad footprint.
- Freeze capacitor footprints and electrical ratings.
- Create and dimensionally verify the C64 User Port edge footprint.
- Select exact DE-9 female PCB connector and matching footprint/orientation.
- Select exact 100 mA resettable PTC and footprint.
- Add automated footprint audit to GitHub Actions.
- Assign all frozen footprints in the native schematic.

M1.10 passed the enforced GitHub Actions qualification gate. M1 is complete. No Gerbers were released from M1.

## M2 — PCB layout — IN PROGRESS

- 2-layer PCB.
- Manufacturable footprints.
- Routing and grounding review.
- Silkscreen pin/function labels.
- Mounting and enclosure considerations.
- DRC clean.
- Gerber and drill generation.

### M2.1 — Mechanical placement baseline — COMPLETE

- Native KiCad PCB with all nine frozen footprints and 75 physical pads.
- J1 card-edge placement corrected and centered inside the board outline.
- J2, U1, PTC and capacitor placement baseline established.
- Closed two-layer board outline qualified in CI.

### M2.2 — Power and charge-pump routing — COMPLETE

- RAW_5V routed from User Port through the resettable PTC.
- Protected +5 V routed to MAX3243E and bypass capacitor.
- C1/C2 charge-pump and V+/V- capacitor nets physically routed.
- Local GND/bypass copper present.
- Physical pad-net and non-floating-copper gates pass.

### M2.3 — Functional signal routing and GND plane — COMPLETE

- All eight C64-side functional serial/control nets physically routed.
- Both User Port RXD contacts B/C retained on the shared RXD net.
- All eight RS-232-side functional nets physically routed to the DE-9.
- Board-wide B.Cu GND zone restored and qualified.
- GitHub Actions run #158 passed the complete M1 regression plus M2.1/M2.2/M2.3 gates.

### M2.4 — Silkscreen, mechanical and fabrication review — NEXT

- Review connector accessibility, board outline and keep-outs.
- Verify TE 5747844-4 boardlock holes and female DE-9 pin orientation against the official manufacturer drawing.
- Add final silkscreen labels and polarity/function markings.
- Review C64 card-edge finish/bevel manufacturing requirements.
- Review routing geometry and clearances before fabrication.

### M2.5 — Final DRC and fabrication package

- Run native KiCad PCB DRC as a blocking CI gate.
- Resolve all layout violations and unrouted connections.
- Generate Gerber and drill outputs.
- Validate fabrication outputs and publish the qualified hardware package.

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

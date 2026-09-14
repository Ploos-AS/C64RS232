# C64RS232 M1 electrical netlist

## Design choice

M1 uses a **MAX3243** RS-232 transceiver. It provides 3 RS-232 drivers and 5 RS-232 receivers, matching the full C64 User Port serial/modem-control signal set used by the traditional C64 RS-232 software convention. The device accepts a 3.0–5.5 V supply and provides true RS-232 levels. It also includes ±15 kV HBM protection on the RS-232 bus pins.

## C64 User Port → MAX3243

| C64 User Port | C64 signal | MAX3243 | Direction |
|---|---|---|---|
| M | PA2 / TXD | T1IN pin 14 | C64 → RS-232 |
| D | PB1 / RTS | T2IN pin 13 | C64 → RS-232 |
| E | PB2 / DTR | T3IN pin 12 | C64 → RS-232 |
| C | PB0 / RXD | R1OUT pin 19 | RS-232 → C64 |
| B + C | FLAG2 + PB0 / RXD | R1OUT pin 19 | RX interrupt/data |
| K | PB6 / CTS | R2OUT pin 18 | RS-232 → C64 |
| L | PB7 / DSR | R3OUT pin 17 | RS-232 → C64 |
| H | PB4 / DCD | R4OUT pin 16 | RS-232 → C64 |
| F | PB3 / RI | R5OUT pin 15 | RS-232 → C64 |
| 2 | +5 V | VCC pin 26 | Power |
| A/N | GND | GND pin 25 | Ground |

The RXD signal is intentionally connected to **both FLAG2 (B) and PB0 (C)**, matching the established C64 RS-232 convention.

## MAX3243 charge pump

- C1: 100 nF between C1+ pin 28 and C1− pin 24.
- C2: 100 nF between C2+ pin 1 and C2− pin 2.
- C3: 100 nF between V+ pin 27 and GND pin 25.
- C4: 100 nF between V− pin 3 and GND pin 25.
- C5: 100 nF local VCC-to-GND bypass capacitor.

## AutoShutdown control

- FORCEON pin 23 → VCC.
- FORCEOFF pin 22 → GND.
- INVALID pin 21 → NC for M1.
- R2OUTB pin 20 → NC for M1; standard R2OUT is used for CTS.

This keeps the transceiver enabled for predictable retro-computer operation.

## MAX3243 → DE-9 DTE

| MAX3243 | RS-232 signal | DE-9 pin |
|---|---|---:|
| T1OUT pin 9 | TXD | 3 |
| T2OUT pin 10 | RTS | 7 |
| T3OUT pin 11 | DTR | 4 |
| R1IN pin 4 | RXD | 2 |
| R2IN pin 5 | CTS | 8 |
| R3IN pin 6 | DSR | 6 |
| R4IN pin 7 | DCD | 1 |
| R5IN pin 8 | RI | 9 |
| GND pin 25 | GND | 5 |

The DE-9 is treated as a **DTE-style port**, making the board suitable for a conventional straight-through connection to a modem/DCE and a null-modem cable for DTE-to-DTE links.

## C64 connector power policy

Only +5 V and ground are consumed from the User Port. The following are intentionally left unconnected:

- pin 3 RESET
- pins 4/5/6/7/8/9
- pins 10/11 9 VAC
- PB5 / J

No 9 VAC is brought onto the PCB power system.

## Protection

M1 relies on the MAX3243's integrated RS-232 input protection. A dedicated external TVS network can be added in a later hardware revision if testing shows a benefit. The C64 +5 V input should have a resettable protection element in the final PCB implementation.

## Qualification prerequisites

Before manufacturing:

1. ERC-clean KiCad schematic.
2. Verify MAX3243 package/footprint against the selected orderable part.
3. Verify User Port edge-connector pitch and board thickness.
4. Verify DE-9 mechanical orientation and female/male choice.
5. Electrical loopback with a real RS-232 adapter.
6. C64 runtime tests at supported baud rates.

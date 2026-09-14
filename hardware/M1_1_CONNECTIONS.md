# C64RS232 M1.1 connection matrix

M1.1 freezes the logical electrical connectivity before the schematic is converted to a native modern KiCad schematic and PCB.

## C64 User Port to U1

| User Port | Signal | U1 pin | Net |
|---|---|---:|---|
| M | PA2 / TXD | 14 T1IN | C64_TXD |
| D | PB1 / RTS | 13 T2IN | C64_RTS |
| E | PB2 / DTR | 12 T3IN | C64_DTR |
| C | PB0 / RXD | 19 R1OUT | C64_RXD |
| B | FLAG2 / RX interrupt | 19 R1OUT | C64_RXD |
| K | PB6 / CTS | 18 R2OUT | C64_CTS |
| L | PB7 / DSR | 17 R3OUT | C64_DSR |
| H | PB4 / DCD | 16 R4OUT | C64_DCD |
| F | PB3 / RI | 15 R5OUT | C64_RI |
| 2 | +5 V | 26 VCC | +5V |
| A, N | GND | 25 GND | GND |

PB5 (J), RESET, 9 VAC and unused User Port pins remain NC.

## U1 to DE-9

| U1 pin | Signal | DE-9 pin | Net |
|---:|---|---:|---|
| 9 T1OUT | RS-232 TXD | 3 | RS232_TXD |
| 10 T2OUT | RS-232 RTS | 7 | RS232_RTS |
| 11 T3OUT | RS-232 DTR | 4 | RS232_DTR |
| 4 R1IN | RS-232 RXD | 2 | RS232_RXD |
| 5 R2IN | RS-232 CTS | 8 | RS232_CTS |
| 6 R3IN | RS-232 DSR | 6 | RS232_DSR |
| 7 R4IN | RS-232 DCD | 1 | RS232_DCD |
| 8 R5IN | RS-232 RI | 9 | RS232_RI |
| 25 GND | Signal ground | 5 | GND |

## Charge pump and control

- C1 100 nF: U1 pin 28 C1+ to pin 24 C1-.
- C2 100 nF: U1 pin 1 C2+ to pin 2 C2-.
- C3 100 nF: U1 pin 27 V+ to GND.
- C4 100 nF: U1 pin 3 V- to GND.
- C5 100 nF: U1 pin 26 VCC to GND, placed immediately at U1.
- U1 pin 23 FORCEON to +5V.
- U1 pin 22 FORCEOFF to GND.
- U1 pin 21 INVALID NC.
- U1 pin 20 R2OUTB NC.

## Power entry

User Port +5 V shall feed a resettable fuse/protection element before U1 VCC. GND is common between the User Port, U1 and DE-9.

The 9 VAC pins are deliberately excluded from the power system.

## Mechanical baseline

- J1: C64 User Port edge connector, 3.96 mm / 0.156 in pitch.
- U1: selected MAX3243 orderable package; footprint must be verified against the exact manufacturer part before PCB release.
- J2: DE-9 female, DTE orientation.
- 2-layer PCB target.

## M1.1 acceptance criteria

1. Every functional User Port signal has exactly one defined logical net.
2. RXD is shared by PB0 and FLAG2.
3. All eight conventional RS-232 signals plus ground reach the DE-9.
4. Charge-pump capacitors and U1 control pins are explicitly defined.
5. No 9 VAC enters the PCB power domain.
6. The matrix is treated as authoritative when producing the native `.kicad_sch` and PCB.

This document does not claim ERC/DRC or manufacturing qualification; those remain later gates.
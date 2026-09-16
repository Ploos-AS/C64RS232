# C64RS232 M1 connection matrix

This document freezes the logical electrical connectivity for the native KiCad schematic and PCB. M1.9 additionally locks the RS-232 transceiver baseline to the TI MAX3243E at the C64 nominal 5 V supply.

## C64 User Port to U1

| User Port | Signal | U1 pin | Net |
|---|---|---:|---|
| M | PA2 / TXD | 14 DIN1 | C64_TXD |
| D | PB1 / RTS | 13 DIN2 | C64_RTS |
| E | PB2 / DTR | 12 DIN3 | C64_DTR |
| C | PB0 / RXD | 19 ROUT1 | C64_RXD |
| B | FLAG2 / RX interrupt | 19 ROUT1 | C64_RXD |
| K | PB6 / CTS | 18 ROUT2 | C64_CTS |
| L | PB7 / DSR | 17 ROUT3 | C64_DSR |
| H | PB4 / DCD | 16 ROUT4 | C64_DCD |
| F | PB3 / RI | 15 ROUT5 | C64_RI |
| 2 | +5 V | 26 VCC | +5V through F1 |
| A, N | GND | 25 GND | GND |

PB5 (J), RESET, 9 VAC and unused User Port pins remain NC.

## U1 to DE-9

| U1 pin | Signal | DE-9 pin | Net |
|---:|---|---:|---|
| 9 DOUT1 | RS-232 TXD | 3 | RS232_TXD |
| 10 DOUT2 | RS-232 RTS | 7 | RS232_RTS |
| 11 DOUT3 | RS-232 DTR | 4 | RS232_DTR |
| 4 RIN1 | RS-232 RXD | 2 | RS232_RXD |
| 5 RIN2 | RS-232 CTS | 8 | RS232_CTS |
| 6 RIN3 | RS-232 DSR | 6 | RS232_DSR |
| 7 RIN4 | RS-232 DCD | 1 | RS232_DCD |
| 8 RIN5 | RS-232 RI | 9 | RS232_RI |
| 25 GND | Signal ground | 5 | GND |

## Charge pump and control — TI MAX3243E, 5 V baseline

The C64 User Port supplies nominal +5 V. For the TI MAX3243E at 5 V ±0.5 V the datasheet test/recommended values are used:

- C1 47 nF: U1 pin 28 C1+ to pin 24 C1-.
- C2 330 nF: U1 pin 1 C2+ to pin 2 C2-.
- C3 330 nF: U1 pin 27 V+ to GND.
- C4 330 nF: U1 pin 3 V- to GND.
- C5 100 nF ceramic bypass: U1 pin 26 VCC to GND, placed immediately at U1.
- U1 pin 23 FORCEON to protected +5V.
- U1 pin 22 FORCEOFF to protected +5V.
- U1 pin 21 INVALID NC.
- U1 pin 20 ROUT2B NC.

Both FORCEON and FORCEOFF are high so auto-powerdown is disabled and the serial interface remains in normal operation. FORCEOFF must not be tied low: low explicitly powers off the normal drivers/receivers.

## Power entry

User Port +5 V feeds resettable fuse/protection F1 before U1 VCC and both control inputs. GND is common between the User Port, U1 and DE-9. The 9 VAC pins are deliberately excluded.

## Mechanical baseline

- J1: C64 User Port edge connector, 3.96 mm / 0.156 in pitch; exact edge geometry remains a PCB footprint gate.
- U1: TI MAX3243EIPWR, active 28-pin TSSOP (PW), industrial -40°C to 85°C baseline.
- J2: DE-9 female, DTE orientation; exact PCB connector orientation remains a footprint gate.
- 2-layer PCB target.

## M1.9 acceptance criteria

1. Every functional User Port and DE-9 signal has the frozen exact U1 pin membership.
2. RXD is shared by PB0 and FLAG2.
3. Charge-pump values match the TI MAX3243E 5 V baseline.
4. FORCEON and FORCEOFF are both high for normal/always-on operation.
5. No 9 VAC enters the PCB power domain.
6. Exported netlist and ERC qualification enforce the frozen topology.
7. Exact physical footprints remain gated before M2 PCB routing.

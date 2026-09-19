# C64RS232 M2.3 — Signal routing and GND plane

## Routing contract

The functional signal set is frozen by the M1 schematic:

- C64 side: TXD, RXD, RTS, CTS, DTR, DSR, DCD, RI
- RS-232 side: TXD, RXD, RTS, CTS, DTR, DSR, DCD, RI

Routing rules:

1. Keep C64 logic-side traces between J1 and U1 on the C64 side of the board where practical.
2. Keep RS-232-side traces between U1 and J2 on the RS-232 side.
3. Avoid unnecessary parallel runs between unrelated RS-232 signals.
4. Keep the +5 V and charge-pump loops from M2.2 compact and do not route functional signals through those loops.
5. Use B.Cu primarily for controlled crossovers/return continuity; prefer F.Cu for short point-to-point signal runs.
6. Establish a substantially continuous B.Cu GND plane after signal routing, with no unnecessary split under the signal path.
7. Do not route the J1 9 VAC contacts into the circuit.
8. M2.3 is not complete until every functional signal has a routed copper path and the resulting PCB passes the KiCad DRC gate.

## Signal inventory

C64_TXD, C64_RXD, C64_RTS, C64_CTS, C64_DTR, C64_DSR, C64_DCD, C64_RI

RS232_TXD, RS232_RXD, RS232_RTS, RS232_CTS, RS232_DTR, RS232_DSR, RS232_DCD, RS232_RI

## Status

M2.3 routing specification established. Actual copper routing and GND-zone completion remain in progress.

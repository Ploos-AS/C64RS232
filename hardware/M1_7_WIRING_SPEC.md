# C64RS232 M1.7 electrical wiring contract

M1.7 turns the M1.1 logical connection freeze into an explicit implementation contract for the native KiCad schematic. This document is intentionally separate from qualification: M1.8 will verify the exported netlist and ERC results.

## C64-side nets

- `C64_TXD`: J1 M / PA2 to U1 pin 14 / T1IN.
- `C64_RTS`: J1 D / PB1 to U1 pin 13 / T2IN.
- `C64_DTR`: J1 E / PB2 to U1 pin 12 / T3IN.
- `C64_RXD`: U1 pin 19 / R1OUT to both J1 C / PB0 and J1 B / FLAG2.
- `C64_CTS`: U1 pin 18 / R2OUT to J1 K / PB6.
- `C64_DSR`: U1 pin 17 / R3OUT to J1 L / PB7.
- `C64_DCD`: U1 pin 16 / R4OUT to J1 H / PB4.
- `C64_RI`: U1 pin 15 / R5OUT to J1 F / PB3.

## RS-232-side nets

- `RS232_TXD`: U1 pin 9 / T1OUT to J2 pin 3 / TXD.
- `RS232_RTS`: U1 pin 10 / T2OUT to J2 pin 7 / RTS.
- `RS232_DTR`: U1 pin 11 / T3OUT to J2 pin 4 / DTR.
- `RS232_RXD`: J2 pin 2 / RXD to U1 pin 4 / R1IN.
- `RS232_CTS`: J2 pin 8 / CTS to U1 pin 5 / R2IN.
- `RS232_DSR`: J2 pin 6 / DSR to U1 pin 6 / R3IN.
- `RS232_DCD`: J2 pin 1 / DCD to U1 pin 7 / R4IN.
- `RS232_RI`: J2 pin 9 / RI to U1 pin 8 / R5IN.
- `GND`: J2 pin 5 to the common board ground.

## Power and MAX3243 charge pump

- User Port +5 V enters a protected `+5V` rail before U1 pin 26 / VCC.
- J1 A, J1 N, U1 pin 25 and J2 pin 5 share `GND`.
- C1: U1 pin 28 / C1+ to U1 pin 24 / C1-.
- C2: U1 pin 1 / C2+ to U1 pin 2 / C2-.
- C3: U1 pin 27 / V+ to GND.
- C4: U1 pin 3 / V- to GND.
- C5: U1 pin 26 / VCC to GND and physically close to U1.
- U1 pin 23 / FORCEON is tied to +5V.
- U1 pin 22 / FORCEOFF is tied to GND.

The capacitor values and FORCEON/FORCEOFF operating state remain subject to final verification against the exact selected MAX3243 manufacturer part before manufacturing release.

## Intentional no-connects

- U1 pin 20 / R2OUTB.
- U1 pin 21 / INVALID.
- J1 J / PB5.
- User Port RESET and unused serial-bus pins.
- User Port 9 VAC pins 10 and 11. They must never enter the board power domain.

## Implementation rules

1. TTL/C64 nets and RS-232 nets remain distinct across U1; labels must not accidentally short the two voltage domains.
2. `C64_RXD` must contain exactly U1 R1OUT, J1 PB0 and J1 FLAG2.
3. Every conventional DE-9 signal plus signal ground must terminate at the intended MAX3243 channel.
4. All unused pins must be explicitly marked no-connect where appropriate so ERC findings are intentional rather than ambiguous.
5. The native `hardware/C64RS232_M1.kicad_sch` is the implementation target. The legacy `.sch` remains historical conversion input and must not silently overwrite newer native electrical work.

## M1.7 exit gate

M1.7 is complete only when the native schematic implements every connection above and exports a netlist matching this contract. An ERC-clean result alone is not sufficient.

M1.8 will add machine-readable netlist assertions and classify/fix remaining ERC findings before the footprint/geometry freeze.
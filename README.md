# C64RS232

Open hardware and software project for connecting a Commodore 64 User Port to a conventional RS-232 interface.

## Goals

- Manufacturable KiCad PCB.
- C64 User Port as the native host interface.
- Standard RS-232 electrical interface, suitable for a DB9 connector.
- C64-side serial driver/API so applications do not need to manipulate CIA registers directly.
- Terminal and interoperability tooling.
- Future SLIP/IP networking over the serial link.
- Optional future PPP support after SLIP is established.

## Project status

**M0 — Architecture baseline: complete**

The project now has a defined hardware/software boundary and implementation roadmap. Hardware implementation, driver implementation, and networking are intentionally separated from final qualification.

See [ROADMAP.md](ROADMAP.md).

## Planned architecture

```text
C64 application
      |
      v
C64RS232 API / driver
      |
      v
CIA-based serial I/O
      |
      v
C64 User Port
      |
      v
RS-232 transceiver
      |
      v
DB9 RS-232
      |
      v
Host serial adapter / gateway
      |
      v
SLIP / IP (future)
```

## Hardware

The hardware target is a simple, robust 2-layer board using a dedicated RS-232 level-transceiver and charge-pump capacitors. Through-hole-friendly parts will be preferred where practical for easy assembly and repair.

## Software

The software stack will provide:

- low-level C64 serial I/O;
- configurable baud rates;
- buffering and status/error handling;
- terminal interoperability;
- SLIP framing and IP transport as a later milestone.

## Qualification

Qualification will cover schematic/PCB ERC/DRC, electrical loopback, real C64 serial interoperability, sustained transfers, and eventual SLIP/IP operation on physical hardware.

## License

License to be selected during the implementation baseline.
# C64RS232 M2 — PCB placement baseline

## Board concept

Target a compact 2-layer board with the C64 User Port connector on one edge and the DE-9 RS-232 connector on the opposite/accessible edge.

## Placement zones

```text
+------------------------------------------------+
| C64 USER PORT                                  |
| J1                                             |
|                                                |
|   F1       U1 MAX3243       C1..C5            |
|                                                |
|                                                |
|                              J2 DE-9           |
+------------------------------------------------+
```

### Placement rules

- Keep U1 close to the User Port signal entry and the charge-pump capacitors close to U1.
- Keep C5 immediately adjacent to U1 VCC/GND.
- Keep the +5 V fuse close to the User Port power entry.
- Keep RS-232 traces grouped between U1 and J2.
- Keep the C64 low-voltage signal region physically separated from the DE-9 cable interface where practical.
- Prefer a continuous ground plane on the bottom layer.
- Avoid routing high-current or noisy paths through the C64 signal return region.
- Provide mounting holes only after the actual User Port and DE-9 mechanical constraints are verified.

## Status

This is a placement baseline only. Exact board dimensions, footprints, mounting holes and routing are not manufacturing-qualified until M2 DRC/mechanical review.

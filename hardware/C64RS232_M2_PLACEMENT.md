# C64RS232 M2 — PCB placement baseline

## M2.1 — Mechanical placement freeze — COMPLETE

M2 starts from the M1.10-qualified footprints. The first PCB step is deliberately mechanical: freeze the board coordinate system, connector edges and component zones before routing.

## Board coordinate system

Use J1 as the primary datum:

- J1 C64 User Port insertion edge is the board mating edge and mechanical X-axis datum.
- J1 contact row remains aligned with the board edge; do not move individual fingers.
- PCB thickness remains 1.57 mm nominal.
- J2 is placed on the opposite accessible board edge with its footprint PCB-edge datum coincident with that edge.
- Board outline must not intrude into either connector's mating/keepout region.
- Final X/Y board dimensions remain provisional until J1/J2 placement has been reviewed in KiCad.

## Placement zones

```text
 C64 mating edge / J1 insertion edge
 v
 +------------------------------------------------+
 | J1: C64 USER PORT EDGE                         |
 |                                                |
 | F1        C64-side signals                     |
 |                                                |
 |              U1 MAX3243E                       |
 |              C1 C2 C3 C4 C5                    |
 |                                                |
 |                         RS-232-side signals     |
 |                                      J2 DE-9   |
 +----------------------------------------|-------+
                                          ^
                                  J2 connector edge
```

## Frozen placement constraints

1. **J1 is the primary mechanical anchor.** Its qualified 3.96 mm pitch, 2.8 × 7.62 mm fingers and front/back alignment must not be altered during PCB layout.
2. **F1 is first on the +5 V path.** Place it immediately after the J1 +5 V contact, before the protected `+5V` rail fans out.
3. **U1 remains central and compact.** Keep the MAX3243E away from the exposed card-edge fingers while minimizing both C64-side and RS-232-side trace lengths.
4. **C1–C4 form the charge-pump cluster.** Place them immediately around the corresponding U1 charge-pump pins; avoid long loops.
5. **C5 is the local bypass.** Place it directly between the U1 VCC/GND region with the shortest practical loop.
6. **J2 is the secondary mechanical anchor.** Its project-local `TE_5747844-4` footprint and PCB-edge datum define the opposite connector edge.
7. **Grounding:** target a substantially continuous B.Cu GND plane. Avoid unnecessary splits or long return detours.
8. **Signal zoning:** keep C64 logic-level routing on the J1/U1 side and RS-232-level routing on the U1/J2 side where practical.
9. **9 VAC:** J1's 9 VAC contacts remain physically present but must have no routed copper into the circuit.
10. **Mounting holes:** none are frozen yet. Add them only if the completed connector/board mechanics leave a justified location.

## M2.1 qualification gate

M2.1 can be marked complete when:

- a native `C64RS232.kicad_pcb` exists;
- all frozen M1.10 footprints are present exactly once;
- J1 and J2 are placed as board-edge mechanical anchors;
- a closed `Edge.Cuts` outline exists;
- the board is 2-layer;
- footprint assignment has not regressed from M1.10;
- unrouted nets are acceptable at this stage, but PCB DRC must not report footprint/board-outline structural errors;
- an automated M2.1 checker is present in CI.

No Gerbers are released from M2.1.

## Later M2 gates

- **M2.2:** component placement and charge-pump/power routing.
- **M2.3:** signal routing and GND plane.
- **M2.4:** silkscreen, mechanical/fabrication review and manufacturer card-edge requirements.
- **M2.5:** final DRC, Gerber/drill generation and fabrication-package qualification.

## Status

M2.1 passed the enforced GitHub Actions structural qualification gate in run #104. The native PCB baseline has 2 copper layers, 1.57 mm nominal thickness, all nine frozen footprints exactly once, a closed provisional Edge.Cuts outline, and the J1/J2 mechanical anchors. No Gerbers are released from M2.1.\n\n## M2.2 — Component placement and charge-pump/power routing — COMPLETE\n\nM2.2 passed the enforced GitHub Actions power/charge-pump qualification gate in run #111. The protected power spine, local bypass and charge-pump copper baseline are present; functional C64/RS-232 signal routing remains deferred to M2.3.\n\n## M2.3 — Signal routing and GND plane — IN PROGRESS\n\nM2.2 now owns refinement of the component coordinates plus the protected +5 V, GND/bypass and MAX3243E charge-pump routing. Final board dimensions remain provisional until the later mechanical/fabrication review.

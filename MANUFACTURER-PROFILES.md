# PCB Manufacturer Profiles

These profiles translate the Ploos-AS maker-friendly hardware standard into practical ordering defaults. They are conveniences, not vendor requirements.

Always use the fabrication requirements of the qualified hardware revision when they differ from these defaults.

## Common maker-friendly baseline

For boards that do not document an exception:

- Layers: 2
- Material: FR-4
- Finished thickness: 1.6 mm
- Copper: 1 oz outer layers
- Surface finish: lead-free HASL by default; ENIG is acceptable when technically useful
- Solder mask: manufacturer standard
- Silkscreen: manufacturer standard
- Minimum track/space target: 0.20 / 0.20 mm or more generous
- Minimum finished drill target: 0.30 mm or larger
- Standard plated through-holes and vias
- No blind/buried vias
- No via-in-pad unless explicitly required
- No controlled impedance unless explicitly required
- Panelization: not required unless documented by the project
- Electrical test: enabled when offered as a normal fabrication option

Board-specific dimensions, layer count, stack-up, impedance, copper weight, finish, castellations, edge connectors, assembly requirements, and other exceptions must come from the qualified release documentation.

## PCBWay profile

Use the common maker-friendly baseline unless the released board specifies otherwise.

Do not select advanced process options merely because they are available. If a PCBWay shared project is published, its settings must match the exact qualified hardware revision and release manufacturing package.

Record any PCBWay-specific settings that affect electrical or mechanical correctness next to the project's direct ordering link in ORDERING.md.

## JLCPCB profile

Use the common maker-friendly baseline unless the released board specifies otherwise.

For assembled boards, verify the BOM and placement data against the exact qualified revision before publishing an assembly/order link. Manufacturer part substitutions must not silently change the reference design.

Record any JLCPCB-specific fabrication or assembly settings that affect correctness next to the project's direct ordering link in ORDERING.md.

## OSH Park profile

OSH Park may use service-defined fabrication parameters rather than the generic baseline. A board should only be published as a shared project after confirming that the qualified design is compatible with the selected OSH Park service.

The shared project must correspond to the exact qualified hardware revision.

Document any meaningful differences from the project's generic manufacturing requirements.

## Advanced boards

Projects such as FPGA, high-speed, or SBC designs may require four or more copper layers, controlled impedance, special stack-ups, smaller geometries, or other advanced fabrication.

Such requirements are permitted, but they must be:

1. technically justified;
2. documented in the project;
3. reproducible without relying on undocumented manufacturer defaults;
4. represented in the qualified manufacturing release;
5. reviewed for availability from more than one manufacturer where practical.

Maker-friendly for an advanced board means minimizing and isolating unavoidable complexity rather than pretending that a simple two-layer process is sufficient.

## Release validation

Before publishing a manufacturer-specific ordering link, verify:

- exact board revision and Git commit/tag;
- manufacturing qualification PASS;
- Gerber and drill files match the release;
- BOM/CPL match the release when assembly is offered;
- board thickness and layer count;
- copper weight;
- surface finish where electrically important;
- any impedance or stack-up requirements;
- special mechanical requirements;
- manufacturer preview/orientation;
- affiliate/referral/sponsorship disclosure.

The vendor-neutral manufacturing ZIP remains the canonical fabrication artifact.

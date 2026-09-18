# Maker-Friendly Hardware Standard

Ploos-AS open-hardware projects should be practical to build, understand, modify, repair, and reproduce by individual makers.

The default design priority is **maker friendly first, cost second**. Projects may deviate where their technical requirements demand it, but deviations should be documented rather than silently becoming requirements.

## PCB defaults

Unless the design requires otherwise, prefer:

- two-layer PCBs;
- standard 1.6 mm FR-4;
- standard 1 oz copper;
- common fabrication capabilities available from multiple PCB manufacturers;
- conservative trace widths, clearances, vias, and annular rings rather than manufacturer-limit geometries;
- board dimensions and construction that do not unnecessarily increase fabrication cost.

Do not make a design dependent on one PCB manufacturer's proprietary process when a broadly supported alternative is practical.

## Components

Component and BOM selection also follows [COMPONENT-POLICY.md](COMPONENT-POLICY.md).

Prefer components that are:

- actively available from multiple distributors or have documented substitutes;
- easy for hobbyists to identify and source;
- hand-solderable where practical;
- available in through-hole packages where this materially improves accessibility, learning, repairability, or socketing;
- otherwise available in reasonably maker-friendly SMD packages.

Avoid BGA, very fine-pitch packages, blind/buried vias, via-in-pad, controlled impedance, exotic stack-ups, and similarly specialized processes unless the project genuinely requires them.

When a specialized component or process is necessary, document why and provide enough information for reproduction.

## Assembly and repair

Where practical:

- use sockets for components that are expensive, programmable, failure-prone, frequently replaced, or educationally useful to remove;
- provide accessible test points for important power rails, clocks, reset, buses, and diagnostic signals;
- label connectors, polarity, pin 1, jumpers, switches, and important test points on the silkscreen;
- avoid placing serviceable parts where they become inaccessible after normal assembly;
- design for ordinary soldering, rework, probing, and fault finding;
- use standard connectors and fasteners when practical.

## Documentation

A released board should provide enough information for a maker to reproduce and troubleshoot it without access to private project knowledge.

As applicable, provide:

- schematic;
- PCB source;
- manufacturing package;
- BOM with manufacturer part numbers or useful specifications;
- assembly notes;
- connector and jumper documentation;
- programming/flashing instructions;
- test points and expected measurements;
- bring-up procedure;
- troubleshooting information;
- known substitutions and alternatives.

## Manufacturer neutrality

A maker must be able to take the released manufacturing package to a suitable manufacturer of their choice.

Manufacturer-specific ordering profiles are conveniences. They must not replace the vendor-neutral fabrication data or become undocumented design requirements.

## Exceptions

Technical requirements take precedence when the maker-friendly defaults would prevent the project from meeting its purpose. Examples may include FPGA memory routing, high-speed interfaces, dense form factors, or unavailable through-hole equivalents.

Document significant exceptions in the project's hardware or manufacturing documentation, including the reason and any impact on home assembly or repair.

## Qualification

Automated CI should check maker-friendly requirements that can be determined reliably from design files. Human-review requirements remain documented checklist items.

A manufacturing qualification passing does not by itself mean that every maker-friendly preference has been met; project-specific exceptions and manual review remain part of hardware release qualification.

# Manufacturing

This project is open hardware. You may manufacture the hardware yourself or use any suitable PCB manufacturer. Ploos AS does not require a particular manufacturer.

## Policy

Ploos-AS hardware projects follow these rules:

- Released hardware must remain vendor-neutral.
- Manufacturing source files must be available independently of any ordering service.
- When direct ordering links are offered, we aim to provide at least two manufacturers and preferably three.
- Referral, affiliate, shared-project, or sponsored links must be clearly disclosed.
- A commercial relationship with a manufacturer does not make that manufacturer the exclusive or required supplier.
- Release manufacturing files, rather than an arbitrary development snapshot, should be used for production.

## Manufacturing package

For hardware revisions that are ready for fabrication, the corresponding release should provide a manufacturing package containing the applicable files:

- Gerber fabrication files
- drill files
- bill of materials (BOM)
- component placement / pick-and-place (CPL) files when assembly is supported
- fabrication and assembly notes
- schematic and relevant documentation
- checksums
- the corresponding KiCad source remains available in the repository

A typical release artifact is named:

```text
<project>-v<version>-manufacturing.zip
```

The exact contents depend on the project and hardware revision. A release must not imply that unqualified hardware is production-ready.

## CI qualification

The repository's `.github/workflows/manufacturing.yml` is the canonical manufacturing-package gate. A hardware release is considered package-ready only when that workflow passes for the release revision.

The workflow intentionally fails if no KiCad PCB is present or if more than one PCB is found without project-specific board selection. This prevents an ambiguous or incomplete development tree from being presented as production-ready.

A successful run validates DRC and produces Gerber/drill data, BOM when a matching schematic is available, CPL placement data, documentation, SHA-256 checksums, and a versioned manufacturing ZIP artifact.

For tagged hardware releases, a successful qualification run also publishes the versioned manufacturing ZIP to the matching GitHub Release. Manual workflow runs retain the package as a CI artifact and do not create a release.

## Order a PCB

For project-specific ordering choices and direct manufacturer links, see [ORDERING.md](ORDERING.md).

The preferred ordering choices are:

1. **PCBWay** — direct/shared-project ordering may be provided when a released board has been published there.
2. **JLCPCB** — ordering information or a project/deep link may be provided when available.
3. **OSH Park** — a shared-project link may be provided when the board is suitable and published there.

Project-specific direct ordering links will be added only after the corresponding PCB revision and manufacturing package are ready. Until then, use the released manufacturing files with any manufacturer of your choice.

Other PCB manufacturers are equally permitted. These options are conveniences, not requirements or endorsements of an exclusive supplier.

## Funding disclosure

Some ordering links may be referral, affiliate, shared-project, or sponsored links. If so, Ploos AS may receive commission, account credit, free prototypes, or another benefit when the link is used.

Using such a link should not increase the project's licensing restrictions and does not change your right to obtain the manufacturing files and use another manufacturer.

Any project-specific commercial relationship or sponsorship should be disclosed next to the relevant link.

## Licensing

Hardware design materials and manufacturing files are licensed under **CERN-OHL-P-2.0** unless explicitly stated otherwise. See `LICENSE-HARDWARE`.

Software, firmware, drivers, tools, and other executable code are licensed under the **MIT License** unless explicitly stated otherwise. See `LICENSE-SOFTWARE`.

Third-party components, libraries, footprints, models, or other materials remain subject to their respective licences and notices.

# Hardware Release Qualification

A hardware revision is **RELEASE-READY** only when all mandatory gates below are PASS. Anything not yet demonstrated remains PENDING; a known violation is FAIL.

## Gate 1 — Design identity

- [ ] Exact hardware revision is identified.
- [ ] Git tag/commit is identified.
- [ ] Canonical KiCad PCB source is identified.
- [ ] Matching schematic source is identified where applicable.
- [ ] Multiple-board projects explicitly identify which PCB(s) belong to the release.

## Gate 2 — Electrical/design qualification

- [ ] KiCad DRC passes with no release-blocking violations.
- [ ] ERC is reviewed/passes where a KiCad schematic supports it.
- [ ] Maker-friendly CI lint has run.
- [ ] Maker-friendly deviations are reviewed and documented.
- [ ] Advanced fabrication requirements are documented where applicable.

## Gate 3 — Components and BOM

- [ ] BOM is generated and structurally valid.
- [ ] Critical components have manufacturer/MPN information.
- [ ] Footprints/packages are reviewed against the BOM.
- [ ] Critical lifecycle/availability risks are reviewed.
- [ ] Known substitutions or substitution constraints are documented.
- [ ] Manufacturer assembly substitutions have not silently changed the design.

## Gate 4 — Maker accessibility

- [ ] Assembly approach is documented.
- [ ] Important connectors, polarity, pin 1, jumpers and switches are clearly identified.
- [ ] Important debug/test interfaces are accessible where practical.
- [ ] Socketing/replaceability opportunities have been reviewed.
- [ ] Significant exceptions to MAKER-FRIENDLY.md are documented.

## Gate 5 — Manufacturing package

- [ ] Gerbers generated from the release revision.
- [ ] Drill files generated from the release revision.
- [ ] BOM included when applicable.
- [ ] CPL/placement data included when assembly is supported.
- [ ] Required fabrication/assembly notes included.
- [ ] SHA-256 checksums generated.
- [ ] Versioned manufacturing ZIP generated.
- [ ] Manufacturing CI passes.

## Gate 6 — Documentation

- [ ] README reflects the released hardware status.
- [ ] MANUFACTURING.md is current.
- [ ] MAKER-FRIENDLY.md is current.
- [ ] COMPONENT-POLICY.md exceptions are documented.
- [ ] MANUFACTURER-PROFILES.md requirements are compatible with the board or exceptions are documented.
- [ ] Connector/pinout documentation is available where applicable.
- [ ] Bring-up/test procedure is available.
- [ ] Known limitations are documented.

## Gate 7 — Ordering

- [ ] Vendor-neutral manufacturing ZIP remains the canonical fabrication artifact.
- [ ] Manufacturer-specific project links, if published, match this exact qualified revision.
- [ ] Manufacturer-specific settings that affect correctness are documented.
- [ ] Affiliate/referral/sponsorship relationships are disclosed next to applicable links.
- [ ] At least two manufacturer choices are targeted where practical; three are preferred.

## Gate 8 — Licensing and provenance

- [ ] Hardware files carry/are covered by CERN-OHL-P-2.0.
- [ ] Software files carry/are covered by MIT unless explicitly documented otherwise.
- [ ] Third-party licences/notices are preserved.
- [ ] No proprietary or redistribution-restricted material is accidentally included in release artifacts.

## Qualification result

Use exactly one release status:

- **PENDING** — one or more mandatory checks have not yet been demonstrated.
- **FAIL** — a known mandatory requirement is violated.
- **PASS / RELEASE-READY** — every mandatory gate has been completed successfully.

Do not describe a hardware revision as production-ready, order-ready, or release-ready while its qualification status is PENDING or FAIL.

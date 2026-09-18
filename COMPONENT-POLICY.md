# Maker-Friendly Component and BOM Policy

Ploos-AS hardware should be practical for individual makers to source, assemble, understand, maintain, and repair.

The default priority is **availability and maker accessibility first, cost optimization second**.

## Component selection

Prefer components that:

- are actively manufactured or broadly stocked;
- are available from more than one distributor where practical;
- have a clear manufacturer part number and datasheet;
- use packages that can be hand-soldered or reworked with ordinary maker tools where practical;
- have second-source or documented substitute options when electrical requirements permit;
- do not require proprietary programming, calibration, or assembly services merely to make the design usable.

Do not select a difficult-to-source or manufacturer-exclusive component solely because it reduces BOM cost.

## Package preference

Use through-hole components where they materially improve education, socketing, repair, experimentation, or hand assembly.

For SMD, prefer maker-friendly package sizes and pitches where the electrical and mechanical design permits. Very fine-pitch, BGA, WLCSP and similar packages require a documented technical reason.

Complex devices may be isolated on modules or replaceable subassemblies where that meaningfully improves maker accessibility.

## Sockets and replaceability

Consider sockets for:

- programmable logic and ROM/EPROM/EEPROM devices;
- CPUs and other educationally useful removable devices;
- expensive or difficult-to-source ICs;
- components likely to be replaced during experimentation;
- parts whose failure would otherwise make repair unnecessarily difficult.

Sockets are not mandatory where signal integrity, mechanical reliability, cost, package type, or other technical requirements make them inappropriate.

## BOM requirements

A released BOM should identify, where applicable:

- reference designator;
- quantity;
- value/function;
- manufacturer;
- manufacturer part number (MPN);
- package/footprint;
- critical electrical or mechanical specifications;
- acceptable substitutes or substitution rules;
- sourcing notes for unusual parts;
- whether the part is critical or freely substitutable.

Distributor stock numbers may be provided as conveniences but must not replace the manufacturer part number or technical specification.

## Substitutions

A substitute is acceptable only when it meets the documented requirements of the design.

For non-critical passives, substitution rules should normally be specification-based rather than tied to one manufacturer.

For critical parts, document the parameters that make the selected component critical. Tested alternatives should be recorded when available.

Never silently substitute a component in a published assembled-board ordering profile if that substitution could affect electrical behaviour, firmware compatibility, timing, mechanical fit, safety, or reliability.

## Lifecycle and availability

Before a production-oriented hardware release, review critical components for availability and lifecycle risk.

Avoid obsolete, NRND, allocation-constrained, or single-source parts when a practical alternative exists. Retro or historically significant components may be intentional exceptions; document them and, where practical, provide modern alternatives, adapters, or sourcing guidance.

## Vendor neutrality

The canonical BOM must not require a particular distributor or PCB assembly service.

LCSC, DigiKey, Mouser, Farnell, RS, TME and similar distributor identifiers may be included as optional sourcing aids. The design remains defined by technical requirements and MPNs, not by one distributor's catalogue.

## Counterfeit and provenance considerations

For expensive, obsolete, safety-relevant, programmable, or frequently counterfeited parts, document provenance concerns where useful. Do not present unverified marketplace sources as equivalent to authorized distribution.

## Advanced-project exceptions

AmiCore, RetroSBC, FPGA designs, compute modules, high-speed interfaces and other advanced hardware may necessarily use dense or single-source devices.

Keep unavoidable complexity localized where practical, expose maker-accessible interfaces around it, and document why the component was selected and what replacement constraints exist.

## Release qualification checklist

Before calling a hardware revision production/package-ready, review:

- BOM completeness;
- MPN coverage for critical components;
- footprint/package consistency;
- critical component lifecycle and availability;
- known substitutions;
- socketing/replaceability opportunities;
- manufacturer-specific assembly substitutions;
- unusual sourcing requirements;
- documented exceptions to this policy.

Automated CI may validate structural BOM requirements, but component suitability and substitution decisions require engineering review.

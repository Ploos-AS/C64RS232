# C64RS232 M1.10 — Footprint and mechanical gate

M1.10 freezes the physical package choices before M2 PCB placement. Electrical qualification remains covered by M1.9.

## U1 — RS-232 transceiver

**Selected device:** Texas Instruments `MAX3243EIPWR`

- Status: active production part.
- Package: PW, 28-pin TSSOP.
- Operating range: -40 °C to +85 °C.
- Package body: approximately 9.7 mm × 6.4 mm overall package envelope per TI product data.
- KiCad target footprint: `Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm`.
- Pin numbering must remain identical to the M1.9 qualified 28-pin DB/DW/PW pinout.

The TSSOP choice is retained because it is the already-qualified/orderable M1 baseline part. A later board variant may use the pin-compatible SOIC DW package if hand assembly becomes a priority, but M2 must not silently substitute packages.

## Charge-pump capacitors

The board is a 5 V design. TI's MAX3243E characterization conditions at 5 V use:

- C1: 0.047 µF (47 nF)
- C2: 0.33 µF (330 nF)
- C3 (V+ reservoir): 0.33 µF (330 nF)
- C4 (V- reservoir): 0.33 µF (330 nF)

C5 is the local VCC bypass capacitor and remains 100 nF in the M1 BOM. Capacitor footprints will be frozen before PCB placement; voltage rating and dielectric must be suitable for the charge-pump rails.

## J1 — C64 User Port edge connector

A project-local KiCad footprint is required rather than an unverified generic card-edge footprint.

Gate requirements:

- 24 contacts, 12 per side.
- 3.96 mm / 0.156 in contact pitch.
- Nominal PCB thickness target approximately 1.6 mm, subject to final mechanical verification against the C64 User Port.
- Correct A–N and 1–12 numbering/orientation when viewed from the component side.
- Gold-finger/contact geometry suitable for repeated insertion.
- Mechanical key/notch treatment must be explicitly verified before fabrication.
- 9 VAC contacts remain physically present but electrically isolated from board power.

M2 is blocked until this footprint has a dimensional drawing/check and automated footprint sanity check.

## J2 — DE-9 female DTE

Use a PCB-mount female DE-9 with the DTE electrical pinout qualified in M1.9.

The exact orderable connector and footprint are **not yet frozen**. Before M2 placement, verify:

- female connector;
- horizontal/right-angle versus vertical mounting choice;
- pin numbering as seen from the mating face;
- shell/mounting-hole spacing;
- board-edge offset;
- mechanical retention and enclosure clearance.

Do not select a KiCad DE-9 footprint solely by visual similarity.

## F1 — +5 V protection

The electrical value remains a 100 mA resettable PTC baseline. Exact manufacturer part and land pattern are **not yet frozen**. Select an active, orderable part and verify hold/trip characteristics and voltage rating before M2.

## M1.10 completion gate

M1.10 is complete only when all of the following are true:

1. U1 footprint/package is assigned and machine-checked against the 28-pin qualified symbol.
2. C1–C5 footprints and voltage/dielectric requirements are frozen.
3. J1 project-local User Port footprint is dimensionally verified.
4. J2 exact orderable DE-9 part and matching footprint are frozen.
5. F1 exact orderable PTC and footprint are frozen.
6. A footprint audit script passes in GitHub Actions.
7. Native schematic contains the frozen footprint assignments.

No PCB routing, DRC release, Gerbers, or manufacturing release is authorized until this gate passes.

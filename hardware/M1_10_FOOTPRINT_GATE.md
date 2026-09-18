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

C5 is the local VCC bypass capacitor and remains 100 nF in the M1 BOM. Frozen capacitor baseline for M2 is 0805 / 2012 metric, X7R ceramic, rated at least 25 V for C1–C5. The common 25 V minimum provides margin above both the 5 V supply and the generated charge-pump rails. TI specifies ceramic capacitors and, at 5 V ±0.5 V, 47 nF for C1 and 330 nF for C2–C4. C5 remains 100 nF local VCC bypass.

## J1 — C64 User Port edge connector

A project-local KiCad footprint is required rather than an unverified generic card-edge footprint.

Verified baseline:

- 24 contacts, 12 per side.
- 3.96 mm / 0.156 in contact pitch.
- Correct C64 contact identifiers: 1–12 and A–F,H,J–N.
- Project-local footprint and automated pitch/numbering audit are present and pass CI.

Frozen M1.10 interface baseline:

- nominal PCB thickness: 1.57 mm;
- contact pitch: 3.96 mm / 0.156 in;
- copper finger width: 2.8 mm;
- copper finger length from insertion edge: 7.62 mm;
- front/back fingers are geometrically aligned on opposite copper sides;
- contact identifiers: 1–12 and A–F,H,J–N;
- 9 VAC contacts remain physically present but electrically isolated from board power.

Manufacturing requirements for the card edge are intentionally separated from the KiCad copper geometry. The fabrication package must call out plated/gold card-edge contacts and an insertion-edge bevel/chamfer suitable for a 1.57 mm card-edge PCB. The PCB manufacturer must confirm its supported bevel angle, depth and finish before Gerber release; these process parameters must not be invented as footprint dimensions.

Key/polarisation is handled by the C64 connector/contact numbering and board outline during M2. It must be visually/mechanically reviewed before fabrication.

The J1 footprint geometry is therefore frozen for M1.10. Final manufacturer-specific bevel/finish parameters are an M2 fabrication gate, not an unresolved schematic-footprint dimension.

## J2 — DE-9 female DTE

**Frozen baseline part:** TE Connectivity `5747844-4`, AMPLIMITE HD-20.

Manufacturer data identifies this as an active 9-position receptacle, right-angle PCB mount, through-hole solder termination, with boardlocks and 4-40 threaded inserts. The recommended PCB thickness is 1.57 mm. This matches the desired female DTE connector orientation and provides mechanical retention suitable for a board-edge serial connector.

Frozen requirements:

- manufacturer part: `5747844-4`;
- 9-position female receptacle;
- right-angle PCB mounting;
- through-hole signal contacts;
- boardlocks;
- 4-40 threaded inserts;
- use the manufacturer product drawing as the dimensional authority for the PCB land pattern and board-edge offset.

The generic 2.77 mm KiCad footprint has been rejected and replaced by the project-local `C64RS232:TE_5747844-4` footprint translated from TE product drawing `ENG_CD_5747844_P.pdf`. The project-local footprint uses the drawing-derived 2.74 mm / .108 in signal pitch and 2.84 mm / .112 in row spacing, and is covered by the M1.10 automated audit. J2 is no longer an M1.10 blocker.

## F1 — +5 V protection

**Frozen baseline part:** Littelfuse `1206L010/30WR`, PolySwitch 1206L series resettable PPTC.

Electrical baseline:

- hold current: 100 mA;
- trip current: 250 mA;
- maximum voltage: 30 VDC;
- package: 1206 / 3216 metric;
- surface mount.

The Littelfuse 1206L datasheet confirms ordering number `1206L010/30WR`, 100 mA hold current, 250 mA trip current, 30 V maximum voltage and 1206 surface-mount construction. The current KiCad 1206 fuse footprint is retained as the M1.10 baseline, but final M2 DRC/fabrication review must keep the manufacturer body/termination envelope clear and preserve short routing between the User Port +5 V input and protected `+5V` rail.

## M1.10 completion gate

M1.10 is complete only when all of the following are true:

1. U1 footprint/package is assigned and machine-checked against the 28-pin qualified symbol.
2. C1–C5 footprints and voltage/dielectric requirements are frozen.
3. J1 project-local User Port footprint is dimensionally verified, including insertion/finger/bevel geometry.
4. J2 `5747844-4` manufacturer drawing has been translated to and checked against the selected KiCad footprint.
5. F1 `1206L010/30WR` has a checked 1206 land pattern.
6. A footprint audit script passes all frozen choices in GitHub Actions.
7. Native schematic contains the frozen footprint assignments.

No PCB routing, DRC release, Gerbers, or manufacturing release is authorized until this gate passes.

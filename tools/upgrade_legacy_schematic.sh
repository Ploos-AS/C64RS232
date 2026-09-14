#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SCHEMATIC="$ROOT/hardware/C64RS232_M1.sch"
NATIVE="$ROOT/hardware/C64RS232_M1.kicad_sch"
OUTDIR="$ROOT/build/kicad"

command -v kicad-cli >/dev/null 2>&1 || {
  echo "ERROR: kicad-cli is required" >&2
  exit 2
}

[ -f "$SCHEMATIC" ] || {
  echo "ERROR: legacy schematic not found: $SCHEMATIC" >&2
  exit 3
}

mkdir -p "$OUTDIR"

# KiCad 9+ can convert legacy Eeschema files directly to the native
# .kicad_sch format. The legacy cache library is intentionally kept beside
# the source schematic so the converter can resolve the project symbols.
if [ ! -f "$NATIVE" ]; then
  kicad-cli sch upgrade "$SCHEMATIC"
fi

[ -s "$NATIVE" ] || {
  echo "ERROR: native schematic was not produced: $NATIVE" >&2
  exit 4
}

# Validate the converted native schematic and retain machine-readable output.
kicad-cli sch export pdf \
  --output "$OUTDIR/C64RS232_M1.pdf" \
  "$NATIVE"

kicad-cli sch export netlist \
  --output "$OUTDIR/C64RS232_M1.net" \
  "$NATIVE"

kicad-cli sch erc \
  --output "$OUTDIR/C64RS232_M1-erc.rpt" \
  --exit-code-violations \
  --severity-error \
  "$NATIVE"

[ -s "$OUTDIR/C64RS232_M1.pdf" ] || {
  echo "ERROR: KiCad PDF export was not produced" >&2
  exit 5
}

[ -s "$OUTDIR/C64RS232_M1.net" ] || {
  echo "ERROR: KiCad netlist export was not produced" >&2
  exit 6
}

[ -s "$OUTDIR/C64RS232_M1-erc.rpt" ] || {
  echo "ERROR: KiCad ERC report was not produced" >&2
  exit 7
}

echo "NATIVE SCHEMATIC VALIDATION PASS"
echo "SCHEMATIC: $NATIVE"
echo "PDF: $OUTDIR/C64RS232_M1.pdf"
echo "NETLIST: $OUTDIR/C64RS232_M1.net"
echo "ERC: $OUTDIR/C64RS232_M1-erc.rpt"

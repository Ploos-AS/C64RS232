#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SCHEMATIC="$ROOT/hardware/C64RS232_M1.sch"
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

# KiCad 7's kicad-cli does not provide a schematic 'upgrade' subcommand.
# Legacy schematics are converted to native .kicad_sch when opened and saved
# by Eeschema; until that native file is committed, CI validates the legacy
# source directly through KiCad's supported export path.
kicad-cli sch export pdf --output "$OUTDIR/C64RS232_M1.pdf" "$SCHEMATIC"
kicad-cli sch export netlist --output "$OUTDIR/C64RS232_M1.net" "$SCHEMATIC"

[ -s "$OUTDIR/C64RS232_M1.pdf" ] || {
  echo "ERROR: KiCad PDF export was not produced" >&2
  exit 4
}

[ -s "$OUTDIR/C64RS232_M1.net" ] || {
  echo "ERROR: KiCad netlist export was not produced" >&2
  exit 5
}

echo "LEGACY SCHEMATIC VALIDATION PASS"
echo "PDF: $OUTDIR/C64RS232_M1.pdf"
echo "NETLIST: $OUTDIR/C64RS232_M1.net"

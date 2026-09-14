#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SCHEMATIC="$ROOT/hardware/C64RS232_M1.sch"
OUT="$ROOT/hardware/C64RS232.kicad_sch"

command -v kicad-cli >/dev/null 2>&1 || {
  echo "ERROR: kicad-cli is required" >&2
  exit 2
}

[ -f "$SCHEMATIC" ] || {
  echo "ERROR: legacy schematic not found: $SCHEMATIC" >&2
  exit 3
}

# KiCad's schematic upgrade command reads legacy .sch files and writes the
# current native schematic format. The legacy source remains untouched.
kicad-cli sch upgrade "$SCHEMATIC"

[ -f "$OUT" ] || {
  echo "ERROR: native schematic was not produced: $OUT" >&2
  exit 4
}

echo "NATIVE SCHEMATIC PASS: $OUT"

#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SCHEMATIC="$ROOT/hardware/C64RS232_M1.sch"
NATIVE="$ROOT/hardware/C64RS232_M1.kicad_sch"
OUTDIR="$ROOT/build/kicad"

command -v kicad-cli >/dev/null 2>&1 || { echo "ERROR: kicad-cli is required" >&2; exit 2; }
command -v eeschema >/dev/null 2>&1 || { echo "ERROR: eeschema is required" >&2; exit 2; }
command -v xvfb-run >/dev/null 2>&1 || { echo "ERROR: xvfb-run is required" >&2; exit 2; }
command -v xdotool >/dev/null 2>&1 || { echo "ERROR: xdotool is required" >&2; exit 2; }

[ -f "$SCHEMATIC" ] || { echo "ERROR: legacy schematic not found: $SCHEMATIC" >&2; exit 3; }
mkdir -p "$OUTDIR"

# KiCad 9.0.9 as packaged on Ubuntu does not expose `sch upgrade` despite
# newer KiCad documentation describing that subcommand. Legacy conversion is
# therefore performed by Eeschema itself: opening a legacy .sch and saving it
# writes the native .kicad_sch format while retaining the cache-library symbols.
if [ ! -s "$NATIVE" ]; then
  rm -f "$NATIVE"
  LOG="$OUTDIR/eeschema-convert.log"
  (
    cd "$ROOT/hardware"
    exec xvfb-run -a eeschema "$(basename "$SCHEMATIC")"
  ) >"$LOG" 2>&1 &
  PID=$!

  for _ in $(seq 1 30); do
    if xdotool search --name 'C64RS232_M1' windowactivate --sync key ctrl+s >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done

  # Allow the save operation to complete, then close Eeschema.
  sleep 3
  xdotool search --name 'C64RS232_M1' windowactivate --sync key alt+F4 >/dev/null 2>&1 || true
  wait "$PID" || true
fi

[ -s "$NATIVE" ] || {
  echo "ERROR: Eeschema did not produce native schematic: $NATIVE" >&2
  cat "$OUTDIR/eeschema-convert.log" >&2 || true
  exit 4
}

kicad-cli sch export pdf --output "$OUTDIR/C64RS232_M1.pdf" "$NATIVE"
kicad-cli sch export netlist --output "$OUTDIR/C64RS232_M1.net" "$NATIVE"
kicad-cli sch erc --output "$OUTDIR/C64RS232_M1-erc.rpt" --exit-code-violations --severity-error "$NATIVE"

[ -s "$OUTDIR/C64RS232_M1.pdf" ] || { echo "ERROR: PDF export missing" >&2; exit 5; }
[ -s "$OUTDIR/C64RS232_M1.net" ] || { echo "ERROR: netlist export missing" >&2; exit 6; }
[ -s "$OUTDIR/C64RS232_M1-erc.rpt" ] || { echo "ERROR: ERC report missing" >&2; exit 7; }

echo "NATIVE SCHEMATIC VALIDATION PASS"
echo "SCHEMATIC: $NATIVE"
echo "PDF: $OUTDIR/C64RS232_M1.pdf"
echo "NETLIST: $OUTDIR/C64RS232_M1.net"
echo "ERC: $OUTDIR/C64RS232_M1-erc.rpt"

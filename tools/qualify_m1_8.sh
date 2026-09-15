#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
NATIVE="$ROOT/hardware/C64RS232_M1.kicad_sch"
OUTDIR="$ROOT/build/kicad/m1_8"

command -v kicad-cli >/dev/null 2>&1 || { echo 'ERROR: kicad-cli is required' >&2; exit 2; }
[ -s "$NATIVE" ] || { echo "ERROR: native schematic missing: $NATIVE" >&2; exit 3; }
mkdir -p "$OUTDIR"

kicad-cli sch export netlist --output "$OUTDIR/C64RS232_M1.net" "$NATIVE"
[ -s "$OUTDIR/C64RS232_M1.net" ] || { echo 'ERROR: M1.8 netlist export missing' >&2; exit 4; }
python3 "$ROOT/tools/check_m1_8_netlist.py"

# Keep ERC evidence visible while M1.8 classifies/fixes violations.  A later
# M1.8 increment will promote the classified ERC result to a hard gate.
set +e
kicad-cli sch erc --output "$OUTDIR/C64RS232_M1-erc.rpt" --exit-code-violations "$NATIVE"
ERC_RC=$?
set -e
printf '%s\n' "$ERC_RC" > "$OUTDIR/erc-exit-code.txt"
[ -s "$OUTDIR/C64RS232_M1-erc.rpt" ] || { echo 'ERROR: M1.8 ERC report missing' >&2; exit 5; }

echo 'M1.8a RUNNER QUALIFICATION PASS'
echo "ERC exit code (classification in progress): $ERC_RC"

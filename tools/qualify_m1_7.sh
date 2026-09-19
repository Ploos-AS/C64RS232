#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
NATIVE="$ROOT/hardware/C64RS232_M1.kicad_sch"
OUTDIR="$ROOT/build/kicad/m1_7"

command -v kicad-cli >/dev/null 2>&1 || { echo 'ERROR: kicad-cli is required' >&2; exit 2; }
[ -s "$NATIVE" ] || { echo "ERROR: native schematic missing: $NATIVE" >&2; exit 3; }
mkdir -p "$OUTDIR"

python3 "$ROOT/tools/check_m1_7.py"

kicad-cli sch export netlist --output "$OUTDIR/C64RS232_M1.net" "$NATIVE"
kicad-cli sch export pdf --output "$OUTDIR/C64RS232_M1.pdf" "$NATIVE"

[ -s "$OUTDIR/C64RS232_M1.net" ] || { echo 'ERROR: M1.7 netlist export missing' >&2; exit 4; }
[ -s "$OUTDIR/C64RS232_M1.pdf" ] || { echo 'ERROR: M1.7 PDF export missing' >&2; exit 5; }

# Use the same ERC policy as the native conversion gate. Warnings remain in
# the report as review evidence; electrical errors are the qualification gate.
set +e
kicad-cli sch erc --output "$OUTDIR/C64RS232_M1-erc.rpt" --exit-code-violations --severity-error "$NATIVE"
erc_rc=$?
set -e
[ -s "$OUTDIR/C64RS232_M1-erc.rpt" ] || { echo 'ERROR: M1.7 ERC report missing' >&2; exit 6; }
echo "--- M1.7 ERC REPORT ---"
cat "$OUTDIR/C64RS232_M1-erc.rpt"
echo "--- END M1.7 ERC REPORT ---"
[ "$erc_rc" -eq 0 ] || exit "$erc_rc"

echo 'M1.7 RUNNER QUALIFICATION PASS'
echo 'ERC error-severity gate: PASS'

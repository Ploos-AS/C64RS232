#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SCHEMATIC="$ROOT/hardware/C64RS232_M1.sch"
NATIVE="$ROOT/hardware/C64RS232_M1.kicad_sch"
OUTDIR="$ROOT/build/kicad"
DISPLAY_NUM=:99

command -v kicad-cli >/dev/null 2>&1 || { echo "ERROR: kicad-cli is required" >&2; exit 2; }
command -v eeschema >/dev/null 2>&1 || { echo "ERROR: eeschema is required" >&2; exit 2; }
command -v Xvfb >/dev/null 2>&1 || { echo "ERROR: Xvfb is required" >&2; exit 2; }
command -v xdotool >/dev/null 2>&1 || { echo "ERROR: xdotool is required" >&2; exit 2; }

[ -f "$SCHEMATIC" ] || { echo "ERROR: legacy schematic not found: $SCHEMATIC" >&2; exit 3; }
mkdir -p "$OUTDIR"

if [ ! -s "$NATIVE" ]; then
  rm -f "$NATIVE"
  LOG="$OUTDIR/eeschema-convert.log"

  Xvfb "$DISPLAY_NUM" -screen 0 1280x1024x24 >"$OUTDIR/xvfb.log" 2>&1 &
  XVFB_PID=$!
  trap 'kill "$XVFB_PID" >/dev/null 2>&1 || true' EXIT
  sleep 2

  export DISPLAY="$DISPLAY_NUM"
  (
    cd "$ROOT/hardware"
    exec eeschema "$(basename "$SCHEMATIC")"
  ) >"$LOG" 2>&1 &
  EESCHEMA_PID=$!

  WINDOW_ID=""
  for _ in $(seq 1 45); do
    WINDOW_ID="$(xdotool search --name 'C64RS232_M1' 2>/dev/null | head -n1 || true)"
    if [ -n "$WINDOW_ID" ]; then
      break
    fi
    if ! kill -0 "$EESCHEMA_PID" >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done

  if [ -z "$WINDOW_ID" ]; then
    echo "ERROR: Eeschema window did not appear" >&2
    cat "$LOG" >&2 || true
    wait "$EESCHEMA_PID" || true
    exit 4
  fi

  xdotool windowactivate --sync "$WINDOW_ID"
  xdotool key --window "$WINDOW_ID" ctrl+s

  for _ in $(seq 1 30); do
    [ -s "$NATIVE" ] && break
    sleep 1
  done

  xdotool key --window "$WINDOW_ID" alt+F4 >/dev/null 2>&1 || true
  wait "$EESCHEMA_PID" || true

  kill "$XVFB_PID" >/dev/null 2>&1 || true
  trap - EXIT
fi

[ -s "$NATIVE" ] || {
  echo "ERROR: Eeschema did not produce native schematic: $NATIVE" >&2
  cat "$OUTDIR/eeschema-convert.log" >&2 || true
  exit 5
}

kicad-cli sch export pdf --output "$OUTDIR/C64RS232_M1.pdf" "$NATIVE"
kicad-cli sch export netlist --output "$OUTDIR/C64RS232_M1.net" "$NATIVE"
kicad-cli sch erc --output "$OUTDIR/C64RS232_M1-erc.rpt" --exit-code-violations --severity-error "$NATIVE"

[ -s "$OUTDIR/C64RS232_M1.pdf" ] || { echo "ERROR: PDF export missing" >&2; exit 6; }
[ -s "$OUTDIR/C64RS232_M1.net" ] || { echo "ERROR: netlist export missing" >&2; exit 7; }
[ -s "$OUTDIR/C64RS232_M1-erc.rpt" ] || { echo "ERROR: ERC report missing" >&2; exit 8; }

echo "NATIVE SCHEMATIC VALIDATION PASS"
echo "SCHEMATIC: $NATIVE"
echo "PDF: $OUTDIR/C64RS232_M1.pdf"
echo "NETLIST: $OUTDIR/C64RS232_M1.net"
echo "ERC: $OUTDIR/C64RS232_M1-erc.rpt"

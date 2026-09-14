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

XVFB_PID=""
EESCHEMA_PID=""
REMAP_TRIGGERED=0

capture_diagnostics() {
  {
    echo "=== date ==="
    date -u || true
    echo "=== processes ==="
    ps -ef | grep -E '[e]eschema|[k]icad|[X]vfb' || true
    echo "=== visible windows ==="
    xdotool search --onlyvisible --name '.*' getwindowname %@ 2>&1 || true
    echo "=== all windows ==="
    xdotool search --name '.*' getwindowname %@ 2>&1 || true
  } >"$OUTDIR/gui-diagnostics.txt" 2>&1

  if command -v import >/dev/null 2>&1; then
    import -display "$DISPLAY_NUM" -window root "$OUTDIR/gui-root.png" >/dev/null 2>&1 || true
  fi
}

cleanup() {
  capture_diagnostics || true

  if [ -n "$EESCHEMA_PID" ] && kill -0 "$EESCHEMA_PID" >/dev/null 2>&1; then
    kill "$EESCHEMA_PID" >/dev/null 2>&1 || true
    sleep 2
    kill -9 "$EESCHEMA_PID" >/dev/null 2>&1 || true
  fi

  if [ -n "$XVFB_PID" ] && kill -0 "$XVFB_PID" >/dev/null 2>&1; then
    kill "$XVFB_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

wait_for_exit() {
  pid="$1"
  seconds="$2"
  for _ in $(seq 1 "$seconds"); do
    if ! kill -0 "$pid" >/dev/null 2>&1; then
      wait "$pid" || true
      return 0
    fi
    sleep 1
  done
  return 1
}

press_enter_on_dialog() {
  title="$1"
  dialog_id="$(xdotool search --onlyvisible --name "$title" 2>/dev/null | head -n1 || true)"
  [ -n "$dialog_id" ] || return 1
  echo "INFO: handling KiCad dialog: $title"
  xdotool windowactivate --sync "$dialog_id" >/dev/null 2>&1 || true
  xdotool key --window "$dialog_id" Return >/dev/null 2>&1 || true
  sleep 2
  return 0
}

click_remap_symbols() {
  dialog_id="$(xdotool search --onlyvisible --name '^Remap Symbols$' 2>/dev/null | head -n1 || true)"
  [ -n "$dialog_id" ] || return 1

  if [ "$REMAP_TRIGGERED" -eq 1 ]; then
    return 0
  fi

  # In KiCad 9 the Remap Symbols window is not an ordinary confirmation
  # dialog: Return does not activate the action button.  Click the actual
  # "Remap Symbols" button explicitly.  Its centre is at roughly 90% of the
  # dialog width and 10% of the dialog height; use window-relative coordinates
  # so this remains independent of the dialog's absolute screen position.
  geometry="$(xdotool getwindowgeometry --shell "$dialog_id" 2>/dev/null || true)"
  width="$(printf '%s\n' "$geometry" | sed -n 's/^WIDTH=//p')"
  height="$(printf '%s\n' "$geometry" | sed -n 's/^HEIGHT=//p')"

  if [ -z "$width" ] || [ -z "$height" ]; then
    echo "ERROR: could not determine Remap Symbols dialog geometry" >&2
    return 1
  fi

  click_x=$((width * 90 / 100))
  click_y=$((height * 10 / 100))
  echo "INFO: clicking KiCad Remap Symbols action at relative ${click_x},${click_y} (${width}x${height})"

  xdotool windowactivate --sync "$dialog_id" >/dev/null 2>&1 || true
  xdotool mousemove --window "$dialog_id" "$click_x" "$click_y" >/dev/null 2>&1 || true
  xdotool click 1 >/dev/null 2>&1 || true
  REMAP_TRIGGERED=1
  sleep 3
  return 0
}

if [ ! -s "$NATIVE" ]; then
  rm -f "$NATIVE"
  LOG="$OUTDIR/eeschema-convert.log"

  Xvfb "$DISPLAY_NUM" -screen 0 1280x1024x24 >"$OUTDIR/xvfb.log" 2>&1 &
  XVFB_PID=$!
  sleep 2

  export DISPLAY="$DISPLAY_NUM"
  (
    cd "$ROOT/hardware"
    exec eeschema "$(basename "$SCHEMATIC")"
  ) >"$LOG" 2>&1 &
  EESCHEMA_PID=$!

  WINDOW_ID=""
  for _ in $(seq 1 90); do
    # Fresh GitHub runners start KiCad with this modal dialog. The
    # recommended "Copy default global symbol library table" option is
    # already selected, so Return accepts it safely.
    press_enter_on_dialog '^Configure Global Symbol Library Table$' || true

    # KiCad 9 then presents a migration window.  Trigger its explicit action
    # once; repeatedly pressing Return leaves this window open forever.
    click_remap_symbols || true

    WINDOW_ID="$(xdotool search --onlyvisible --name 'C64RS232_M1' 2>/dev/null | head -n1 || true)"
    if [ -n "$WINDOW_ID" ]; then
      break
    fi
    if ! kill -0 "$EESCHEMA_PID" >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done

  if [ -z "$WINDOW_ID" ]; then
    echo "ERROR: Eeschema schematic window did not appear within 90 seconds" >&2
    capture_diagnostics
    cat "$LOG" >&2 || true
    exit 4
  fi

  xdotool windowactivate --sync "$WINDOW_ID" || true
  xdotool key --window "$WINDOW_ID" ctrl+s || true

  for _ in $(seq 1 45); do
    [ -s "$NATIVE" ] && break

    # Legacy-to-native conversion can open a Save As dialog. KiCad proposes
    # the converted .kicad_sch name, so accepting the default is intentional.
    press_enter_on_dialog '^Save As$' || true

    if ! kill -0 "$EESCHEMA_PID" >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done

  if [ ! -s "$NATIVE" ]; then
    echo "ERROR: native schematic was not created within 45 seconds after Ctrl+S" >&2
    capture_diagnostics
    cat "$LOG" >&2 || true
    exit 5
  fi

  xdotool key --window "$WINDOW_ID" alt+F4 >/dev/null 2>&1 || true

  if ! wait_for_exit "$EESCHEMA_PID" 15; then
    echo "WARNING: Eeschema did not exit within 15 seconds; terminating it" >&2
    capture_diagnostics
    kill "$EESCHEMA_PID" >/dev/null 2>&1 || true
    if ! wait_for_exit "$EESCHEMA_PID" 5; then
      kill -9 "$EESCHEMA_PID" >/dev/null 2>&1 || true
      wait "$EESCHEMA_PID" || true
    fi
  fi
  EESCHEMA_PID=""
fi

[ -s "$NATIVE" ] || {
  echo "ERROR: Eeschema did not produce native schematic: $NATIVE" >&2
  cat "$OUTDIR/eeschema-convert.log" >&2 || true
  exit 6
}

kicad-cli sch export pdf --output "$OUTDIR/C64RS232_M1.pdf" "$NATIVE"
kicad-cli sch export netlist --output "$OUTDIR/C64RS232_M1.net" "$NATIVE"
kicad-cli sch erc --output "$OUTDIR/C64RS232_M1-erc.rpt" --exit-code-violations --severity-error "$NATIVE"

[ -s "$OUTDIR/C64RS232_M1.pdf" ] || { echo "ERROR: PDF export missing" >&2; exit 7; }
[ -s "$OUTDIR/C64RS232_M1.net" ] || { echo "ERROR: netlist export missing" >&2; exit 8; }
[ -s "$OUTDIR/C64RS232_M1-erc.rpt" ] || { echo "ERROR: ERC report missing" >&2; exit 9; }

echo "NATIVE SCHEMATIC VALIDATION PASS"
echo "SCHEMATIC: $NATIVE"
echo "PDF: $OUTDIR/C64RS232_M1.pdf"
echo "NETLIST: $OUTDIR/C64RS232_M1.net"
echo "ERC: $OUTDIR/C64RS232_M1-erc.rpt"

#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
SCHEMATIC="$ROOT/hardware/C64RS232.kicad_sch"
PROJECT="$ROOT/hardware/C64RS232.kicad_pro"

fail=0

if [ ! -f "$PROJECT" ]; then
    echo "FAIL: missing $PROJECT"
    fail=1
fi

if [ ! -f "$SCHEMATIC" ]; then
    echo "PENDING: native KiCad schematic has not yet been generated"
    fail=1
else
    case "$(wc -c < "$SCHEMATIC")" in
        0) echo "FAIL: native schematic is empty"; fail=1 ;;
        *) echo "FOUND: native KiCad schematic" ;;
    esac
fi

if command -v kicad-cli >/dev/null 2>&1 && [ -f "$SCHEMATIC" ]; then
    echo "Running KiCad schematic ERC..."
    if ! kicad-cli sch erc "$SCHEMATIC" --exit-code-violations 2>/dev/null; then
        echo "FAIL: KiCad ERC reported violations"
        fail=1
    else
        echo "PASS: KiCad ERC"
    fi
else
    echo "INFO: kicad-cli unavailable or native schematic missing; ERC not run"
fi

if [ "$fail" -ne 0 ]; then
    exit 1
fi

echo "M1.4 NATIVE KICAD GATE PASS"

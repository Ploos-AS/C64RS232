EESchema Schematic File Version 4
LIBS:C64RS232_M1-cache
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
Sheet 1 1
Title "C64RS232 User Port to RS-232"
Date "2026-09-14"
Rev "M1"
Comp "Ploos-AS"
Comment1 "C64 User Port / MAX3243 / DE-9 DTE"
Comment2 "SLIP-capable architecture"
Comment3 "M1 schematic baseline"
Comment4 "Verify against datasheets before manufacture"
$EndDescr
$Comp
L C64_USERPORT J1
U 1 1 1
P 1800 3800
F 0 "J1" H 1800 5100 50  0000 C CNN
F 1 "C64 USER PORT" H 1800 5000 50 0000 C CNN
	1    1800 3800
	1 0 0 -1
$EndComp
$Comp
L MAX3243 U1
U 1 1 2
P 5200 3800
F 0 "U1" H 5200 5350 50 0000 C CNN
F 1 "MAX3243" H 5200 5250 50 0000 C CNN
	1    5200 3800
	1 0 0 -1
$EndComp
$Comp
L DB9_DTE J2
U 1 1 3
P 8500 3800
F 0 "J2" H 8500 4450 50 0000 C CNN
F 1 "DE-9 FEMALE / DTE" H 8500 4350 50 0000 C CNN
	1    8500 3800
	1 0 0 -1
$EndComp
$Comp
L C C1
U 1 1 4
P 3900 1600
F 0 "C1" H 4015 1646 50 0000 L CNN
F 1 "100nF" H 4015 1555 50 0000 L CNN
	1    3900 1600
	1 0 0 -1
$EndComp
$Comp
L C C2
U 1 1 5
P 4400 1600
F 0 "C2" H 4515 1646 50 0000 L CNN
F 1 "100nF" H 4515 1555 50 0000 L CNN
	1    4400 1600
	1 0 0 -1
$EndComp
$Comp
L C C3
U 1 1 6
P 4900 1600
F 0 "C3" H 5015 1646 50 0000 L CNN
F 1 "100nF" H 5015 1555 50 0000 L CNN
	1    4900 1600
	1 0 0 -1
$EndComp
$Comp
L C C4
U 1 1 7
P 5400 1600
F 0 "C4" H 5515 1646 50 0000 L CNN
F 1 "100nF" H 5515 1555 50 0000 L CNN
	1    5400 1600
	1 0 0 -1
$EndComp
$Comp
L C C5
U 1 1 8
P 5900 1600
F 0 "C5" H 6015 1646 50 0000 L CNN
F 1 "100nF" H 6015 1555 50 0000 L CNN
	1    5900 1600
	1 0 0 -1
$EndComp
$Comp
L R R1
U 1 1 9
P 7000 1500
F 0 "R1" V 6793 1500 50 0000 C CNN
F 1 "1k" V 6884 1500 50 0000 C CNN
	1    7000 1500
	0 1 1 0
$EndComp
Text Notes 1300 2400 0 80 ~ 16
C64 USER PORT
Text Notes 4550 2400 0 80 ~ 16
RS-232 TRANSCEIVER
Text Notes 8000 2400 0 80 ~ 16
DE-9 DTE
Text Notes 1400 5600 0 60 ~ 12
Only required User Port signals are connected. +5V is used; 9VAC and RESET are intentionally NC.
Text Notes 1400 5750 0 60 ~ 12
RXD uses both FLAG2 (B) and PB0 (C), as required by the C64 RS-232 software convention.
Text Notes 1400 5900 0 60 ~ 12
MAX3243 provides 3 drivers / 5 receivers, matching TXD/RTS/DTR and RXD/CTS/DSR/DCD/RI.
Text Notes 1400 6050 0 60 ~ 12
FORCEON is tied high and FORCEOFF low for normal always-on operation.
Text Notes 1400 6200 0 60 ~ 12
This is an M1 design baseline; ERC/DRC and manufacturer-specific footprint checks remain required.
Text Label 2300 3000 0 50 ~ 0
C64_+5V
Text Label 2300 3200 0 50 ~ 0
C64_GND
Text Label 2300 3400 0 50 ~ 0
TXD_PA2
Text Label 2300 3600 0 50 ~ 0
RXD_PB0_FLAG2
Text Label 2300 3800 0 50 ~ 0
RTS_PB1
Text Label 2300 4000 0 50 ~ 0
DTR_PB2
Text Label 2300 4200 0 50 ~ 0
RI_PB3
Text Label 2300 4400 0 50 ~ 0
DCD_PB4
Text Label 2300 4600 0 50 ~ 0
CTS_PB6
Text Label 2300 4800 0 50 ~ 0
DSR_PB7
Text Label 6000 3000 0 50 ~ 0
RS232_TXD
Text Label 6000 3200 0 50 ~ 0
RS232_RTS
Text Label 6000 3400 0 50 ~ 0
RS232_DTR
Text Label 6000 3600 0 50 ~ 0
RS232_RXD
Text Label 6000 3800 0 50 ~ 0
RS232_CTS
Text Label 6000 4000 0 50 ~ 0
RS232_DSR
Text Label 6000 4200 0 50 ~ 0
RS232_DCD
Text Label 6000 4400 0 50 ~ 0
RS232_RI
Text Label 7700 3000 0 50 ~ 0
DB9_DCD_1
Text Label 7700 3200 0 50 ~ 0
DB9_RXD_2
Text Label 7700 3400 0 50 ~ 0
DB9_TXD_3
Text Label 7700 3600 0 50 ~ 0
DB9_DTR_4
Text Label 7700 3800 0 50 ~ 0
DB9_GND_5
Text Label 7700 4000 0 50 ~ 0
DB9_DSR_6
Text Label 7700 4200 0 50 ~ 0
DB9_RTS_7
Text Label 7700 4400 0 50 ~ 0
DB9_CTS_8
Text Label 7700 4600 0 50 ~ 0
DB9_RI_9
Wire Notes Line
	1300 2500 3200 2500
Wire Notes Line
	3200 2500 3200 5250
Wire Notes Line
	3200 5250 1300 5250
Wire Notes Line
	1300 5250 1300 2500
Wire Notes Line
	4300 2500 6100 2500
Wire Notes Line
	6100 2500 6100 5250
Wire Notes Line
	6100 5250 4300 5250
Wire Notes Line
	4300 5250 4300 2500
Wire Notes Line
	7600 2500 9300 2500
Wire Notes Line
	9300 2500 9300 5000
Wire Notes Line
	9300 5000 7600 5000
Wire Notes Line
	7600 5000 7600 2500
$EndSCHEMATC

EESchema Schematic File Version 4
LIBS:C64RS232_M1-cache
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
Sheet 1 1
Title "C64RS232 User Port to RS-232"
Date "2026-09-14"
Rev "M1.10"
Comp "Ploos-AS"
Comment1 "C64 User Port / MAX3243 / DE-9 DTE"
Comment2 "SLIP-capable architecture"
Comment3 "M1.10 frozen footprint baseline"
Comment4 "Verify against datasheets before manufacture"
$EndDescr
$Comp
L C64_USERPORT J1
U 1 1 1
P 1800 3800
F 0 "J1" H 1800 5100 50  0000 C CNN
F 1 "C64 USER PORT" H 1800 5000 50 0000 C CNN
F 2 "C64RS232:C64_User_Port_Edge" H 0 0 50 0001 C CNN
	1    1800 3800
	1 0 0 -1
$EndComp
$Comp
L MAX3243 U1
U 1 1 2
P 5200 3800
F 0 "U1" H 5200 5350 50 0000 C CNN
F 1 "MAX3243EIPWR" H 0 0 50 0000 C CNN
F 2 "Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm" H 0 0 50 0001 C CNN
	1    5200 3800
	1 0 0 -1
$EndComp
$Comp
L DB9_DTE J2
U 1 1 3
P 8500 3800
F 0 "J2" H 8500 4450 50 0000 C CNN
F 1 "5747844-4" H 0 0 50 0000 C CNN
F 2 "Connector_Dsub:DSUB-9_Female_Horizontal_P2.77x2.84mm_EdgePinOffset9.40mm_Housed_MountingHolesOffset11.32mm" H 0 0 50 0001 C CNN
	1    8500 3800
	1 0 0 -1
$EndComp
$Comp
L C C1
U 1 1 4
P 3900 1600
F 0 "C1" H 4015 1646 50 0000 L CNN
F 1 "47nF" H 4015 1555 50 0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder" H 0 0 50 0001 C CNN
	1    3900 1600
	1 0 0 -1
$EndComp
$Comp
L C C2
U 1 1 5
P 4400 1600
F 0 "C2" H 4515 1646 50 0000 L CNN
F 1 "330nF" H 4515 1555 50 0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder" H 0 0 50 0001 C CNN
	1    4400 1600
	1 0 0 -1
$EndComp
$Comp
L C C3
U 1 1 6
P 4900 1600
F 0 "C3" H 5015 1646 50 0000 L CNN
F 1 "330nF" H 5015 1555 50 0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder" H 0 0 50 0001 C CNN
	1    4900 1600
	1 0 0 -1
$EndComp
$Comp
L C C4
U 1 1 7
P 5400 1600
F 0 "C4" H 5515 1646 50 0000 L CNN
F 1 "330nF" H 5515 1555 50 0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder" H 0 0 50 0001 C CNN
	1    5400 1600
	1 0 0 -1
$EndComp
$Comp
L C C5
U 1 1 8
P 5900 1600
F 0 "C5" H 6015 1646 50 0000 L CNN
F 1 "100nF" H 6015 1555 50 0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder" H 0 0 50 0001 C CNN
	1    5900 1600
	1 0 0 -1
$EndComp
$Comp
L R F1
U 1 1 9
P 7000 1500
F 0 "F1" V 6793 1500 50 0000 C CNN
F 1 "1206L010/30WR" H 0 0 50 0000 C CNN
F 2 "Fuse:Fuse_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 0 0 50 0001 C CNN
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
FORCEON and FORCEOFF are tied high for normal always-on operation.
Text Notes 1400 6200 0 60 ~ 12
This is an M1 design baseline; ERC/DRC and manufacturer-specific footprint checks remain required.
Text Label 1300 4300 0 50 ~ 0
C64_TXD
Text Label 4500 3900 0 50 ~ 0
C64_TXD
Text Label 1300 3600 0 50 ~ 0
C64_RTS
Text Label 4500 3800 0 50 ~ 0
C64_RTS
Text Label 1300 3700 0 50 ~ 0
C64_DTR
Text Label 4500 3700 0 50 ~ 0
C64_DTR
Text Label 1300 3500 0 50 ~ 0
C64_RXD
Text Label 1300 3400 0 50 ~ 0
C64_RXD
Text Label 5900 3500 0 50 ~ 0
C64_RXD
Text Label 1300 4100 0 50 ~ 0
C64_CTS
Text Label 5900 3600 0 50 ~ 0
C64_CTS
Text Label 1300 4200 0 50 ~ 0
C64_DSR
Text Label 5900 3700 0 50 ~ 0
C64_DSR
Text Label 1300 3900 0 50 ~ 0
C64_DCD
Text Label 5900 3800 0 50 ~ 0
C64_DCD
Text Label 1300 3800 0 50 ~ 0
C64_RI
Text Label 5900 3900 0 50 ~ 0
C64_RI
Text Label 4500 3400 0 50 ~ 0
RS232_TXD
Text Label 8000 3600 0 50 ~ 0
RS232_TXD
Text Label 4500 3500 0 50 ~ 0
RS232_RTS
Text Label 8000 4000 0 50 ~ 0
RS232_RTS
Text Label 4500 3600 0 50 ~ 0
RS232_DTR
Text Label 8000 3700 0 50 ~ 0
RS232_DTR
Text Label 4500 2900 0 50 ~ 0
RS232_RXD
Text Label 8000 3500 0 50 ~ 0
RS232_RXD
Text Label 4500 3000 0 50 ~ 0
RS232_CTS
Text Label 8000 4100 0 50 ~ 0
RS232_CTS
Text Label 4500 3100 0 50 ~ 0
RS232_DSR
Text Label 8000 3900 0 50 ~ 0
RS232_DSR
Text Label 4500 3200 0 50 ~ 0
RS232_DCD
Text Label 8000 3400 0 50 ~ 0
RS232_DCD
Text Label 4500 3300 0 50 ~ 0
RS232_RI
Text Label 8000 4200 0 50 ~ 0
RS232_RI
Text Label 2300 3400 0 50 ~ 0
RAW_5V
Text Label 7000 1350 0 50 ~ 0
RAW_5V
Text Label 7000 1650 0 50 ~ 0
+5V
Text Label 5900 2800 0 50 ~ 0
+5V
Text Label 5900 3100 0 50 ~ 0
+5V
Text Label 5900 3200 0 50 ~ 0
+5V
Text Label 5900 1450 0 50 ~ 0
+5V
Text Label 2300 3300 0 50 ~ 0
GND
Text Label 2300 4400 0 50 ~ 0
GND
Text Label 1300 3300 0 50 ~ 0
GND
Text Label 1300 4400 0 50 ~ 0
GND
Text Label 5900 2900 0 50 ~ 0
GND
Text Label 8000 3800 0 50 ~ 0
GND
Text Label 4900 1750 0 50 ~ 0
GND
Text Label 5400 1750 0 50 ~ 0
GND
Text Label 5900 1750 0 50 ~ 0
GND
Text Label 3900 1450 0 50 ~ 0
C1_PLUS
Text Label 5900 2600 0 50 ~ 0
C1_PLUS
Text Label 3900 1750 0 50 ~ 0
C1_MINUS
Text Label 5900 3000 0 50 ~ 0
C1_MINUS
Text Label 4400 1450 0 50 ~ 0
C2_PLUS
Text Label 4500 2600 0 50 ~ 0
C2_PLUS
Text Label 4400 1750 0 50 ~ 0
C2_MINUS
Text Label 4500 2700 0 50 ~ 0
C2_MINUS
Text Label 4900 1450 0 50 ~ 0
VPLUS
Text Label 5900 2700 0 50 ~ 0
VPLUS
Text Label 5400 1450 0 50 ~ 0
VMINUS
Text Label 4500 2800 0 50 ~ 0
VMINUS
NoConn ~ 2300 3500
NoConn ~ 2300 3600
NoConn ~ 2300 3700
NoConn ~ 2300 3800
NoConn ~ 2300 3900
NoConn ~ 2300 4000
NoConn ~ 2300 4100
NoConn ~ 2300 4200
NoConn ~ 2300 4300
NoConn ~ 1300 4000
NoConn ~ 5900 3400
NoConn ~ 5900 3300
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
$Comp
L PWR_FLAG #FLG0101
U 1 1 10
P 7500 1650
F 0 "#FLG0101" H 7500 1725 50 0001 C CNN
F 1 "PWR_FLAG" H 7500 1823 50 0000 C CNN
	1    7500 1650
	1    0    0    -1
$EndComp
Text Label 7500 1650 0 50 ~ 0
+5V
$EndSCHEMATC

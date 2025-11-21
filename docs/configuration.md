---
layout: default
title: Configuration
---

# Klipper Configuration

To control the Box Turtle from your printer, you need to add it as a secondary MCU in Klipper.

## 1. Find the Serial ID

SSH into your Klipper host (e.g., Raspberry Pi) and run:

```bash
ls /dev/serial/by-id/*
```

Look for a device named `usb-Klipper_rp2040_...`. Copy this path.

## 2. Edit `printer.cfg`

Add the following configuration to your `printer.cfg` file:

```ini
[mcu feeder]
serial: /dev/serial/by-id/usb-Klipper_rp2040_YOUR_ID_HERE

# --- Lane 1 ---
[stepper_extra lane1]
step_pin: feeder:gpio2
dir_pin: feeder:gpio3
enable_pin: !feeder:gpio12
microsteps: 16
rotation_distance: 22.6 # Calibrate this!
endstop_pin: ^feeder:gpio16 # Sensor 1

# --- Lane 2 ---
[stepper_extra lane2]
step_pin: feeder:gpio4
dir_pin: feeder:gpio5
enable_pin: !feeder:gpio12
microsteps: 16
rotation_distance: 22.6
endstop_pin: ^feeder:gpio17 # Sensor 2

# ... (Repeat for Lanes 3 & 4 using pins from electronics_design.md) ...

# --- Cutter Servo ---
[servo cutter]
pin: feeder:gpio20
maximum_servo_angle: 180
initial_angle: 0
```

## 3. Macros

Add these macros to automate filament changes:

```ini
[gcode_macro CUT_FILAMENT]
gcode:
    SET_SERVO SERVO=cutter ANGLE=90
    G4 P500
    SET_SERVO SERVO=cutter ANGLE=0
    G4 P500
    SET_SERVO SERVO=cutter WIDTH=0

[gcode_macro LOAD_LANE_1]
gcode:
    MANUAL_STEPPER STEPPER=lane1 ENABLE=1
    MANUAL_STEPPER STEPPER=lane1 MOVE=500 SPEED=20 # Feed 500mm
    MANUAL_STEPPER STEPPER=lane1 ENABLE=0
```

## 4. Slicer Setup

In your slicer (Orca/Prusa), set the "Tool Change G-code" to:

```gcode
T[next_extruder]
```

And define `[gcode_macro T0]`, `[gcode_macro T1]`, etc., in Klipper to call your `LOAD_LANE_X` macros.

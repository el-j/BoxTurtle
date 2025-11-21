# Box Turtle 4-Lane Feeder Electronics Design

This guide details the electronics hardware required to build a 4-lane filament feeder and cutter system for the Box Turtle project. While I cannot generate a binary Fritzing (`.fzz`) file, this document provides the complete Bill of Materials (BOM), wiring specifications, and configuration details needed to build the circuit.

## 1. System Overview

The system consists of:
*   **4x Feeder Units**: Each lane has a stepper motor to push/pull filament.
*   **4x Filament Sensors**: To detect filament presence in each lane.
*   **1x Cutter Mechanism**: A servo-actuated blade to cut filament before retraction.
*   **Controller**: A microcontroller (MCU) running Klipper firmware to manage the motors and sensors.

## 2. Bill of Materials (BOM)

### Core Electronics
| Component | Quantity | Description |
| :--- | :--- | :--- |
| **Microcontroller** | 1 | **Raspberry Pi Pico** (RP2040) or **BTT SKR Pico** (All-in-one solution). |
| **Stepper Drivers** | 4 | **TMC2209** (Silent, UART control) or A4988 (Cheaper, noisier). |
| **Stepper Motors** | 4 | **NEMA 14** or **NEMA 17** Stepper Motors (depending on your printed feeder design). |
| **Filament Sensors** | 4 | **Microswitches** (e.g., KW10, Omron) or **Optical Sensors**. |
| **Cutter Servo** | 1 | **MG996R** (High torque) or **MG90S** (Compact), depending on cutter resistance. |
| **Power Supply** | 1 | **24V DC PSU** (Usually shared with the main printer). |
| **Buck Converter** | 1 | **24V to 5V** (To power the Pico and Servo). |
| **Capacitors** | 4 | **100µF 35V** (Electrolytic, one for each stepper driver power input). |

### Connectors & Misc
*   Breadboard or Prototype PCB.
*   JST-XH Connectors (2.54mm) for motors/sensors.
*   22 AWG Wire for power, 26 AWG for signals.

---

## 3. Wiring Diagram / Pinout (Raspberry Pi Pico Example)

If building a custom board with a Raspberry Pi Pico, use the following pin mapping.

### Power Distribution
*   **24V PSU (+) / (-)** -> Connects to `VMOT` and `GND` on Stepper Drivers.
*   **24V PSU** -> **Buck Converter** -> **5V Output**.
*   **5V Output** -> Pico `VSYS` (Pin 39) and Servo `VCC`.
*   **Common Ground**: Connect all GNDs (Pico, PSU, Buck, Drivers) together.

### Stepper Motor Wiring (4 Lanes)
*Each driver needs: STEP, DIR, EN (Optional), VMOT, VDD (3.3V from Pico), GND.*

| Lane | Component | Pico Pin (GP) | Driver Pin |
| :--- | :--- | :--- | :--- |
| **Lane 1** | Motor 1 Step | GP2 | STEP |
| | Motor 1 Dir | GP3 | DIR |
| | Motor 1 UART | GP0 | UART_RX/TX (if using TMC2209) |
| **Lane 2** | Motor 2 Step | GP4 | STEP |
| | Motor 2 Dir | GP5 | DIR |
| | Motor 2 UART | GP1 | UART_RX/TX |
| **Lane 3** | Motor 3 Step | GP6 | STEP |
| | Motor 3 Dir | GP7 | DIR |
| | Motor 3 UART | GP8 | UART_RX/TX |
| **Lane 4** | Motor 4 Step | GP10 | STEP |
| | Motor 4 Dir | GP11 | DIR |
| | Motor 4 UART | GP9 | UART_RX/TX |
| **All** | Enable | GP12 | EN (Shared) |

### Sensor & Servo Wiring

| Component | Pico Pin (GP) | Type |
| :--- | :--- | :--- |
| **Sensor 1** | GP16 | Input (Pull-up) |
| **Sensor 2** | GP17 | Input (Pull-up) |
| **Sensor 3** | GP18 | Input (Pull-up) |
| **Sensor 4** | GP19 | Input (Pull-up) |
| **Cutter Servo** | GP20 | PWM Output |

---

## 4. The "Cutting" Mechanism

Since the mechanical cutter design is not specified in the files, you have two options:

### Option A: Toolhead Cutter (Recommended)
Most "Box Turtle" setups use a cutter mounted on the **print head** (Toolhead).
*   **Mechanism**: A lever on the toolhead hits a block on the frame (at X max) to actuate a blade.
*   **Automation**: The printer moves to X=Max, cuts the filament, then the feeder retracts it.
*   **Hardware**: No extra electronics needed (purely mechanical actuation by movement).

### Option B: Standalone Servo Cutter
If you want a dedicated cutter unit (e.g., near the feeder):
1.  **Hardware**: Mount a servo (MG996R) with a blade arm (e.g., a craft knife blade) across the filament path.
2.  **Automation**:
    *   Klipper Macro: `CUT_FILAMENT`
    *   Action: Servo rotates 90° to slice, then returns.
    *   Timing: Triggered *before* a filament change retraction sequence.

## 5. Klipper Configuration (`printer.cfg`)

Add this to your Klipper config to control the new hardware.

```ini
[mcu feeder]
serial: /dev/serial/by-id/usb-Klipper_rp2040_...

# --- Lane 1 ---
[stepper_extra lane1]
step_pin: feeder:gpio2
dir_pin: feeder:gpio3
enable_pin: !feeder:gpio12
microsteps: 16
rotation_distance: 22.6 # Calibrate this
endstop_pin: ^feeder:gpio16 # Sensor 1

# --- Cutter Servo ---
[servo cutter]
pin: feeder:gpio20
maximum_servo_angle: 180
minimum_pulse_width: 0.0005
maximum_pulse_width: 0.0025
initial_angle: 0

# --- Macros ---
[gcode_macro CUT_FILAMENT]
gcode:
    SET_SERVO SERVO=cutter ANGLE=90
    G4 P500 ; Wait 500ms
    SET_SERVO SERVO=cutter ANGLE=0
    G4 P500
    SET_SERVO SERVO=cutter WIDTH=0 ; Turn off servo
```

## 6. Automation Logic

To "fully automate" the color change:
1.  **Slicer**: Configure your slicer (OrcaSlicer/PrusaSlicer) to insert `T0`, `T1`, etc., on color changes.
2.  **Klipper Macros**:
    *   `T0`: Checks if filament is loaded. If yes, unloads current. Loads Lane 1.
    *   `Unload`: Calls `CUT_FILAMENT`, then retracts motor.
    *   `Load`: Feeds motor until toolhead sensor triggers.

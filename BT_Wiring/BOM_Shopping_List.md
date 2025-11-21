# Box Turtle Electronics BOM & Shopping List

This list corresponds to the "Pico Shield" design found in `BoxTurtle_Pico_Shield.fz`.

# Box Turtle Electronics BOM & Shopping List

This project supports two variants:
1.  **Basic**: Standard Raspberry Pi Pico, core feeding functionality.
2.  **Extended**: Raspberry Pi Pico W, WiFi/Bluetooth, OLED Display, I2C Sensors.

## 1. Core Components (Choose One Variant)

### Variant A: Basic
| Component | Quantity | Description | Notes |
| :--- | :--- | :--- | :--- |
| **Raspberry Pi Pico** | 1 | Standard RP2040 | Soldered headers required. |
| **Stepper Drivers** | 4 | TMC2209 or A4988 | SilentStepStick footprint. |
| **Buck Converter** | 1 | 24V to 5V (3A) | e.g., LM2596 Module. |

### Variant B: Extended (WiFi + Display)
| Component | Quantity | Description | Notes |
| :--- | :--- | :--- | :--- |
| **Raspberry Pi Pico W** | 1 | RP2040 with WiFi/BT | **Required** for Web UI. |
| **Stepper Drivers** | 4 | TMC2209 (UART) | Recommended for silence. |
| **Buck Converter** | 1 | 24V to 5V (3A) | e.g., LM2596 Module. |
| **OLED Display** | 1 | 0.96" I2C (SSD1306) | Status Monitor. |
| **I2C Pull-ups** | 2 | 4.7kΩ Resistors | Required for I2C bus. |

## 2. PCB Connectors (Through-Hole)
These parts are soldered onto the PCB Shield.

| Component | Quantity | Description | Usage |
| :--- | :--- | :--- | :--- |
| **Female Header (40-pin)** | 2 strips | 2.54mm Pitch | Cut to size for Pico (2x20 pins). |
| **Female Header (8-pin)** | 8 strips | 2.54mm Pitch | For Stepper Drivers (2 strips per driver). |
| **JST-XH Connector (4-pin)** | 6 | 2.54mm Right Angle | 4x Motors, 1x I2C Exp, 1x Display. |
| **JST-XH Connector (3-pin)** | 5 | 2.54mm Right Angle | 4x Sensors, 1x Servo. |
| **Screw Terminal (2-pin)** | 1 | 5.08mm Pitch | Main 24V Power Input. |

## 3. Passive Components (Safety & Stability)
**Critical for reliable operation.**

| Component | Quantity | Description | Usage |
| :--- | :--- | :--- | :--- |
| **Electrolytic Capacitor** | 4 | 100µF 35V (or 50V) | **REQUIRED**. Place across VMOT/GND for each driver. |
| **Resistor** | 2 | 4.7kΩ (1/4W) | I2C Pull-ups (SDA, SCL). |
| **Resistor** | 1 | 330Ω - 1kΩ (1/4W) | Current limiting for Power LED. |
| **LED** | 1 | 3mm or 5mm (Green) | Power Indicator (5V rail). |

## 4. Off-Board Hardware (Cables & Actuators)
| Component | Quantity | Description |
| :--- | :--- | :--- |
| **Stepper Motors** | 4 | NEMA 14 (Round) | Ensure cable matches JST-XH 4-pin. |
| **Microswitches** | 4 | Omron D2HW-C201H | Sealed, Long Lever. Wired to JST-XH 3-pin. |
| **Servo** | 1 | MG996R / MG90S | Standard 3-pin connector. |
| **Power Supply** | 1 | 24V DC | From Printer PSU. |
| **Display (Optional)** | 1 | OLED (I2C) or Nextion (UART) | Connects to Expansion ports. |
| **Env Sensor (Optional)** | 1 | BME280 / AHT10 | Connects to I2C Port. |

## 5. Optional / Misc
*   **PCB**: 100x80mm Prototype Board or Custom PCB (from Gerber).
*   **Fuse Holder**: Inline fuse holder for 24V input (Recommended: 5A).
*   **Display**: 0.96" I2C OLED (SSD1306) - Connects to I2C Port.
*   **Mounting**: 3D Printed Case (See `CAD/Shield_Mount.scad`).

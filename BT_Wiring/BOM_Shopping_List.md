# Box Turtle Electronics BOM & Shopping List

This list corresponds to the "Pico Shield" design found in `BoxTurtle_Pico_Shield.fz`.

## 1. Core Components
| Component | Quantity | Description | Notes |
| :--- | :--- | :--- | :--- |
| **Raspberry Pi Pico** | 1 | Microcontroller | Soldered headers required. |
| **Stepper Drivers** | 4 | TMC2209 or A4988 | SilentStepStick footprint. |
| **Buck Converter** | 1 | 24V to 5V (3A) | e.g., LM2596 Module. |

## 2. PCB Connectors (Through-Hole)
These parts are soldered onto the PCB Shield.

| Component | Quantity | Description | Usage |
| :--- | :--- | :--- | :--- |
| **Female Header (40-pin)** | 2 strips | 2.54mm Pitch | Cut to size for Pico (2x20 pins). |
| **Female Header (8-pin)** | 8 strips | 2.54mm Pitch | For Stepper Drivers (2 strips per driver). |
| **JST-XH Connector (4-pin)** | 6 | 2.54mm Right Angle | 4x Motors, 1x I2C Exp, 1x Display. |
| **JST-XH Connector (3-pin)** | 5 | 2.54mm Right Angle | 4x Sensors, 1x Servo. |
| **Screw Terminal (2-pin)** | 1 | 5.08mm Pitch | Main 24V Power Input. |

## 3. Off-Board Hardware (Cables & Actuators)
| Component | Quantity | Description |
| :--- | :--- | :--- |
| **Stepper Motors** | 4 | NEMA 14 or 17 | Ensure cable matches JST-XH 4-pin. |
| **Microswitches** | 4 | KW10 / Omron | Wired to JST-XH 3-pin (GND, Sig). |
| **Servo** | 1 | MG996R / MG90S | Standard 3-pin connector. |
| **Power Supply** | 1 | 24V DC | From Printer PSU. |
| **Display (Optional)** | 1 | OLED (I2C) or Nextion (UART) | Connects to Expansion ports. |
| **Env Sensor (Optional)** | 1 | BME280 / AHT10 | Connects to I2C Port. |

## 4. Optional / Misc
*   **Capacitors**: 4x 100µF 35V Electrolytic (Place near each driver's VMOT pin).
*   **PCB**: 100x80mm Prototype Board or Custom PCB (from Gerber).

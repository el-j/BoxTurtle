# Box Turtle Scripts

This directory contains utility scripts for generating hardware designs and managing the project.

## Scripts

### `generate_shield_v4.py`
**Purpose**: Generates the Fritzing (`.fz`) project file for the Box Turtle Pico Shield v2.
**Output**: `BT_Wiring/BoxTurtle_Pico_Shield_v2.fz`

**Usage**:
```bash
python3 scripts/generate_shield_v4.py
```

**Version History**:
*   **v4**: Added safety capacitors (100uF), I2C pull-up resistors, Power LED, and Screw Terminals.
*   **v3**: Initial Shield design with NEMA 14 and Omron D2HW labels.
*   **v2**: Basic wiring generation.

## Requirements
*   Python 3.x

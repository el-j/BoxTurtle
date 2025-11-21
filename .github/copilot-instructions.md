# BoxTurtle Repository Instructions

This repository hosts 3D printing files, CAD designs, electronics specifications, and control logic for "Box Turtle" modifications. While primarily a hardware design repository, it includes firmware configuration and logic definitions.

## Project Structure & Architecture
- **Nature**: Hardware modifications, CAD assets, and electronics design for the Box Turtle project.
- **Key Directories**:
  - `CAD/`: Engineering source files (STEP, Fusion 360) for parts like mounts and tools.
  - `STLs/`: 3D printable mesh files, organized by component (Extruder, Skirts, etc.).
  - `BT_Wiring/`: Wiring diagrams, Fritzing PCB designs (`.fz`), and BOMs.
- **Key Files**:
  - `electronics_design.md`: Comprehensive guide for electronics, BOM, and Klipper pinouts.
  - `BT_Wiring/BoxTurtle_Pico_Shield_v2.fz`: Fritzing project file for the custom PCB shield (Pico + 4x Drivers).
  - `BT_Wiring/BOM_Shopping_List.md`: Specific BOM for the PCB shield components.
  - `feeder_control.xml`: PLCopen XML definition for the feeder control logic.

## AI Agent Guidelines

### 1. Binary & CAD File Handling
-   **Read-Only**: You cannot read or edit `.f3d`, `.step`, `.stp`, `.stl`, `.3mf`, `.lbrn2`, or `.fz` files directly.
-   **Inference**: Rely on filenames and parent directory `README.md` files to understand the purpose of binary assets.
-   **No Edits**: Do not suggest code edits for these binary formats.

### 2. Electronics & Firmware
-   **PCB Design**: The `BT_Wiring/*.fz` files define the custom shield layout. Use `BT_Wiring/BOM_Shopping_List.md` for component sourcing.
-   **Klipper**: The project uses Klipper firmware. Refer to `electronics_design.md` for pin mappings (Raspberry Pi Pico/SKR Pico) and wiring.
-   **Control Logic**: `feeder_control.xml` defines the state machine (IDLE, CUTTING, etc.). Treat this as the reference for logical behavior, even if the implementation is in Klipper macros.

### 3. Documentation & BOMs
-   **Source of Truth**: The documentation (`*.md`) is the primary "source code" for assembly and configuration.
-   **BOM Management**: Pay close attention to Bill of Materials in `BT_BOM.md`, `electronics_design.md`, and `BT_Wiring/BOM_Shopping_List.md`. Ensure consistency between these files.
-   **Attribution**: Always preserve community attributions (e.g., "Projects from Dad's Garage", "Boothy") when summarizing.

### 4. Workflows
-   **"Building"**: Refers to physical assembly, 3D printing, or wiring.
-   **Validation**: Cross-reference `electronics_design.md` against `feeder_control.xml` to ensure hardware capabilities match logical requirements.
-   **Scripting**: You may be asked to generate Python scripts for file management or Klipper macros based on the XML logic.

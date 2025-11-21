# Welcome to Box Turtle Feeder

**The Open Source, 4-Lane Filament Changer for Klipper.**

This documentation covers the **Custom Pico Shield v2** build of the Box Turtle. This version uses a Raspberry Pi Pico (or Pico W) to control 4 stepper motors, 4 filament sensors, and a cutter servo, providing a robust and "AMS-like" experience for your Voron or Klipper printer.

## Project Overview

*   **Hardware**: 4x NEMA 14 Steppers, Custom PCB Shield, 3D Printed Feeder Units.
*   **Firmware**: Custom Rust-based firmware (Embassy framework) for high-performance, async control.
*   **Software**: Integrates with Klipper via USB Serial.

## Getting Started

Follow these guides in order to build your system:

1.  [**Hardware Assembly**](./hardware_assembly.md)
    *   Printing the parts.
    *   Building the "Pico Shield v2" electronics.
    *   Wiring the motors and sensors.
2.  [**Firmware Setup**](./firmware_setup.md)
    *   Choosing a variant (Basic vs. Extended).
    *   Flashing the Raspberry Pi Pico.
3.  [**Configuration**](./configuration.md)
    *   Setting up Klipper (`printer.cfg`).
    *   Defining Macros for color changing.
4.  [**User Manual**](./user_manual.md)
    *   Loading filament.
    *   Troubleshooting.
5.  [**Credits**](./credits.md)
    *   Acknowledgements for the original creators and contributors.

## Resources

*   [GitHub Repository](https://github.com/el-j/BoxTurtle)
*   [Discord Community](https://discord.gg/eT8zc3bvPR)

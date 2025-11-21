# Box Turtle Firmware (Rust/Embassy)

This directory contains the custom firmware for the Box Turtle 4-Lane Feeder, designed to run on a **Raspberry Pi Pico (RP2040)** mounted on the **Box Turtle Pico Shield v2**.

It is written in **Rust** using the **Embassy** framework for efficient, asynchronous control of the 4 stepper motors and sensors.

## Hardware Support
This firmware is configured for the **Box Turtle Pico Shield v2** (`../BT_Wiring/BoxTurtle_Pico_Shield_v2.fz`).

*   **MCU**: Raspberry Pi Pico
*   **Motors**: 4x Stepper Drivers (A4988/TMC2209) on Pins GP2-GP11.
*   **Sensors**: 4x Filament Switches (Omron D2HW) on Pins GP16-GP19.
*   **Servo**: Cutter Servo on GP20.
*   **Expansion**: I2C (GP14/15) and Aux (GP21/22) enabled.

## Prerequisites
1.  **Rust Toolchain**: Install Rust via [rustup.rs](https://rustup.rs/).
2.  **Thumbv6m Target**: `rustup target add thumbv6m-none-eabi`
3.  **Probe-rs**: `cargo install probe-rs --features cli` (for flashing).
4.  **Flip-Link**: `cargo install flip-link` (recommended linker).

## Building & Flashing

### 1. Build
```bash
cargo build --release
```

### 2. Flash (via Debug Probe)
If you have a debug probe (Picoprobe, CMSIS-DAP):
```bash
cargo run --release
```

### 3. Flash (via USB Bootloader)
If you don't have a probe, convert to UF2:
1.  Install `elf2uf2-rs`: `cargo install elf2uf2-rs`
2.  Hold BOOTSEL on Pico and plug in USB.
3.  Run:
    ```bash
    cargo build --release
    elf2uf2-rs target/thumbv6m-none-eabi/release/box_turtle_firmware
    ```
    *(Note: You may need to mount the Pico as a drive first)*

## Architecture
*   `src/main.rs`: Implements the State Machine (IDLE -> LOADING -> CUTTING -> UNLOADING) derived from `feeder_control.xml`.
*   `src/pico_hardware.rs`: Hardware Abstraction Layer (HAL) defining the specific pinout for the Shield v2.

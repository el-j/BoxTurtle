---
layout: default
title: Firmware Setup
---

# Firmware Setup Guide

The Box Turtle uses custom Rust firmware for high-performance control.

## Prerequisites
*   A computer with the Rust toolchain installed ([rustup.rs](https://rustup.rs)).
*   A USB-C cable.

## Step 1: Choose Your Variant

*   **Basic**: Standard USB control.
*   **Extended**: WiFi/Bluetooth enabled (requires Pico W).

## Step 2: Build the Firmware

1.  Open a terminal in the `firmware/` directory.
2.  Run the build command:

    **For Basic:**
    ```bash
    cargo build --release
    ```

    **For Extended (Pico W):**
    ```bash
    cargo build --release --features pico-w
    ```

## Step 3: Flash the Pico

1.  Unplug the Pico from USB.
2.  Hold down the **BOOTSEL** button on the Pico.
3.  Plug the Pico into your computer while holding the button.
4.  Release the button. A drive named `RPI-RP2` should appear.
5.  Run the flash tool (requires `elf2uf2-rs`):

    ```bash
    cargo install elf2uf2-rs
    elf2uf2-rs target/thumbv6m-none-eabi/release/box_turtle_firmware
    ```

    *Alternatively, copy the `.uf2` file from `target/thumbv6m-none-eabi/release/` to the `RPI-RP2` drive manually.*

## Step 4: Verify

Once flashed, the **Green LED** on the Pico (or Shield) should start blinking (Heartbeat). This indicates the firmware is running and waiting for commands.

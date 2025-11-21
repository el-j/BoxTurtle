# User Manual

## Loading Filament

1.  **Insert**: Push the filament into the input of Lane 1 (or 2, 3, 4).
2.  **Detect**: The firmware will detect the filament via the Omron switch.
3.  **Auto-Load**: If configured, the motor will automatically grab the filament and feed it to the buffer (TurtleNeck).
    *   *Note: This behavior depends on your specific macro configuration.*

## Unloading Filament

1.  **Command**: Issue a tool change command (e.g., `T1` to switch to Lane 2).
2.  **Cut**: The system will first actuate the **Cutter Servo** to slice the filament in the current lane.
3.  **Retract**: The motor will reverse to pull the filament back onto the spool.

## Troubleshooting

### Motor Stalls / Clicking
*   **Check Current**: Ensure the stepper driver VREF is set correctly for NEMA 14 motors (usually around 0.5V - 0.7V).
*   **Check Path**: Ensure the PTFE tubes are not kinked and the filament path is smooth.

### Sensor Not Triggering
*   **Check Wiring**: Verify the 3-pin JST connector is seated.
*   **Check Switch**: Ensure the lever on the Omron switch is physically being pressed by the filament. You may need to adjust the printed part.

### WiFi Issues (Extended Variant)
*   **Check LED**: If the LED is not blinking, the firmware might be stuck connecting.
*   **Check Credentials**: Ensure your WiFi SSID and Password are correct in the firmware configuration (requires recompiling).

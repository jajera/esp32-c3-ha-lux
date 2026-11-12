---
inclusion: always
---

# Product

ESP32-C3 lux node for Home Assistant: VEML7700 ambient light, a binary LED (on/off only), and an ST7789 that shows live lux and the active control mode.

It onboards like a consumer device: no home Wi‑Fi in the firmware; setup is QR on the screen (SoftAP + captive portal). Firmware also enables Improv BLE/serial but the docs do not walk those paths. Credentials and mode settings persist in NVS across reboots. Factory reset (BOOT held 5 s, or the HA button) clears prefs only, so the same binary stays on the device.

## Control modes

HA `select` **Mode**, default **Off**. Config is set from Home Assistant and stored on the ESP32; Schedule and Night keep running while disconnected.

| Mode | Meaning |
|------|---------|
| **Off** (default) | Automatic mechanisms off. LED only changes from HA on/off (including ad‑hoc scripts/scenes/voice). |
| **Schedule** | On-device daily start/end window (local clock). Supports windows that cross midnight. |
| **Night** | On-device lux hysteresis: on below dark threshold, off above bright threshold. |

Ad‑hoc control is **Off**, not a fourth mode.

## Display

ST7789 run page: Wi‑Fi status, live lux (`lx`), mode label (`Off` / `Schedule` / `Night`), LED on/off, IP. Setup page: SoftAP QR. HA **Display** switch controls the backlight.

Tutorial: walk through the code → build image → wire and validate → flash → configure and test. Host: Ubuntu 24.04.

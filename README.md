# ESP32-C3 HA lux

An ambient light sensor and binary LED for Home Assistant, built from an ESP32-C3, a VEML7700, and an ST7789 screen running ESPHome.

It sets up like a store-bought device: scan the QR code on its screen to connect it to Wi‑Fi, and Home Assistant finds it. Mode, schedule, and night lux thresholds are set from Home Assistant and stored on the device, so Schedule and Night keep working while disconnected. Holding **BOOT** for 5 seconds resets it to setup mode. No Wi‑Fi password is stored in the firmware or this repo.

Tutorial: [esp32-c3-ha-lux.johna.kiwi](https://esp32-c3-ha-lux.johna.kiwi/)

1. [Walk through the code](docs/01-walkthrough/index.md)
2. [Build the image](docs/02-build-image.md)
3. [Wire and validate](docs/03-wire/index.md)
4. [Flash the ESP32](docs/04-flash-esp32.md)
5. [Configure and test](docs/05-configure-and-test.md)

Wiring: [docs/03-wire/](docs/03-wire/index.md). Firmware: [`firmware/lux.yaml`](firmware/lux.yaml).

## Icons and logos

The docs use a few brand marks as inline icons. Copies live in `overrides/.icons/brands/`, with their source and terms in `SOURCE.txt` there. Home Assistant and ESPHome are trademarks of the Open Home Foundation, and Ubuntu is a trademark of Canonical Ltd. They are used here to identify the products, and are not relicensed under this repo's license.

## Preview the docs

```bash
/usr/bin/python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-docs.txt
.venv/bin/python -m zensical serve
```

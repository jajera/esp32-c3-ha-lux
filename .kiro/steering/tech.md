---
inclusion: always
---

# Tech

Ubuntu 24.04, Python 3.14 (`/usr/bin/python3.14`; ESPHome supports 3.12–3.14). Docs: Zensical + patina. Firmware: ESPHome for ESP32-C3 DevKit.

Flash through the USB serial port (typically `/dev/ttyACM0`).

Pins (ESP32-C3 DevKit):

- I2C: SDA **4**, SCL **5** (VEML7700 at **0x10**)
- LED (binary light): **GPIO6**
- SPI display: SCK **1**, MOSI **0**, CS **10**, DC **3**, RST **7**, backlight **21**
- GPIO9 (BOOT): factory reset long-press; don’t wire anything else to it
- Avoid 18/19 (USB Serial/JTAG) and other strapping pins for general I/O

Timezone for Schedule: `Pacific/Auckland` in `firmware/lux.yaml` substitutions (change if needed).

```bash
.venv/bin/esphome compile firmware/lux.yaml
.venv/bin/esphome upload firmware/lux.yaml --device /dev/ttyACM0
```

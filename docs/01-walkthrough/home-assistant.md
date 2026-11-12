# Home Assistant

How the device talks to Home Assistant and how it gets updates later.

```yaml
api:
  encryption: {}

ota:
  - platform: esphome

dashboard_import:
  package_import_url: github://jajera/esp32-c3-ha-lux/firmware/lux.yaml@main
  import_full_config: true
```

| Key | What it does |
|-----|--------------|
| `api` | Native link to Home Assistant — no MQTT broker |
| `ota` | Over-the-air updates after the first USB flash |
| `dashboard_import` | Lets the ESPHome dashboard pull this file from GitHub when you adopt the device. Safe to ignore if you only flash from this repo |

!!! note "Where the encryption key comes from"
    `encryption: {}` turns encryption on without baking a key into the file. Home Assistant creates the key when you add the device and stores it on the board. A [factory reset](reset.md) clears that key along with the saved Wi‑Fi and mode settings.

Once adopted, the device shows entities from the later blocks:

| Entity | Type | Comes from |
|--------|------|------------|
| Illuminance | Sensor | [Lux and LED](lux-led.md) |
| LED | Light | [Lux and LED](lux-led.md) |
| Mode, Schedule Start/End, night lux | Select / time / numbers | [Modes](modes.md) |
| Display | Switch | [Display](display.md) |
| Factory Reset, Restart | Buttons | [Factory reset](reset.md) |
| WiFi Signal, Uptime, Mode Label | Diagnostic | [Lux and LED](lux-led.md) / [Modes](modes.md) |

**Next:** [Wi‑Fi setup](wifi.md)

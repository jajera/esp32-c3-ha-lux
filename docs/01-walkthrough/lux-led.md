# Lux and LED

The VEML7700 reports illuminance over I2C. The LED is a binary light: on or off, no brightness. Two more sensors watch the device itself for the screen and diagnostics.

```yaml
i2c:
  sda: GPIO4
  scl: GPIO5
  scan: true

sensor:
  - platform: veml7700
    address: 0x10
    update_interval: 5s
    ambient_light:
      name: Illuminance
      id: lux_lx
      unit_of_measurement: lx
      accuracy_decimals: 0
      filters:
        - clamp:
            min_value: 0
            max_value: 120000

  - platform: wifi_signal
    id: wifi_rssi_db
    name: WiFi Signal
    entity_category: diagnostic
    update_interval: 10s

  - platform: uptime
    name: Uptime
    entity_category: diagnostic

text_sensor:
  - platform: wifi_info
    ip_address:
      id: wifi_ip
      internal: true
    ssid:
      id: wifi_ssid_ts
      internal: true
```

## Pins

| Signal | Pin | Wired in |
|--------|-----|----------|
| SDA | **GPIO4** | [VEML7700](../03-wire/veml7700.md) |
| SCL | **GPIO5** | [VEML7700](../03-wire/veml7700.md) |

`scan: true` prints every I2C address found at boot. After flash, the log should show `0x10` — see [Flash the ESP32](../04-flash-esp32.md).

| Key | What it does |
|-----|--------------|
| `address: 0x10` | Usual VEML7700 address |
| `update_interval: 5s` | Reads lux every five seconds |
| `ambient_light` | Lux reading. `name` is what Home Assistant shows; `id` feeds Night mode and the screen |
| `accuracy_decimals: 0` | Whole lux only |
| `clamp` | Keeps values between 0 and 120000 lx |

## Binary LED

```yaml
output:
  - platform: gpio
    id: led_gpio
    pin: GPIO6

light:
  - platform: binary
    name: LED
    id: led_light
    output: led_gpio
    restore_mode: RESTORE_DEFAULT_OFF
```

| Pin | Role | Wired in |
|-----|------|----------|
| GPIO6 | LED output | [LED](../03-wire/led.md) |

A `binary` light has only on and off — no brightness slider. `RESTORE_DEFAULT_OFF` restores the last LED state after reboot, or starts off if nothing was saved.

## What appears in Home Assistant

| Entity | Where | Used on screen as |
|--------|-------|-------------------|
| Illuminance | Main, whole lx | `lux_lx` |
| LED | Main light | LED bulb icon |
| WiFi Signal | **Diagnostic** | `wifi_rssi_db` (dBm + strength icon) |
| Uptime | **Diagnostic** | — |
| SSID / IP (`wifi_info`) | Internal only | `wifi_ssid_ts` / `wifi_ip` on the run page |

Each `name` becomes an entity. Each `id` lets other blocks (the [display](display.md), [modes](modes.md)) read the value. `entity_category: diagnostic` keeps signal and uptime out of the main list. The `wifi_info` text sensors stay `internal` so they feed the screen without cluttering Home Assistant.

## Who controls the LED

| Mode | What changes the LED |
|------|----------------------|
| **Off** | Only Home Assistant (the LED entity, and any script / scene / voice that calls it) |
| **Schedule** | The on-device script, from the local clock |
| **Night** | The on-device script, from lux |

In **Schedule** or **Night**, a Home Assistant toggle still works as a short override until the next 15 s evaluation. To keep a manual state, set Mode to **Off**. Details are in [Modes](modes.md).

**Next:** [Modes](modes.md)

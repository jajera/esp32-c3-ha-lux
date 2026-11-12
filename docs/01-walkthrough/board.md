# ESP32

The top of the file names the device and describes the board. A few variables are reused later for the setup hotspot, QR code, and Schedule timezone.

## Name and substitutions

```yaml
substitutions:
  name: esp32-c3-ha-lux
  friendly_name: ESP32-C3 HA Lux
  ap_ssid: Lux Setup
  ap_password: setup1234
  timezone: Pacific/Auckland

esphome:
  name: ${name}
  friendly_name: ${friendly_name}
  name_add_mac_suffix: true
  project:
    name: jajera.esp32-c3-ha-lux
    version: "1.0.0"
  on_boot:
    priority: -100
    then:
      - if:
          condition:
            lambda: return !wifi::global_wifi_component->has_sta();
          then:
            - display.page.show: page_setup
```

`${name}` and the other substitutions are filled in wherever they appear later in the file.

| Key | What it does |
|-----|--------------|
| `ap_ssid` / `ap_password` | Setup hotspot only (`Lux Setup` / `setup1234`). **Not** your home Wi‑Fi. Same values go into the QR code |
| `timezone` | Used by SNTP so **Schedule** uses the right local clock |
| `name_add_mac_suffix` | Appends the end of the MAC address, e.g. `esp32-c3-ha-lux-a1b2c3`, so several boards don't clash |
| `project` | Tags the binary so Home Assistant can show where the config came from |
| `on_boot` | After Wi‑Fi has loaded NVS: show the QR only when no home network is saved (see [Wi‑Fi setup](wifi.md)) |

!!! note "The hotspot password is not a secret"
    It is in the QR code and in this repo. It only opens the setup page while the device has no network.

## Board and log

```yaml
esp32:
  board: esp32-c3-devkitm-1
  framework:
    type: esp-idf

logger:
```

| Key | What it does |
|-----|--------------|
| `esp32` | ESP32-C3 DevKitM-1 class board |
| `framework: esp-idf` | Espressif's native framework (needed for this display stack) |
| `logger` | Serial log over USB — what you watch in the [flash step](../04-flash-esp32.md) |

## Time

```yaml
time:
  - platform: sntp
    id: sntp_time
    timezone: ${timezone}
```

When the device is online, SNTP keeps the clock accurate. **Schedule** uses that clock on the device, including after Wi‑Fi drops, for as long as the board stays powered. There is no battery-backed clock: after a cold boot with no network, Schedule waits until a time server is reachable again.

**Next:** [Home Assistant](home-assistant.md)

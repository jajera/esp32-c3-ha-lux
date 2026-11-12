# Agent notes

Lux node: ESP32-C3 + VEML7700 + binary LED + ST7789 → Home Assistant via ESPHome. Docs in Zensical. Firmware: `firmware/lux.yaml`. Demo host: Ubuntu 24.04.

Read `.kiro/steering/` first. Docs flow: walk through the code → build image → wire and validate → flash ESP32 → configure and test.

```bash
.venv/bin/esphome compile firmware/lux.yaml
.venv/bin/python -m zensical serve
```

`requirements.txt` is ESPHome (for readers); `requirements-docs.txt` is the docs site (for CI and authors).

Don’t flash unless asked and a serial port is there. No Wi‑Fi passwords, API keys, or HA tokens in git. Config (mode, schedule, lux thresholds) persists in NVS across reboots; factory reset clears prefs only (same binary).

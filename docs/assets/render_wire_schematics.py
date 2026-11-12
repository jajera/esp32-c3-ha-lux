"""Step wiring schematics (SVG) for Wire pages — VEML7700, LED, and display.

Same look as the climate tutorial schematics:
  3V3 = red, GND = black, I2C/SPI signals each their own colour.
Only the wires added in that step are drawn; later pins are greyed.

Regenerate from docs/assets/:
  python3 render_wire_schematics.py
"""

INK = "#1c1e20"
MUTED = "#6e7376"
BG = "#f5f5f2"
RED = "#c0392b"      # 3V3
BLK = "#2b2d2f"      # GND
C_SCL = "#1f8a70"    # I2C SCL (teal)
C_SDA = "#2e86de"    # I2C SDA (blue)
C_SCK = "#e67e22"    # SPI SCK  (orange)
C_MOSI = "#8e44ad"   # SPI MOSI (purple)
C_CS = "#16a085"     # SPI CS   (green-teal)
C_DC = "#5c6bc0"     # SPI DC   (indigo)
C_RES = "#f1c40f"    # SPI RST  (yellow)
C_BL = "#7f8c8d"     # backlight PWM
C_LED = "#f39c12"    # LED GPIO
C3_ACCENT = "#4a6078"
VEML_ACCENT = "#1f8a70"
LED_ACCENT = "#f39c12"
TFT_ACCENT = "#e67e22"

FONT = "DejaVu Sans, sans-serif"
ROW_H = 40


def block(x, y, w, pins, title, accent, dim=()):
    """pins: list of names. dim: names drawn greyed (present but unused)."""
    h = ROW_H * len(pins) + 50
    parts = [
        f'<rect x="{x+4}" y="{y+5}" width="{w}" height="{h}" rx="12" fill="#e1e1dd"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#ffffff" '
        f'stroke="{accent}" stroke-width="3"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="36" rx="12" fill="{accent}"/>',
        f'<rect x="{x}" y="{y+20}" width="{w}" height="16" fill="{accent}"/>',
        f'<text x="{x+w/2}" y="{y+25}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="18" font-weight="700" fill="#ffffff">{title}</text>',
    ]
    pin_y = {}
    for i, p in enumerate(pins):
        py = y + 50 + i * ROW_H + ROW_H / 2
        pin_y[p] = py
        col = "#b9bdbf" if p in dim else INK
        parts.append(f'<text x="{x+w/2}" y="{py+5}" text-anchor="middle" '
                     f'font-family="{FONT}" font-size="16" fill="{col}">{p}</text>')
    return "".join(parts), pin_y, h


def render(out, title, sub, host_pins, host_title, host_accent, dev_name, dev_accent,
           dev_pins, dev_dim, nets, footer, legend=((RED, "3V3"), (BLK, "GND"))):
    W = 940
    hx, hw = 70, 230
    devx, devw = 640, 230
    top = 150

    host_svg, hy, hh = block(hx, top, hw, host_pins, host_title, host_accent)
    dev_svg, dy, dh = block(devx, top, devw, dev_pins, dev_name, dev_accent, dev_dim)
    H = top + max(hh, dh) + 90

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="{title}">',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        f'<text x="48" y="52" font-family="{FONT}" font-size="27" '
        f'font-weight="700" fill="{INK}">{title}</text>',
        f'<text x="50" y="82" font-family="{FONT}" font-size="15" '
        f'fill="{MUTED}">{sub}</text>',
    ]
    lx = 50
    for col, lab in legend:
        parts.append(f'<rect x="{lx}" y="108" width="26" height="6" rx="3" fill="{col}"/>')
        parts.append(f'<text x="{lx+32}" y="116" font-family="{FONT}" '
                     f'font-size="14" fill="{INK}">{lab}</text>')
        lx += 32 + len(lab) * 8 + 24

    for src, dpin, col in nets:
        sy = hy[src]
        dest_y = dy[dpin]
        sx = hx + hw
        dx = devx
        midx = (sx + dx) / 2
        parts.append(f'<path d="M {sx} {sy} C {midx} {sy}, {midx} {dest_y}, {dx} {dest_y}" '
                     f'fill="none" stroke="{col}" stroke-width="4"/>')
        parts.append(f'<circle cx="{sx}" cy="{sy}" r="5" fill="{col}"/>')
        parts.append(f'<circle cx="{dx}" cy="{dest_y}" r="5" fill="{col}"/>')

    parts += [host_svg, dev_svg]
    parts.append(f'<text x="50" y="{H-26}" font-family="{FONT}" font-size="14" '
                 f'fill="{MUTED}">{footer}</text>')
    parts.append("</svg>")

    with open(out, "w") as f:
        f.write("\n".join(parts))
    print("ok ->", out)


# --- VEML7700 power ---------------------------------------------------------
render(
    out="wiring-veml7700-power.svg",
    title="VEML7700 — power",
    sub="Two wires from the breadboard rails. Leave SDA and SCL open for now.",
    host_pins=["3V3", "GND"],
    host_title="ESP32-C3",
    host_accent=C3_ACCENT,
    dev_name="VEML7700",
    dev_accent=VEML_ACCENT,
    dev_pins=["VIN", "3Vo", "GND", "SCL", "SDA"],
    dev_dim=["3Vo", "SCL", "SDA"],
    nets=[("3V3", "VIN", RED), ("GND", "GND", BLK)],
    footer="Take 3V3 / GND from the rails. Leave 3Vo open — it is a 3.3 V output, not an input.",
)

# --- VEML7700 I2C -----------------------------------------------------------
render(
    out="wiring-veml7700-i2c.svg",
    title="VEML7700 — I2C data",
    sub="Two data wires. Power from the previous step stays on. 3Vo still open.",
    host_pins=["GPIO4", "GPIO5"],
    host_title="ESP32-C3",
    host_accent=C3_ACCENT,
    dev_name="VEML7700",
    dev_accent=VEML_ACCENT,
    dev_pins=["VIN", "3Vo", "GND", "SCL", "SDA"],
    dev_dim=["VIN", "3Vo", "GND"],
    nets=[("GPIO4", "SDA", C_SDA), ("GPIO5", "SCL", C_SCL)],
    footer="Both wires or neither. Address 0x10. Do not join these to the display SPI pins.",
    legend=((C_SDA, "SDA"), (C_SCL, "SCL")),
)

# --- LED --------------------------------------------------------------------
render(
    out="wiring-led.svg",
    title="LED — GPIO6",
    sub="One GPIO wire (and cathode to GND). Sensor I2C stays on.",
    host_pins=["GPIO6", "GND"],
    host_title="ESP32-C3",
    host_accent=C3_ACCENT,
    dev_name="LED",
    dev_accent=LED_ACCENT,
    dev_pins=["Anode", "Cathode"],
    dev_dim=(),
    nets=[("GPIO6", "Anode", C_LED), ("GND", "Cathode", BLK)],
    footer="Use a series resistor with a discrete LED. On-board GPIO LEDs: change the pin in firmware.",
    legend=((C_LED, "GPIO6"), (BLK, "GND")),
)

# --- Display power (+ BL pin) -----------------------------------------------
render(
    out="wiring-display-power.svg",
    title="Display — power",
    sub="Three wires. VEML7700 and LED stay on. Leave the SPI pins open for now.",
    host_pins=["3V3", "GND", "GPIO21"],
    host_title="ESP32-C3",
    host_accent=C3_ACCENT,
    dev_name="ST7789 240\u00d7240",
    dev_accent=TFT_ACCENT,
    dev_pins=["VCC", "GND", "BL", "SCL", "SDA", "RST", "DC", "CS"],
    dev_dim=["SCL", "SDA", "RST", "DC", "CS"],
    nets=[("3V3", "VCC", RED), ("GND", "GND", BLK), ("GPIO21", "BL", C_BL)],
    footer="Wire BL to GPIO21 now. The panel stays dark until you flash. Greyed pins are SPI — next.",
    legend=((RED, "3V3"), (BLK, "GND"), (C_BL, "BL")),
)

# --- Display SPI ------------------------------------------------------------
render(
    out="wiring-display-spi.svg",
    title="Display — SPI",
    sub="Five SPI wires. Power, BL, VEML7700 I2C, and LED stay on.",
    host_pins=["GPIO1", "GPIO0", "GPIO10", "GPIO3", "GPIO7"],
    host_title="ESP32-C3",
    host_accent=C3_ACCENT,
    dev_name="ST7789 240\u00d7240",
    dev_accent=TFT_ACCENT,
    dev_pins=["VCC", "GND", "BL", "SCL", "SDA", "RST", "DC", "CS"],
    dev_dim=["VCC", "GND", "BL"],
    nets=[("GPIO1", "SCL", C_SCK), ("GPIO0", "SDA", C_MOSI),
          ("GPIO10", "CS", C_CS), ("GPIO3", "DC", C_DC), ("GPIO7", "RST", C_RES)],
    footer="All five or the panel stays blank. Do not join TFT SDA to VEML7700 SDA.",
    legend=((C_SCK, "SCK"), (C_MOSI, "MOSI"), (C_CS, "CS"),
            (C_DC, "DC"), (C_RES, "RST")),
)

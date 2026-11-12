"""Schematic wiring diagram (SVG) for the Wire / Validate pages.

ESP32-C3 → VEML7700 (I2C) + binary LED + ST7789 (SPI). Pins match lux.yaml.

Dark background so it reads well in both the light and dark docs themes.
Regenerate from docs/assets/:
  python3 render_wiring_schematic.py
"""

INK = "#e8f1f4"
MUTED = "#93a7af"
BG = "#0f1a20"

RED = "#c0392b"      # 3V3
BLK = "#9aa5ab"      # GND (light grey so it shows on the dark background)
C_SCL_I = "#1f8a70"  # I2C SCL
C_SDA_I = "#2e86de"  # I2C SDA
C_LED = "#f39c12"    # LED GPIO
C_SCK = "#e67e22"    # SPI SCK
C_MOSI = "#8e44ad"   # SPI MOSI
C_CS = "#16a085"     # SPI CS
C_DC = "#5c6bc0"     # SPI DC (indigo — not power red)
C_RES = "#f1c40f"    # SPI RST
C_BL = "#7f8c8d"     # backlight PWM

FONT = "DejaVu Sans, sans-serif"

W, H = 1180, 900
C3_X, C3_W = 70, 250
MOD_X, MOD_W = 820, 250
ROW_H = 34
TOP = 150

c3_pins = ["3V3", "GND", "GPIO4", "GPIO5", "GPIO6",
           "GPIO0", "GPIO1", "GPIO10", "GPIO3", "GPIO7", "GPIO21"]
veml_pins = ["VIN", "GND", "SCL", "SDA"]
led_pins = ["anode", "cathode"]
# 240×240 module: VCC GND SCL/SCK SDA RST DC CS BL
tft_pins = ["VCC", "GND", "SCL", "SDA", "RST", "DC", "CS", "BL"]

nets = [
    ("3V3", "veml", "VIN", RED),
    ("GND", "veml", "GND", BLK),
    ("GPIO5", "veml", "SCL", C_SCL_I),
    ("GPIO4", "veml", "SDA", C_SDA_I),
    ("GPIO6", "led", "anode", C_LED),
    ("GND", "led", "cathode", BLK),
    ("3V3", "tft", "VCC", RED),
    ("GND", "tft", "GND", BLK),
    ("GPIO1", "tft", "SCL", C_SCK),
    ("GPIO0", "tft", "SDA", C_MOSI),
    ("GPIO7", "tft", "RST", C_RES),
    ("GPIO3", "tft", "DC", C_DC),
    ("GPIO10", "tft", "CS", C_CS),
    ("GPIO21", "tft", "BL", C_BL),
]

legend = [
    (RED, "3V3"), (BLK, "GND"),
    (C_SCL_I, "I2C SCL"), (C_SDA_I, "I2C SDA"), (C_LED, "LED"),
    (C_SCK, "SPI SCK"), (C_MOSI, "SPI MOSI"), (C_CS, "SPI CS"),
    (C_DC, "SPI DC"), (C_RES, "SPI RST"), (C_BL, "BL PWM"),
]


def block(x, y, w, pins, title, accent):
    h = ROW_H * len(pins) + 46
    out = [f'<rect x="{x+4}" y="{y+5}" width="{w}" height="{h}" rx="12" fill="#091217"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#16262e" '
           f'stroke="{accent}" stroke-width="3"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="12" fill="{accent}"/>',
           f'<rect x="{x}" y="{y+18}" width="{w}" height="16" fill="{accent}"/>',
           f'<text x="{x+w/2}" y="{y+24}" text-anchor="middle" font-family="{FONT}" '
           f'font-size="19" font-weight="700" fill="#ffffff">{title}</text>']
    pin_y = {}
    for i, p in enumerate(pins):
        py = y + 46 + i * ROW_H + ROW_H / 2
        pin_y[p] = py
    return "".join(out), pin_y, h


svg_parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
    f'height="{H}" role="img" aria-label="Schematic wiring: ESP32-C3 to VEML7700 '
    f'(I2C), LED, and ST7789 (SPI), with 3V3 and GND nets">',
    f'<rect width="{W}" height="{H}" fill="{BG}"/>',
    f'<text x="48" y="54" font-family="{FONT}" font-size="30" font-weight="700" '
    f'fill="{INK}">Wiring, pad to pad</text>',
    f'<text x="50" y="86" font-family="{FONT}" font-size="16" fill="{MUTED}">'
    f'One colour per net. Trace each wire end to end. '
    f'Do not join TFT SDA to VEML7700 SDA.</text>',
]

lx, ly = 50, 108
for col, lab in legend:
    svg_parts.append(f'<rect x="{lx}" y="{ly}" width="26" height="6" rx="3" fill="{col}"/>')
    svg_parts.append(f'<text x="{lx+32}" y="{ly+8}" font-family="{FONT}" '
                     f'font-size="14" fill="{INK}">{lab}</text>')
    lx += 32 + len(lab) * 8 + 18

c3_svg, c3y, c3h = block(C3_X, TOP, C3_W, c3_pins, "ESP32-C3", "#4a6078")
veml_svg, vemly, vemlh = block(MOD_X, TOP, MOD_W, veml_pins, "VEML7700", C_SCL_I)
led_top = TOP + vemlh + 28
led_svg, ledy, ledh = block(MOD_X, led_top, MOD_W, led_pins, "LED", C_LED)
tft_top = led_top + ledh + 28
tft_svg, tfty, tfth = block(MOD_X, tft_top, MOD_W, tft_pins, "ST7789 240×240", C_SCK)

dst_y = {"veml": vemly, "led": ledy, "tft": tfty}

for src, dst, dpin, col in nets:
    sy = c3y[src]
    dy = dst_y[dst][dpin]
    sx = C3_X + C3_W
    dx = MOD_X
    midx = (sx + dx) / 2
    svg_parts.append(
        f'<path d="M {sx} {sy} C {midx} {sy}, {midx} {dy}, {dx} {dy}" '
        f'fill="none" stroke="{col}" stroke-width="3.5" opacity="0.9"/>')
    svg_parts.append(f'<circle cx="{sx}" cy="{sy}" r="5" fill="{col}"/>')
    svg_parts.append(f'<circle cx="{dx}" cy="{dy}" r="5" fill="{col}"/>')

svg_parts += [c3_svg, veml_svg, led_svg, tft_svg]

for p, py in c3y.items():
    svg_parts.append(f'<text x="{C3_X+C3_W-14}" y="{py+5}" text-anchor="end" '
                     f'font-family="{FONT}" font-size="16" fill="{INK}">{p}</text>')
for p, py in vemly.items():
    svg_parts.append(f'<text x="{MOD_X+14}" y="{py+5}" font-family="{FONT}" '
                     f'font-size="16" fill="{INK}">{p}</text>')
for p, py in ledy.items():
    svg_parts.append(f'<text x="{MOD_X+14}" y="{py+5}" font-family="{FONT}" '
                     f'font-size="16" fill="{INK}">{p}</text>')
for p, py in tfty.items():
    svg_parts.append(f'<text x="{MOD_X+14}" y="{py+5}" font-family="{FONT}" '
                     f'font-size="16" fill="{INK}">{p}</text>')

svg_parts.append(f'<text x="50" y="{H-24}" font-family="{FONT}" font-size="15" '
                 f'fill="{MUTED}">ST7789 240\u00d7240 \u00b7 '
                 f'TFT supply VCC \u00b7 clock SCL or SCK \u00b7 '
                 f'VEML7700 power VIN / VCC / VDD \u00b7 '
                 f'LED anode via series resistor \u00b7 '
                 f'match pins by silk label.</text>')
svg_parts.append("</svg>")

with open("wiring-schematic.svg", "w") as f:
    f.write("\n".join(svg_parts))
print("ok -> wiring-schematic.svg")

"""Breadboard mid-rail gaps + bridge jumpers (SVG) for the Breadboard page.

Full-size board: power rails on both long edges. Each edge has a + and a −
column, and each column is split halfway — four bridges to make both sides
continuous end to end.

Regenerate from docs/assets/:
  python3 render_breadboard_rail_bridge.py
"""

INK = "#1c1e20"
MUTED = "#6e7376"
BG = "#f5f5f2"
RED = "#c0392b"
BLU = "#2980b9"
JUMP = "#f39c12"
BOARD = "#ffffff"
EDGE = "#c5c9cc"
HOLE = "#dfe3e6"
TRENCH = "#ecece8"

FONT = "DejaVu Sans, sans-serif"
W, H = 720, 760


def col_holes(x, y0, n=12, pitch=18):
    """One vertical column of holes."""
    return "\n".join(
        f'<circle cx="{x}" cy="{y0 + i * pitch}" r="3.2" fill="{HOLE}" '
        f'stroke="{EDGE}" stroke-width="1"/>'
        for i in range(n)
    )


def terminal_row(y, x0, n=5, pitch=16):
    return "\n".join(
        f'<circle cx="{x0 + i * pitch}" cy="{y}" r="3" fill="{HOLE}" '
        f'stroke="{EDGE}" stroke-width="1"/>'
        for i in range(n)
    )


# Layout (top-down breadboard):
#   left + | left − |  a–e  | trench |  f–j  | right − | right +
LX_P, LX_M = 100, 126
RX_M, RX_P = 594, 620
TERM_L, TERM_R = 175, 400
TOP_Y0, BOT_Y0 = 140, 440
N_HALF = 10
PITCH = 18

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
    f'height="{H}" role="img" aria-label="Breadboard with power rails on both '
    f'long edges; each plus and minus rail is split in the middle and bridged '
    f'with a short jumper">',
    f'<rect width="{W}" height="{H}" fill="{BG}"/>',
    f'<text x="36" y="40" font-family="{FONT}" font-size="26" font-weight="700" '
    f'fill="{INK}">Bridge every rail gap</text>',
    f'<text x="38" y="68" font-family="{FONT}" font-size="15" fill="{MUTED}">'
    f'Both long edges have a + and a −. Each is two halves — bridge all four.</text>',
    f'<rect x="70" y="95" width="580" height="580" rx="12" fill="{BOARD}" '
    f'stroke="{EDGE}" stroke-width="2"/>',
    f'<rect x="340" y="115" width="40" height="540" rx="4" fill="{TRENCH}"/>',
    f'<text x="360" y="105" text-anchor="middle" font-family="{FONT}" font-size="13" '
    f'fill="{MUTED}">centre trench</text>',
    # coloured rail markers (top / bottom halves)
    f'<rect x="{LX_P - 4}" y="120" width="8" height="210" rx="3" fill="{RED}"/>',
    f'<rect x="{LX_M - 4}" y="120" width="8" height="210" rx="3" fill="{BLU}"/>',
    f'<rect x="{LX_P - 4}" y="430" width="8" height="210" rx="3" fill="{RED}"/>',
    f'<rect x="{LX_M - 4}" y="430" width="8" height="210" rx="3" fill="{BLU}"/>',
    f'<rect x="{RX_M - 4}" y="120" width="8" height="210" rx="3" fill="{BLU}"/>',
    f'<rect x="{RX_P - 4}" y="120" width="8" height="210" rx="3" fill="{RED}"/>',
    f'<rect x="{RX_M - 4}" y="430" width="8" height="210" rx="3" fill="{BLU}"/>',
    f'<rect x="{RX_P - 4}" y="430" width="8" height="210" rx="3" fill="{RED}"/>',
    # gap bands
    f'<rect x="84" y="350" width="56" height="56" rx="6" fill="#fdecea"/>',
    f'<rect x="580" y="350" width="56" height="56" rx="6" fill="#fdecea"/>',
    f'<text x="112" y="383" text-anchor="middle" font-family="{FONT}" font-size="12" '
    f'font-weight="700" fill="{RED}">gap</text>',
    f'<text x="608" y="383" text-anchor="middle" font-family="{FONT}" font-size="12" '
    f'font-weight="700" fill="{RED}">gap</text>',
    # one hole column per rail half
    col_holes(LX_P, TOP_Y0, N_HALF, PITCH),
    col_holes(LX_M, TOP_Y0, N_HALF, PITCH),
    col_holes(LX_P, BOT_Y0, N_HALF, PITCH),
    col_holes(LX_M, BOT_Y0, N_HALF, PITCH),
    col_holes(RX_M, TOP_Y0, N_HALF, PITCH),
    col_holes(RX_P, TOP_Y0, N_HALF, PITCH),
    col_holes(RX_M, BOT_Y0, N_HALF, PITCH),
    col_holes(RX_P, BOT_Y0, N_HALF, PITCH),
]

# terminal strips only (a–e / f–j), no extras beside the rails
for y in range(140, 640, 28):
    parts.append(terminal_row(y, TERM_L, 5))
    parts.append(terminal_row(y, TERM_R, 5))

# last hole in top half / first in bottom half — jumper endpoints
y_top = TOP_Y0 + (N_HALF - 1) * PITCH
y_bot = BOT_Y0

parts += [
    f'<text x="{LX_P}" y="112" text-anchor="middle" font-family="{FONT}" font-size="14" '
    f'font-weight="700" fill="{RED}">+</text>',
    f'<text x="{LX_M}" y="112" text-anchor="middle" font-family="{FONT}" font-size="16" '
    f'font-weight="700" fill="{BLU}">−</text>',
    f'<text x="{RX_M}" y="112" text-anchor="middle" font-family="{FONT}" font-size="16" '
    f'font-weight="700" fill="{BLU}">−</text>',
    f'<text x="{RX_P}" y="112" text-anchor="middle" font-family="{FONT}" font-size="14" '
    f'font-weight="700" fill="{RED}">+</text>',
    # left + bridge (outside)
    f'<path d="M {LX_P} {y_top} C 40 360, 40 400, {LX_P} {y_bot}" fill="none" '
    f'stroke="{JUMP}" stroke-width="6" stroke-linecap="round"/>',
    f'<circle cx="{LX_P}" cy="{y_top}" r="6" fill="{JUMP}"/>',
    f'<circle cx="{LX_P}" cy="{y_bot}" r="6" fill="{JUMP}"/>',
    # left − bridge (toward trench)
    f'<path d="M {LX_M} {y_top} C 160 360, 160 400, {LX_M} {y_bot}" fill="none" '
    f'stroke="{JUMP}" stroke-width="6" stroke-linecap="round"/>',
    f'<circle cx="{LX_M}" cy="{y_top}" r="6" fill="{JUMP}"/>',
    f'<circle cx="{LX_M}" cy="{y_bot}" r="6" fill="{JUMP}"/>',
    # right − bridge (toward trench)
    f'<path d="M {RX_M} {y_top} C 560 360, 560 400, {RX_M} {y_bot}" fill="none" '
    f'stroke="{JUMP}" stroke-width="6" stroke-linecap="round"/>',
    f'<circle cx="{RX_M}" cy="{y_top}" r="6" fill="{JUMP}"/>',
    f'<circle cx="{RX_M}" cy="{y_bot}" r="6" fill="{JUMP}"/>',
    # right + bridge (outside)
    f'<path d="M {RX_P} {y_top} C 680 360, 680 400, {RX_P} {y_bot}" fill="none" '
    f'stroke="{JUMP}" stroke-width="6" stroke-linecap="round"/>',
    f'<circle cx="{RX_P}" cy="{y_top}" r="6" fill="{JUMP}"/>',
    f'<circle cx="{RX_P}" cy="{y_bot}" r="6" fill="{JUMP}"/>',
    f'<text x="36" y="385" font-family="{FONT}" font-size="13" font-weight="700" '
    f'fill="{JUMP}">bridge</text>',
    f'<text x="668" y="385" font-family="{FONT}" font-size="13" font-weight="700" '
    f'fill="{JUMP}">bridge</text>',
    f'<text x="38" y="708" font-family="{FONT}" font-size="14" fill="{MUTED}">'
    f'Four short jumpers: left +, left −, right +, right −.</text>',
    f'<text x="38" y="730" font-family="{FONT}" font-size="14" fill="{MUTED}">'
    f'Only need one edge for 3V3/GND? Still bridge both + and − on that edge.</text>',
    "</svg>",
]

with open("breadboard-rail-bridge.svg", "w") as f:
    f.write("\n".join(parts))
print("ok -> breadboard-rail-bridge.svg")

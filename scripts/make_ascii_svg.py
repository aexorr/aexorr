from pathlib import Path
import base64

from PIL import Image, ImageEnhance

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

SOURCE = ROOT / "source-photo.png"
OUTPUT = ROOT / "avi-ascii.svg"

# Compact premium layout
WIDTH = 900
HEIGHT = 560

# -------------------------
# Prepare photo
# -------------------------

img = Image.open(SOURCE).convert("RGB")

# Smaller portrait area
img.thumbnail((540, 390), Image.Resampling.LANCZOS)

# Slight cinematic treatment
img = ImageEnhance.Contrast(img).enhance(1.10)
img = ImageEnhance.Brightness(img).enhance(0.90)
img = ImageEnhance.Sharpness(img).enhance(1.08)

PHOTO_W = 540
PHOTO_H = 390

canvas = Image.new(
    "RGB",
    (PHOTO_W, PHOTO_H),
    (5, 8, 13)
)

x = (PHOTO_W - img.width) // 2
y = (PHOTO_H - img.height) // 2

canvas.paste(img, (x, y))

# Encode image
temp = ROOT / "_profile_temp.png"
canvas.save(temp, "PNG")

data = base64.b64encode(
    temp.read_bytes()
).decode("ascii")

temp.unlink(missing_ok=True)

# -------------------------
# SVG
# -------------------------

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

  <clipPath id="photoClip">
    <rect
      x="180"
      y="92"
      width="{PHOTO_W}"
      height="{PHOTO_H}"
      rx="10"/>
  </clipPath>

  <filter id="redGlitch">
    <feColorMatrix type="matrix"
      values="
      1 0 0 0 0.45
      0 0 0 0 0
      0 0 0 0 0
      0 0 0 1 0"/>
  </filter>

  <filter id="cyanGlitch">
    <feColorMatrix type="matrix"
      values="
      0 0 0 0 0
      0 1 0 0 0.55
      0 0 1 0 0.65
      0 0 0 1 0"/>
  </filter>

  <filter id="glow">
    <feGaussianBlur stdDeviation="3"/>
  </filter>

  <linearGradient id="scanGradient"
    x1="0" y1="0"
    x2="0" y2="1">

    <stop offset="0"
      stop-color="#66ffe0"
      stop-opacity="0"/>

    <stop offset="0.5"
      stop-color="#66ffe0"
      stop-opacity="0.16"/>

    <stop offset="1"
      stop-color="#66ffe0"
      stop-opacity="0"/>

  </linearGradient>

  <style>

    .red {{
      animation: redGlitch 5.5s infinite steps(1);
    }}

    .cyan {{
      animation: cyanGlitch 6.2s infinite steps(1);
    }}

    .scan {{
      animation: scan 4.5s linear infinite;
    }}

    .flicker {{
      animation: flicker 6s infinite;
    }}

    @keyframes redGlitch {{

      0%, 88%, 100% {{
        opacity: 0;
        transform: translate(0,0);
      }}

      89% {{
        opacity: .30;
        transform: translate(6px,0);
      }}

      90% {{
        opacity: .16;
        transform: translate(-4px,1px);
      }}

      91% {{
        opacity: 0;
        transform: translate(0,0);
      }}

    }}

    @keyframes cyanGlitch {{

      0%, 72%, 100% {{
        opacity: 0;
        transform: translate(0,0);
      }}

      73% {{
        opacity: .25;
        transform: translate(-5px,0);
      }}

      74% {{
        opacity: .12;
        transform: translate(3px,-1px);
      }}

      75% {{
        opacity: 0;
        transform: translate(0,0);
      }}

    }}

    @keyframes scan {{

      0% {{
        transform: translateY(-400px);
        opacity: 0;
      }}

      12% {{
        opacity: .65;
      }}

      50% {{
        opacity: .35;
      }}

      100% {{
        transform: translateY(400px);
        opacity: 0;
      }}

    }}

    @keyframes flicker {{

      0%, 96%, 100% {{
        opacity: 1;
      }}

      97% {{
        opacity: .90;
      }}

      98% {{
        opacity: 1;
      }}

    }}

  </style>

</defs>

<!-- BACKGROUND -->

<rect
  width="900"
  height="560"
  fill="#04070b"/>

<!-- VERY SUBTLE GRID -->

<g
  stroke="#17212c"
  stroke-width="1"
  opacity=".22">

  <line x1="45" y1="70" x2="855" y2="70"/>
  <line x1="45" y1="500" x2="855" y2="500"/>

</g>

<!-- TERMINAL HEADER -->

<rect
  x="40"
  y="24"
  width="820"
  height="40"
  rx="8"
  fill="#0a1017"
  stroke="#263441"/>

<circle cx="61" cy="44" r="5" fill="#ff4d4d"/>
<circle cx="80" cy="44" r="5" fill="#ffbd2e"/>
<circle cx="99" cy="44" r="5" fill="#28c840"/>

<text
  x="122"
  y="49"
  fill="#7d8b99"
  font-size="13"
  font-family="monospace">

  aexorr@github:~$ ./profile.sh

</text>

<!-- OUTER PHOTO FRAME -->

<rect
  x="150"
  y="76"
  width="600"
  height="422"
  rx="16"
  fill="#02050a"
  stroke="#263542"
  stroke-width="2"/>

<!-- GLOW BORDER -->

<rect
  x="153"
  y="79"
  width="594"
  height="416"
  rx="14"
  fill="none"
  stroke="#53e6c5"
  stroke-width="1"
  opacity=".16"
  filter="url(#glow)"/>

<!-- RED GLITCH -->

<g
  clip-path="url(#photoClip)"
  class="red">

  <image
    x="180"
    y="92"
    width="{PHOTO_W}"
    height="{PHOTO_H}"
    preserveAspectRatio="xMidYMid meet"
    href="data:image/png;base64,{data}"
    filter="url(#redGlitch)"/>

</g>

<!-- CYAN GLITCH -->

<g
  clip-path="url(#photoClip)"
  class="cyan">

  <image
    x="180"
    y="92"
    width="{PHOTO_W}"
    height="{PHOTO_H}"
    preserveAspectRatio="xMidYMid meet"
    href="data:image/png;base64,{data}"
    filter="url(#cyanGlitch)"/>

</g>

<!-- MAIN PHOTO -->

<g class="flicker">

  <image
    x="180"
    y="92"
    width="{PHOTO_W}"
    height="{PHOTO_H}"
    preserveAspectRatio="xMidYMid meet"
    href="data:image/png;base64,{data}"/>

</g>

<!-- PHOTO INNER BORDER -->

<rect
  x="180"
  y="92"
  width="{PHOTO_W}"
  height="{PHOTO_H}"
  rx="10"
  fill="none"
  stroke="#52616f"
  stroke-width="1"
  opacity=".35"/>

<!-- SCANLINES -->

<g
  clip-path="url(#photoClip)"
  opacity=".22">

  <rect
    x="180"
    y="92"
    width="{PHOTO_W}"
    height="{PHOTO_H}"
    fill="url(#scanGradient)"
    class="scan"/>

  <g
    stroke="#ffffff"
    stroke-opacity=".045">

'''

# Fine scanlines
for y in range(98, 478, 7):
    svg += f'''
    <line
      x1="180"
      y1="{y}"
      x2="720"
      y2="{y}"/>
'''

svg += f'''

  </g>

</g>

<!-- MOVING SCAN BAR -->

<rect
  x="180"
  y="92"
  width="{PHOTO_W}"
  height="2"
  fill="#64ffe0"
  opacity=".32"
  class="scan"
  clip-path="url(#photoClip)"/>

<!-- CORNER MARKERS -->

<g
  stroke="#61e6c5"
  stroke-width="2"
  opacity=".65">

  <line x1="164" y1="108" x2="164" y2="126"/>
  <line x1="164" y1="108" x2="182" y2="108"/>

  <line x1="736" y1="108" x2="736" y2="126"/>
  <line x1="718" y1="108" x2="736" y2="108"/>

  <line x1="164" y1="466" x2="164" y2="484"/>
  <line x1="164" y1="484" x2="182" y2="484"/>

  <line x1="736" y1="466" x2="736" y2="484"/>
  <line x1="718" y1="484" x2="736" y2="484"/>

</g>

<!-- STATUS BAR -->

<text
  x="160"
  y="525"
  fill="#647586"
  font-size="12"
  font-family="monospace">

  IDENTITY: AEXORR

</text>

<text
  x="405"
  y="525"
  fill="#647586"
  font-size="12"
  font-family="monospace">

  STATUS: ONLINE

</text>

<text
  x="650"
  y="525"
  fill="#39ff88"
  font-size="12"
  font-family="monospace">

  [ ACCESS GRANTED ]

</text>

<!-- BOTTOM ACCENT -->

<line
  x1="160"
  y1="540"
  x2="740"
  y2="540"
  stroke="#182630"
  stroke-width="1"/>

<circle
  cx="160"
  cy="540"
  r="2"
  fill="#39ff88"/>

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"wrote {OUTPUT}")

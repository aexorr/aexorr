from pathlib import Path
import base64

from PIL import Image, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

SOURCE = ROOT / "source-photo.png"
OUTPUT = ROOT / "avi-ascii.svg"

WIDTH = 1000
HEIGHT = 620

# --------------------------------------------------
# PHOTO
# --------------------------------------------------

img = Image.open(SOURCE).convert("RGB")

img.thumbnail((430, 430), Image.Resampling.LANCZOS)

img = ImageEnhance.Contrast(img).enhance(1.12)
img = ImageEnhance.Brightness(img).enhance(0.88)
img = ImageEnhance.Sharpness(img).enhance(1.12)

PHOTO_W = 430
PHOTO_H = 430

canvas = Image.new("RGB", (PHOTO_W, PHOTO_H), (4, 7, 11))

x = (PHOTO_W - img.width) // 2
y = (PHOTO_H - img.height) // 2

canvas.paste(img, (x, y))

temp = ROOT / "_aexorr_profile.png"
canvas.save(temp, "PNG")

photo_data = base64.b64encode(
    temp.read_bytes()
).decode("ascii")

temp.unlink(missing_ok=True)

# --------------------------------------------------
# SVG
# --------------------------------------------------

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

  <clipPath id="photoClip">
    <rect x="74" y="122"
          width="430"
          height="430"
          rx="8"/>
  </clipPath>

  <filter id="cyanGlow">
    <feGaussianBlur stdDeviation="3"/>
  </filter>

  <filter id="softGlow">
    <feGaussianBlur stdDeviation="6"/>
  </filter>

  <style>

    text {{
      font-family: "Courier New", monospace;
    }}

    .cyan {{
      fill: #55ffe1;
    }}

    .green {{
      fill: #39ff88;
    }}

    .red {{
      fill: #ff4d67;
    }}

    .dim {{
      fill: #506473;
    }}

    .muted {{
      fill: #78909c;
    }}

    .value {{
      fill: #a6fff0;
    }}

    .small {{
      font-size: 11px;
      letter-spacing: 2px;
    }}

    .tiny {{
      font-size: 9px;
      letter-spacing: 1.5px;
    }}

    .label {{
      font-size: 12px;
      letter-spacing: 2px;
    }}

    .main {{
      font-size: 18px;
      font-weight: bold;
      letter-spacing: 4px;
    }}

    .glitch-red {{
      animation: glitchRed 5s infinite steps(1);
    }}

    .glitch-cyan {{
      animation: glitchCyan 6s infinite steps(1);
    }}

    .scan {{
      animation: scan 4s linear infinite;
    }}

    .flicker {{
      animation: flicker 7s infinite;
    }}

    @keyframes glitchRed {{
      0%, 90%, 100% {{
        opacity: 0;
        transform: translate(0,0);
      }}

      91% {{
        opacity: .45;
        transform: translate(5px,0);
      }}

      92% {{
        opacity: .15;
        transform: translate(-3px,1px);
      }}

      93% {{
        opacity: 0;
      }}
    }}

    @keyframes glitchCyan {{
      0%, 76%, 100% {{
        opacity: 0;
        transform: translate(0,0);
      }}

      77% {{
        opacity: .35;
        transform: translate(-5px,0);
      }}

      78% {{
        opacity: .12;
        transform: translate(3px,-1px);
      }}

      79% {{
        opacity: 0;
      }}
    }}

    @keyframes scan {{
      0% {{
        transform: translateY(-450px);
        opacity: 0;
      }}

      15% {{
        opacity: .55;
      }}

      50% {{
        opacity: .18;
      }}

      100% {{
        transform: translateY(450px);
        opacity: 0;
      }}
    }}

    @keyframes flicker {{
      0%, 96%, 100% {{
        opacity: 1;
      }}

      97% {{
        opacity: .86;
      }}

      98% {{
        opacity: 1;
      }}
    }}

  </style>

</defs>

<!-- ================================================= -->
<!-- BACKGROUND -->
<!-- ================================================= -->

<rect
  width="1000"
  height="620"
  fill="#03070b"/>

<!-- subtle cyber grid -->

<g
  stroke="#10202a"
  stroke-width="1"
  opacity=".38">

  <line x1="40" y1="90" x2="960" y2="90"/>
  <line x1="40" y1="580" x2="960" y2="580"/>

  <line x1="40" y1="90" x2="40" y2="580"/>
  <line x1="960" y1="90" x2="960" y2="580"/>

</g>

<!-- ================================================= -->
<!-- TERMINAL HEADER -->
<!-- ================================================= -->

<rect
  x="40"
  y="28"
  width="920"
  height="42"
  rx="7"
  fill="#071017"
  stroke="#20333e"/>

<circle cx="62" cy="49" r="5" fill="#ff4d5c"/>
<circle cx="80" cy="49" r="5" fill="#ffbd2e"/>
<circle cx="98" cy="49" r="5" fill="#32d74b"/>

<text
  x="122"
  y="54"
  class="small cyan">

  AEXORR@GITHUB:~$ ./PROFILE.SH

</text>

<text
  x="790"
  y="54"
  class="tiny dim">

  SESSION_07

</text>

<!-- ================================================= -->
<!-- LEFT PHOTO PANEL -->
<!-- ================================================= -->

<rect
  x="50"
  y="100"
  width="500"
  height="470"
  rx="13"
  fill="#050a0f"
  stroke="#213640"
  stroke-width="2"/>

<!-- cyan glow -->

<rect
  x="53"
  y="103"
  width="494"
  height="464"
  rx="11"
  fill="none"
  stroke="#3fffd0"
  stroke-width="2"
  opacity=".10"
  filter="url(#softGlow)"/>

<!-- photo -->

<g class="flicker">

  <image
    x="74"
    y="122"
    width="430"
    height="430"
    preserveAspectRatio="xMidYMid meet"
    href="data:image/png;base64,{photo_data}"/>

</g>

<!-- RGB glitch layers -->

<g
  clip-path="url(#photoClip)"
  class="glitch-red">

  <image
    x="74"
    y="122"
    width="430"
    height="430"
    preserveAspectRatio="xMidYMid meet"
    href="data:image/png;base64,{photo_data}"
    opacity=".5"/>

</g>

<g
  clip-path="url(#photoClip)"
  class="glitch-cyan">

  <image
    x="74"
    y="122"
    width="430"
    height="430"
    preserveAspectRatio="xMidYMid meet"
    href="data:image/png;base64,{photo_data}"
    opacity=".5"/>

</g>

<!-- scanlines -->

<g
  clip-path="url(#photoClip)"
  opacity=".16"
  stroke="#6affea">

'''

for y in range(126, 550, 8):
    svg += f'''
  <line x1="74" y1="{y}" x2="504" y2="{y}"/>
'''

svg += f'''

</g>

<!-- moving scan bar -->

<rect
  x="74"
  y="122"
  width="430"
  height="2"
  fill="#56ffe0"
  opacity=".45"
  class="scan"
  clip-path="url(#photoClip)"/>

<!-- photo border -->

<rect
  x="74"
  y="122"
  width="430"
  height="430"
  rx="8"
  fill="none"
  stroke="#304854"
  stroke-width="1"/>

<!-- corner HUD -->

<g
  stroke="#4fffe0"
  stroke-width="2"
  fill="none"
  opacity=".85">

  <path d="M60 140 V120 H80"/>
  <path d="M520 120 H540 V140"/>

  <path d="M60 530 V550 H80"/>
  <path d="M520 550 H540 V530"/>

</g>

<!-- photo panel status -->

<text x="70" y="108" class="tiny dim">
  CAMERA_FEED // 001
</text>

<text x="405" y="108" class="tiny green">
  LIVE
</text>

<!-- ================================================= -->
<!-- RIGHT SYSTEM PANEL -->
<!-- ================================================= -->

<text
  x="590"
  y="118"
  class="tiny dim">

  // SYSTEM_IDENTITY

</text>

<text
  x="590"
  y="153"
  class="main cyan">

  AEXORR

</text>

<text
  x="592"
  y="178"
  class="tiny muted">

  DIGITAL ENTITY / DEVELOPER NODE

</text>

<line
  x1="590"
  y1="194"
  x2="930"
  y2="194"
  stroke="#19323b"/>

<!-- system -->

<text x="590" y="225" class="tiny dim">
  SYSTEM
</text>

<text x="590" y="248" class="label value">
  ONLINE // STABLE
</text>

<!-- user -->

<text x="590" y="282" class="tiny dim">
  USER
</text>

<text x="590" y="305" class="label cyan">
  AEXORR
</text>

<!-- role -->

<text x="590" y="339" class="tiny dim">
  ROLE
</text>

<text x="590" y="362" class="label value">
  DEVELOPER
</text>

<!-- stack -->

<text x="590" y="396" class="tiny dim">
  STACK
</text>

<text x="590" y="419" class="label value">
  PYTHON // JS // WEB
</text>

<!-- status -->

<text x="590" y="453" class="tiny dim">
  CURRENT_STATUS
</text>

<text x="590" y="476" class="label green">
  BUILDING...
</text>

<!-- access -->

<rect
  x="590"
  y="502"
  width="340"
  height="42"
  rx="5"
  fill="#06130d"
  stroke="#1d633d"/>

<text
  x="610"
  y="528"
  class="label green">

  [ ACCESS_GRANTED ]

</text>

<!-- ================================================= -->
<!-- CYBER DETAILS -->
<!-- ================================================= -->

<text
  x="590"
  y="562"
  class="tiny dim">

  NODE_07 // AUTH_0xA3 // SECURE_CHANNEL

</text>

<!-- bottom system bar -->

<line
  x1="50"
  y1="590"
  x2="950"
  y2="590"
  stroke="#17303a"/>

<circle
  cx="65"
  cy="590"
  r="3"
  fill="#39ff88"/>

<text
  x="80"
  y="595"
  class="tiny green">

  CONNECTION_SECURE

</text>

<text
  x="350"
  y="595"
  class="tiny dim">

  // ENCRYPTED // NO_TRACE //

</text>

<text
  x="790"
  y="595"
  class="tiny cyan">

  0xAEXORR

</text>

<!-- tiny cyber marks -->

<g
  class="tiny"
  opacity=".45">

  <text x="900" y="105" class="red">01</text>
  <text x="918" y="120" class="cyan">10</text>
  <text x="900" y="135" class="dim">01</text>
  <text x="918" y="150" class="green">11</text>

</g>

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"wrote {OUTPUT}")

from pathlib import Path
import base64
import html

from PIL import Image, ImageEnhance, ImageOps


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

SOURCE = ROOT / "source-photo.png"
OUTPUT = ROOT / "avi-ascii.svg"

WIDTH = 1000
HEIGHT = 620


# -------------------------
# Prepare normal photo
# -------------------------

img = Image.open(SOURCE).convert("RGB")

# Keep the real photo — no ASCII conversion.
img.thumbnail((760, 470), Image.Resampling.LANCZOS)

# Slight contrast boost
img = ImageEnhance.Contrast(img).enhance(1.08)

# Darken slightly for cyber-terminal look
img = ImageEnhance.Brightness(img).enhance(0.88)

# Put photo inside a fixed canvas
canvas = Image.new("RGB", (760, 470), (8, 12, 18))

x = (760 - img.width) // 2
y = (470 - img.height) // 2

canvas.paste(img, (x, y))

# Encode image inside SVG
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
        <rect x="120" y="75"
              width="760"
              height="470"
              rx="10"/>
    </clipPath>

    <filter id="redChannel">
        <feColorMatrix type="matrix"
        values="
        1 0 0 0 0.55
        0 0 0 0 0
        0 0 0 0 0
        0 0 0 1 0"/>
    </filter>

    <filter id="cyanChannel">
        <feColorMatrix type="matrix"
        values="
        0 0 0 0 0
        0 1 0 0 0.65
        0 0 1 0 0.65
        0 0 0 1 0"/>
    </filter>

    <filter id="softGlow">
        <feGaussianBlur stdDeviation="2"/>
    </filter>

    <linearGradient id="scanGradient"
                    x1="0" y1="0"
                    x2="0" y2="1">
        <stop offset="0" stop-color="#ffffff" stop-opacity="0"/>
        <stop offset="0.5" stop-color="#55ffcc" stop-opacity="0.10"/>
        <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <style>

        .glitchRed {{
            animation: glitchRed 4.5s infinite steps(1);
        }}

        .glitchCyan {{
            animation: glitchCyan 5.2s infinite steps(1);
        }}

        .scan {{
            animation: scan 3.8s linear infinite;
        }}

        .flicker {{
            animation: flicker 4s infinite;
        }}

        .noise {{
            animation: noise 1.8s infinite steps(2);
        }}

        @keyframes glitchRed {{

            0%, 82%, 100% {{
                transform: translate(0,0);
                opacity: 0;
            }}

            83% {{
                transform: translate(8px,-2px);
                opacity: .42;
            }}

            84% {{
                transform: translate(-5px,2px);
                opacity: .25;
            }}

            85% {{
                transform: translate(3px,0);
                opacity: .38;
            }}

            86% {{
                transform: translate(0,0);
                opacity: 0;
            }}
        }}

        @keyframes glitchCyan {{

            0%, 67%, 100% {{
                transform: translate(0,0);
                opacity: 0;
            }}

            68% {{
                transform: translate(-7px,1px);
                opacity: .38;
            }}

            69% {{
                transform: translate(4px,-2px);
                opacity: .25;
            }}

            70% {{
                transform: translate(0,0);
                opacity: 0;
            }}
        }}

        @keyframes scan {{

            0% {{
                transform: translateY(-490px);
                opacity: 0;
            }}

            12% {{
                opacity: .7;
            }}

            55% {{
                opacity: .45;
            }}

            100% {{
                transform: translateY(490px);
                opacity: 0;
            }}
        }}

        @keyframes flicker {{

            0%, 94%, 100% {{
                opacity: 1;
            }}

            95% {{
                opacity: .82;
            }}

            96% {{
                opacity: 1;
            }}
        }}

        @keyframes noise {{

            0%, 100% {{
                opacity: .08;
            }}

            50% {{
                opacity: .18;
            }}
        }}

    </style>

</defs>


<!-- BACKGROUND -->

<rect width="1000"
      height="620"
      fill="#05080d"/>


<!-- TERMINAL HEADER -->

<rect x="35"
      y="25"
      width="930"
      height="42"
      rx="8"
      fill="#0b1119"
      stroke="#273342"/>

<circle cx="58" cy="46" r="6" fill="#ff4d4d"/>
<circle cx="80" cy="46" r="6" fill="#ffbd2e"/>
<circle cx="102" cy="46" r="6" fill="#28c840"/>

<text x="125"
      y="51"
      fill="#718096"
      font-size="14"
      font-family="monospace">
    aexorr@github:~$ ./profile.sh
</text>


<!-- PHOTO FRAME -->

<rect x="105"
      y="70"
      width="790"
      height="500"
      rx="14"
      fill="#020408"
      stroke="#263241"
      stroke-width="2"/>


<!-- RED GLITCH COPY -->

<g clip-path="url(#photoClip)"
   class="glitchRed">

    <image
        x="120"
        y="75"
        width="760"
        height="470"
        preserveAspectRatio="xMidYMid meet"
        href="data:image/png;base64,{data}"
        filter="url(#redChannel)"/>

</g>


<!-- CYAN GLITCH COPY -->

<g clip-path="url(#photoClip)"
   class="glitchCyan">

    <image
        x="120"
        y="75"
        width="760"
        height="470"
        preserveAspectRatio="xMidYMid meet"
        href="data:image/png;base64,{data}"
        filter="url(#cyanChannel)"/>

</g>


<!-- MAIN REAL PHOTO -->

<g class="flicker">

    <image
        x="120"
        y="75"
        width="760"
        height="470"
        preserveAspectRatio="xMidYMid meet"
        href="data:image/png;base64,{data}"/>

</g>


<!-- SCANLINES -->

<g clip-path="url(#photoClip)"
   class="noise">

    <rect x="120"
          y="75"
          width="760"
          height="470"
          fill="url(#scanGradient)"
          opacity=".25"/>

    <g stroke="#ffffff"
       stroke-opacity=".055">

'''

# Horizontal scanlines
for y in range(82, 545, 6):
    svg += f'''
        <line x1="120"
              y1="{y}"
              x2="880"
              y2="{y}"/>
'''

svg += f'''
    </g>

</g>


<!-- MOVING SCAN BAR -->

<rect x="120"
      y="75"
      width="760"
      height="3"
      fill="#7fffd4"
      opacity=".28"
      class="scan"
      clip-path="url(#photoClip)"/>


<!-- TERMINAL STATUS -->

<text x="125"
      y="592"
      fill="#4f6275"
      font-size="13"
      font-family="monospace">
    IDENTITY: AEXORR
</text>

<text x="430"
      y="592"
      fill="#4f6275"
      font-size="13"
      font-family="monospace">
    STATUS: ONLINE
</text>

<text x="720"
      y="592"
      fill="#39ff88"
      font-size="13"
      font-family="monospace">
    [ ACCESS GRANTED ]
</text>

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")
print(f"wrote {{OUTPUT}}")


print(f"wrote {{OUTPUT}}")

from pathlib import Path
import html

from PIL import Image, ImageOps


# ============================================================
# AEXORR // CYBER TERMINAL PORTRAIT
# ============================================================

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

INPUT = ROOT / "source-prepped.png"
OUTPUT = ROOT / "avi-ascii.svg"


# Compact size — page ko huge nahi banayega
COLS = 78
ROWS = 42

# ASCII ramp
RAMP = " .:-=+*#%@"

# Terminal dimensions
CELL_W = 9
CELL_H = 13

WIDTH = 760
HEIGHT = 650


def brightness_to_char(value):
    index = int(
        (value / 255)
        * (len(RAMP) - 1)
    )

    return RAMP[index]


def load_image():

    image = Image.open(INPUT).convert("L")

    # Improve contrast
    image = ImageOps.autocontrast(image)

    # Preserve portrait proportions
    image.thumbnail(
        (COLS, ROWS),
        Image.Resampling.LANCZOS
    )

    canvas = Image.new(
        "L",
        (COLS, ROWS),
        255
    )

    x = (COLS - image.width) // 2
    y = (ROWS - image.height) // 2

    canvas.paste(
        image,
        (x, y)
    )

    return canvas


def build_ascii(image):

    lines = []

    for y in range(ROWS):

        line = []

        for x in range(COLS):

            pixel = image.getpixel(
                (x, y)
            )

            # Invert because dark pixels
            # should become strong ASCII
            pixel = 255 - pixel

            char = brightness_to_char(
                pixel
            )

            line.append(char)

        lines.append(
            "".join(line)
        )

    return lines


def esc(text):
    return html.escape(text)


def main():

    image = load_image()

    ascii_lines = build_ascii(image)

    svg = []

    # ========================================================
    # SVG HEADER
    # ========================================================

    svg.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{WIDTH}"
        height="{HEIGHT}"
        viewBox="0 0 {WIDTH} {HEIGHT}">'''
    )

    # Background
    svg.append(
        '''
        <rect
            width="100%"
            height="100%"
            rx="18"
            fill="#05080d"
        />
        '''
    )

    # Outer border
    svg.append(
        '''
        <rect
            x="1"
            y="1"
            width="758"
            height="648"
            rx="18"
            fill="none"
            stroke="#30363d"
        />
        '''
    )

    # ========================================================
    # TERMINAL TOP BAR
    # ========================================================

    svg.append(
        '''
        <rect
            x="1"
            y="1"
            width="758"
            height="48"
            rx="18"
            fill="#0d1117"
        />
        '''
    )

    # Hide lower rounded corners of top bar
    svg.append(
        '''
        <rect
            x="1"
            y="25"
            width="758"
            height="25"
            fill="#0d1117"
        />
        '''
    )

    # Terminal buttons
    svg.append(
        '<circle cx="25" cy="25" r="6" fill="#ff5f56"/>'
    )

    svg.append(
        '<circle cx="47" cy="25" r="6" fill="#ffbd2e"/>'
    )

    svg.append(
        '<circle cx="69" cy="25" r="6" fill="#27c93f"/>'
    )

    # Terminal title
    svg.append(
        '''
        <text
            x="380"
            y="30"
            text-anchor="middle"
            fill="#8b949e"
            font-family="monospace"
            font-size="13">
            aexorr@github:~$ ./portrait.sh
        </text>
        '''
    )

    # Separator
    svg.append(
        '''
        <line
            x1="1"
            y1="49"
            x2="759"
            y2="49"
            stroke="#30363d"
        />
        '''
    )

    # ========================================================
    # STATUS HEADER
    # ========================================================

    svg.append(
        '''
        <text
            x="30"
            y="80"
            fill="#58a6ff"
            font-family="monospace"
            font-size="13">
            [ PROFILE // IDENTITY MATRIX ]
        </text>
        '''
    )

    svg.append(
        '''
        <text
            x="730"
            y="80"
            text-anchor="end"
            fill="#3fb950"
            font-family="monospace"
            font-size="12">
            ONLINE
        </text>
        '''
    )

    # ========================================================
    # ASCII PORTRAIT PANEL
    # ========================================================

    PANEL_X = 28
    PANEL_Y = 100
    PANEL_W = 704
    PANEL_H = 430

    svg.append(
        f'''
        <rect
            x="{PANEL_X}"
            y="{PANEL_Y}"
            width="{PANEL_W}"
            height="{PANEL_H}"
            rx="10"
            fill="#020409"
            stroke="#21262d"
        />
        '''
    )

    # Subtle red scan line
    svg.append(
        '''
        <rect
            x="29"
            y="105"
            width="702"
            height="2"
            fill="#ff3030"
            opacity="0.18">
            <animate
                attributeName="y"
                values="105;525;105"
                dur="4s"
                repeatCount="indefinite"/>
        </rect>
        '''
    )

    # ASCII text
    start_x = 70
    start_y = 135

    for row, line in enumerate(ascii_lines):

        y = start_y + row * CELL_H

        # Different subtle tones based on row
        if row % 7 == 0:
            fill = "#c9d1d9"
        else:
            fill = "#8b949e"

        svg.append(
            f'''
            <text
                x="{start_x}"
                y="{y}"
                fill="{fill}"
                font-family="monospace"
                font-size="11"
                xml:space="preserve">
                {esc(line)}
            </text>
            '''
        )

    # ========================================================
    # SYSTEM LABELS
    # ========================================================

    svg.append(
        '''
        <text
            x="45"
            y="555"
            fill="#58a6ff"
            font-family="monospace"
            font-size="12">
            aexorr@github:~$
        </text>
        '''
    )

    svg.append(
        '''
        <text
            x="190"
            y="555"
            fill="#c9d1d9"
            font-family="monospace"
            font-size="12">
            whoami
        </text>
        '''
    )

    svg.append(
        '''
        <text
            x="45"
            y="580"
            fill="#3fb950"
            font-family="monospace"
            font-size="12">
            &gt; AEXORR // DEVELOPER // BUILDER
        </text>
        '''
    )

    svg.append(
        '''
        <text
            x="45"
            y="605"
            fill="#8b949e"
            font-family="monospace"
            font-size="11">
            [ SYSTEM ONLINE ]  [ ACCESS GRANTED ]  [ TRACE ACTIVE ]
        </text>
        '''
    )

    # Cursor
    svg.append(
        '''
        <rect
            x="45"
            y="620"
            width="7"
            height="13"
            fill="#58a6ff">
            <animate
                attributeName="opacity"
                values="1;0;1"
                dur="0.9s"
                repeatCount="indefinite"/>
        </rect>
        '''
    )

    svg.append("</svg>")

    OUTPUT.write_text(
        "".join(svg),
        encoding="utf-8"
    )

    print(
        f"wrote {OUTPUT}"
    )


if __name__ == "__main__":
    main()

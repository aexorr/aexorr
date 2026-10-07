from pathlib import Path
import html

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "info-card.svg"

# =========================
# CUSTOMIZE YOUR PROFILE
# =========================

HOST = "aexorr@github"

ROWS = [
    ("host",),

    ("kv", "User", "aexorr"),
    ("kv", "Role", "Developer"),
    ("kv", "Focus", "Web • AI • Projects"),

    ("gap",),

    ("sec", "Stack"),

    ("kv", "Languages", "Python • JavaScript • C++"),
    ("kv", "Frontend", "HTML • CSS • React"),
    ("kv", "Backend", "Node.js • APIs"),
    ("kv", "Tools", "Git • GitHub • VS Code"),

    ("gap",),

    ("sec", "Currently"),

    ("kv", "Building", "Projects & Experiments"),
    ("kv", "Learning", "AI • Web Development"),
    ("kv", "Status", "Building • Learning • Shipping"),
]

# =========================
# DESIGN
# =========================

WIDTH = 520

ROW_HEIGHT = 27
TOP_PADDING = 65
BOTTOM_PADDING = 32

HEIGHT = (
    TOP_PADDING
    + len(ROWS) * ROW_HEIGHT
    + BOTTOM_PADDING
)

BG = "#0d1117"
BORDER = "#30363d"

TEXT = "#c9d1d9"
MUTED = "#8b949e"
ACCENT = "#58a6ff"

FONT = (
    "ui-monospace, "
    "SFMono-Regular, "
    "Menlo, "
    "Monaco, "
    "Consolas, "
    "monospace"
)


def esc(value):
    return html.escape(str(value))


# =========================
# SVG
# =========================

svg = []

svg.append(
    f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
    font-family="{FONT}">'''
)

# Background

svg.append(
    f'''
    <rect
        x="0"
        y="0"
        width="{WIDTH}"
        height="{HEIGHT}"
        rx="12"
        fill="{BG}"
    />
    '''
)

# Border

svg.append(
    f'''
    <rect
        x="0.5"
        y="0.5"
        width="{WIDTH - 1}"
        height="{HEIGHT - 1}"
        rx="12"
        fill="none"
        stroke="{BORDER}"
    />
    '''
)

# =========================
# TERMINAL HEADER
# =========================

# Red / yellow / green dots

svg.append(
    '<circle cx="20" cy="22" r="5" fill="#ff5f56"/>'
)

svg.append(
    '<circle cx="38" cy="22" r="5" fill="#ffbd2e"/>'
)

svg.append(
    '<circle cx="56" cy="22" r="5" fill="#27c93f"/>'
)

# Header text

svg.append(
    f'''
    <text
        x="75"
        y="27"
        fill="{MUTED}"
        font-size="12"
    >
        {esc(HOST)}:~$ neofetch
    </text>
    '''
)

# Separator

svg.append(
    f'''
    <line
        x1="0"
        y1="43"
        x2="{WIDTH}"
        y2="43"
        stroke="{BORDER}"
    />
    '''
)


# =========================
# CONTENT
# =========================

y = TOP_PADDING

for index, row in enumerate(ROWS):

    kind = row[0]

    # ---------------------
    # HOST
    # ---------------------

    if kind == "host":

        svg.append(
            f'''
            <text
                x="24"
                y="{y}"
                fill="{ACCENT}"
                font-size="14"
                font-weight="bold"
            >
                {esc(HOST)}
            </text>
            '''
        )

        y += ROW_HEIGHT
        continue

    # ---------------------
    # GAP
    # ---------------------

    if kind == "gap":

        y += ROW_HEIGHT
        continue

    # ---------------------
    # SECTION
    # ---------------------

    if kind == "sec":

        title = row[1]

        svg.append(
            f'''
            <text
                x="24"
                y="{y}"
                fill="{ACCENT}"
                font-size="14"
                font-weight="bold"
            >
                [{esc(title)}]
            </text>
            '''
        )

        y += ROW_HEIGHT
        continue

    # ---------------------
    # KEY / VALUE
    # ---------------------

    if kind == "kv":

        key = row[1]
        value = row[2]

        svg.append(
            f'''
            <text
                x="24"
                y="{y}"
                fill="{MUTED}"
                font-size="13"
            >
                {esc(key)}:
            </text>
            '''
        )

        svg.append(
            f'''
            <text
                x="145"
                y="{y}"
                fill="{TEXT}"
                font-size="13"
            >
                {esc(value)}
            </text>
            '''
        )

        y += ROW_HEIGHT
        continue


# =========================
# FOOTER
# =========================

svg.append(
    f'''
    <line
        x1="24"
        y1="{HEIGHT - 30}"
        x2="{WIDTH - 24}"
        y2="{HEIGHT - 30}"
        stroke="{BORDER}"
    />
    '''
)

svg.append(
    f'''
    <text
        x="24"
        y="{HEIGHT - 12}"
        fill="{MUTED}"
        font-size="11"
    >
        {esc(HOST)}:~$ _
    </text>
    '''
)

svg.append("</svg>")


# =========================
# WRITE FILE
# =========================

OUT.write_text(
    "".join(svg),
    encoding="utf-8"
)

print(f"wrote {OUT}")

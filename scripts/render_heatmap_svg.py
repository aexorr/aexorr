#!/usr/bin/env python3

"""
Render data/contributions.json as an animated GitHub-style
contribution heatmap SVG.

Input:
    ../data/contributions.json

Output:
    ../contrib-heatmap.svg
"""

import datetime
import json
import os


HERE = os.path.dirname(os.path.abspath(__file__))

IN_PATH = os.path.join(
    HERE,
    "..",
    "data",
    "contributions.json",
)

OUT_PATH = os.path.join(
    HERE,
    "..",
    "contrib-heatmap.svg",
)


# GitHub-style contribution colors
PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]


CELL = 12
GAP = 3
STEP = CELL + GAP

PAD = 22
LEFT_LABEL_W = 30
TOP_LABEL_H = 20
TITLEBAR_H = 30


BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"

MUTED = "#7d8590"
TEXT = "#e6edf3"

ACCENT = "#22d3ee"
GREEN = "#39d353"
GOLD = "#f2cc60"


# Animation timing
COL_T = 0.018
ROW_T = 0.045
CELL_DUR = 0.42


def level_for(count):

    if count == 0:
        return 0

    if count <= 5:
        return 1

    if count <= 15:
        return 2

    if count <= 30:
        return 3

    if count <= 50:
        return 4

    return 5


def build_grid(days):

    first = datetime.date.fromisoformat(
        days[0]["date"]
    )

    # Sunday = 0
    lead_pad = (
        first.weekday() + 1
    ) % 7

    grid = []

    column = [None] * lead_pad

    for day in days:

        date = datetime.date.fromisoformat(
            day["date"]
        )

        weekday = (
            date.weekday() + 1
        ) % 7

        while len(column) < weekday:
            column.append(None)

        column.append(
            (
                day["date"],
                day["count"],
                level_for(day["count"]),
            )
        )

        if len(column) == 7:

            grid.append(column)

            column = []

    if column:

        while len(column) < 7:
            column.append(None)

        grid.append(column)

    return grid


def render(data):

    days = data["days"]

    grid = build_grid(days)

    number_of_columns = len(grid)

    art_width = (
        number_of_columns * STEP
    )

    art_height = 7 * STEP

    # Month labels
    month_labels = []

    seen_months = set()

    for column_index, column in enumerate(grid):

        for cell in column:

            if cell is None:
                continue

            date = datetime.date.fromisoformat(
                cell[0]
            )

            key = (
                date.year,
                date.month,
            )

            if (
                key not in seen_months
                and date.day <= 7
            ):

                seen_months.add(key)

                month_labels.append(
                    (
                        column_index,
                        date.strftime("%b"),
                    )
                )

            break

    canvas_width = (
        PAD
        + LEFT_LABEL_W
        + art_width
        + PAD
    )

    stats_height = 88

    canvas_height = (
        TITLEBAR_H
        + TOP_LABEL_H
        + art_height
        + stats_height
        + PAD
    )

    # CSS animation
    css = f"""
    @keyframes cell {{
        0% {{
            opacity: 0;
            transform: translateY(-6px);
        }}

        100% {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .c {{
        opacity: 0;
        animation:
            cell {CELL_DUR:.2f}s
            cubic-bezier(.2,.8,.2,1)
            both;
    }}
    """.strip()

    parts = [

        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{canvas_width}" '
            f'height="{canvas_height}" '
            f'viewBox="0 0 {canvas_width} {canvas_height}" '
            f'font-family="ui-monospace, SFMono-Regular, '
            f'Menlo, Consolas, monospace">'
        ),

        f"<style>{css}</style>",

        "<defs>",

        (
            f'<linearGradient id="hbg" '
            f'x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{BG2}"/>'
            f'<stop offset="1" stop-color="{BG}"/>'
            f"</linearGradient>"
        ),

        "</defs>",

        (
            f'<rect '
            f'width="{canvas_width}" '
            f'height="{canvas_height}" '
            f'rx="12" '
            f'fill="url(#hbg)"/>'
        ),

        (
            f'<rect '
            f'x="0.5" '
            f'y="0.5" '
            f'width="{canvas_width - 1}" '
            f'height="{canvas_height - 1}" '
            f'rx="12" '
            f'fill="none" '
            f'stroke="{FRAME}" '
            f'stroke-width="1" '
            f'stroke-opacity="0.55"/>'
        ),

        (
            f'<line '
            f'x1="0" '
            f'y1="{TITLEBAR_H}" '
            f'x2="{canvas_width}" '
            f'y2="{TITLEBAR_H}" '
            f'stroke="{FRAME}" '
            f'stroke-opacity="0.35"/>'
        ),
    ]

    # Terminal window dots
    for index, dot_color in enumerate(
        [
            "#ff5f56",
            "#ffbd2e",
            "#27c93f",
        ]
    ):

        parts.append(
            f'<circle '
            f'cx="{PAD + index * 16}" '
            f'cy="{TITLEBAR_H / 2}" '
            f'r="5" '
            f'fill="{dot_color}"/>'
        )

    username = data.get(
        "username",
        "aexorr",
    ).lower()

    parts.append(
        f'<text '
        f'x="{canvas_width / 2}" '
        f'y="{TITLEBAR_H / 2 + 4}" '
        f'fill="{MUTED}" '
        f'font-size="12" '
        f'text-anchor="middle">'
        f'{username}@github: ~/contributions --graph'
        f"</text>"
    )

    grid_top = (
        TITLEBAR_H
        + TOP_LABEL_H
    )

    grid_left = (
        PAD
        + LEFT_LABEL_W
    )

    # Month labels
    for column_index, label in month_labels:

        x = (
            grid_left
            + column_index * STEP
        )

        parts.append(
            f'<text '
            f'x="{x}" '
            f'y="{TITLEBAR_H + 14}" '
            f'fill="{MUTED}" '
            f'font-size="10">'
            f'{label}'
            f"</text>"
        )

    # Weekday labels
    for week_index, week_name in [
        (1, "Mon"),
        (3, "Wed"),
        (5, "Fri"),
    ]:

        y = (
            grid_top
            + week_index * STEP
            + CELL * 0.78
        )

        parts.append(
            f'<text '
            f'x="{PAD}" '
            f'y="{y:.1f}" '
            f'fill="{MUTED}" '
            f'font-size="9">'
            f'{week_name}'
            f"</text>"
        )

    # Contribution boxes
    for column_index, column in enumerate(grid):

        grid_x = (
            grid_left
            + column_index * STEP
        )

        for row_index, cell in enumerate(column):

            if cell is None:
                continue

            date_string, count, level = cell

            grid_y = (
                grid_top
                + row_index * STEP
            )

            delay = (
                column_index * COL_T
                + row_index * ROW_T
            )

            plural = (
                "s"
                if count != 1
                else ""
            )

            parts.append(
                f'<rect '
                f'class="c" '
                f'x="{grid_x}" '
                f'y="{grid_y}" '
                f'width="{CELL}" '
                f'height="{CELL}" '
                f'rx="2.5" '
                f'fill="{PALETTE[level]}" '
                f'style="animation-delay:{delay:.3f}s">'
                f'<title>'
                f'{date_string}: '
                f'{count} contribution{plural}'
                f'</title>'
                f'</rect>'
            )

    # Legend
    legend_y = (
        grid_top
        + art_height
        + 6
    )

    legend_x = (
        canvas_width
        - PAD
        - (
            len(PALETTE)
            * (CELL - 1)
            + 70
        )
    )

    parts.append(
        f'<text '
        f'x="{legend_x}" '
        f'y="{legend_y + CELL * 0.8:.1f}" '
        f'fill="{MUTED}" '
        f'font-size="10" '
        f'text-anchor="end">'
        f'Less'
        f'</text>'
    )

    legend_box_x = (
        legend_x + 8
    )

    for level, color in enumerate(
        PALETTE
    ):

        parts.append(
            f'<rect '
            f'x="{legend_box_x}" '
            f'y="{legend_y}" '
            f'width="{CELL - 1}" '
            f'height="{CELL - 1}" '
            f'rx="2.2" '
            f'fill="{color}"/>'
        )

        legend_box_x += CELL

    parts.append(
        f'<text '
        f'x="{legend_box_x + 4}" '
        f'y="{legend_y + CELL * 0.8:.1f}" '
        f'fill="{MUTED}" '
        f'font-size="10">'
        f'More'
        f'</text>'
    )

    separator_y = (
        legend_y
        + CELL
        + 14
    )

    parts.append(
        f'<line '
        f'x1="0" '
        f'y1="{separator_y}" '
        f'x2="{canvas_width}" '
        f'y2="{separator_y}" '
        f'stroke="{FRAME}" '
        f'stroke-opacity="0.25"/>'
    )

    # Stats
    current_streak = data[
        "current_streak"
    ]["length"]

    longest_streak = data[
        "longest_streak"
    ]["length"]

    total = data[
        "total_contributions"
    ]

    best = data[
        "best_day"
    ]

    date_range = data[
        "range"
    ]

    stats_y = (
        separator_y + 24
    )

    parts.append(
        f'<text '
        f'x="{PAD}" '
        f'y="{stats_y}" '
        f'font-size="13" '
        f'fill="{GREEN}">'
        f'<tspan font-weight="700">'
        f'{total:,}'
        f'</tspan>'
        f'<tspan fill="{MUTED}">'
        f' contributions in the last year'
        f'</tspan>'
        f'</text>'
    )

    parts.append(
        f'<text '
        f'x="{canvas_width - PAD}" '
        f'y="{stats_y}" '
        f'font-size="12" '
        f'fill="{MUTED}" '
        f'text-anchor="end">'
        f'{date_range["start"]}'
        f' &#8594; '
        f'{date_range["end"]}'
        f'</text>'
    )

    stats_y += 24

    parts.append(
        f'<text '
        f'x="{PAD}" '
        f'y="{stats_y}" '
        f'font-size="13" '
        f'fill="{MUTED}">'
        f'current streak '
        f'<tspan '
        f'fill="{ACCENT}" '
        f'font-weight="700">'
        f'{current_streak} days'
        f'</tspan>'
        f'<tspan fill="{MUTED}">'
        f'   ·   longest '
        f'</tspan>'
        f'<tspan '
        f'fill="{ACCENT}" '
        f'font-weight="700">'
        f'{longest_streak} days'
        f'</tspan>'
        f'</text>'
    )

    parts.append(
        f'<text '
        f'x="{canvas_width - PAD}" '
        f'y="{stats_y}" '
        f'font-size="12" '
        f'fill="{MUTED}" '
        f'text-anchor="end">'
        f'best day '
        f'<tspan '
        f'fill="{GOLD}" '
        f'font-weight="700">'
        f'{best["count"]}'
        f'</tspan>'
        f' on {best["date"]}'
        f'</text>'
    )

    parts.append(
        "</svg>"
    )

    return "".join(parts)


if __name__ == "__main__":

    with open(
        IN_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    svg = render(data)

    with open(
        OUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(svg)

    print(
        f"wrote {OUT_PATH} "
        f"({len(svg)} bytes)"
    )

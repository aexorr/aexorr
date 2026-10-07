#!/usr/bin/env python3
"""
Fetch real daily contribution counts from GitHub's public contribution
calendar and write data/contributions.json.

No GitHub token or GraphQL API is required.
"""

import datetime
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup


USERNAME = os.environ.get("GH_PROFILE_USER", "aexorr")

URL = f"https://github.com/users/{USERNAME}/contributions"

OUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "contributions.json",
)


def fetch_days():
    response = requests.get(
        URL,
        headers={
            "User-Agent": "aexorr-profile-readme-bot/1.0"
        },
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    cells = soup.select(
        "td.ContributionCalendar-day"
    )

    if not cells:
        print(
            "No contribution calendar cells found. "
            "GitHub markup may have changed.",
            file=sys.stderr,
        )
        sys.exit(1)

    days = []

    for td in cells:

        date = td.get("data-date")

        if not date:
            continue

        td_id = td.get("id")

        tooltip_el = (
            soup.find(
                "tool-tip",
                attrs={"for": td_id}
            )
            if td_id
            else None
        )

        text = (
            tooltip_el.get_text(strip=True)
            if tooltip_el
            else ""
        )

        if re.search(
            r"no contributions",
            text,
            re.I,
        ):
            count = 0

        else:

            match = re.match(
                r"(\d+)",
                text
            )

            count = (
                int(match.group(1))
                if match
                else 0
            )

        days.append(
            {
                "date": date,
                "count": count,
                "level": int(
                    td.get("data-level") or 0
                ),
            }
        )

    days.sort(
        key=lambda item: item["date"]
    )

    return days


def compute_current_streak(days):

    index = len(days) - 1

    # Today may not be finished yet.
    if days[index]["count"] == 0:
        index -= 1

    streak = 0

    end_index = index

    while (
        index >= 0
        and days[index]["count"] > 0
    ):
        streak += 1
        index -= 1

    start_index = index + 1

    if streak == 0:
        return 0, None, None

    return (
        streak,
        days[start_index]["date"],
        days[end_index]["date"],
    )


def compute_longest_streak(days):

    longest = 0
    run = 0

    longest_start = None
    longest_end = None

    run_start_index = None

    for index, day in enumerate(days):

        if day["count"] > 0:

            if run == 0:
                run_start_index = index

            run += 1

            if run > longest:

                longest = run

                longest_start = days[
                    run_start_index
                ]["date"]

                longest_end = days[
                    index
                ]["date"]

        else:

            run = 0

    return (
        longest,
        longest_start,
        longest_end,
    )


def build_data(days):

    total = sum(
        day["count"]
        for day in days
    )

    active_days = sum(
        1
        for day in days
        if day["count"] > 0
    )

    best = max(
        days,
        key=lambda day: day["count"]
    )

    current_length, current_start, current_end = (
        compute_current_streak(days)
    )

    longest_length, longest_start, longest_end = (
        compute_longest_streak(days)
    )

    monthly = {}

    for day in days:

        month = day["date"][:7]

        monthly[month] = (
            monthly.get(month, 0)
            + day["count"]
        )

    monthly_list = [
        {
            "month": month,
            "total": total,
        }
        for month, total in sorted(
            monthly.items()
        )
    ]

    return {
        "username": USERNAME,

        "generated_at": (
            datetime.datetime.utcnow()
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        ),

        "range": {
            "start": days[0]["date"],
            "end": days[-1]["date"],
        },

        "total_contributions": total,

        "active_days": active_days,

        "avg_per_active_day": (
            round(
                total / active_days,
                1
            )
            if active_days
            else 0
        ),

        "current_streak": {
            "length": current_length,
            "start": current_start,
            "end": current_end,
        },

        "longest_streak": {
            "length": longest_length,
            "start": longest_start,
            "end": longest_end,
        },

        "best_day": {
            "date": best["date"],
            "count": best["count"],
        },

        "monthly": monthly_list,

        "days": days,
    }


if __name__ == "__main__":

    days = fetch_days()

    data = build_data(days)

    output_directory = os.path.dirname(
        OUT_PATH
    )

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    with open(
        OUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2
        )

    print(
        f"wrote {OUT_PATH}: "
        f"{data['total_contributions']} contributions, "
        f"current streak "
        f"{data['current_streak']['length']}, "
        f"longest streak "
        f"{data['longest_streak']['length']}"
    )

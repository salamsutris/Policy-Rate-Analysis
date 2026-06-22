"""
02_descriptive_analysis.py
Spatial maps, box plots, and combined lollipop chart.

Outputs:
  - world_map_choropleth.jpg
  - combined_lollipop_continent.jpg
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
from matplotlib.cm import ScalarMappable
import geopandas as gpd
import numpy as np
import sys, os, warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    load_clean_data, get_active_countries, apply_theme, style_axis,
    save_chart, rate_to_color, PALETTE, COLORS,
    CONTINENT_COLORS, CONTINENT_ORDER, COUNTRY_ISO, COUNTRY_COORDS,
)


def plot_world_map(df, latest_active):
    """Generate choropleth world map with policy rate labels."""
    fig, ax = plt.subplots(figsize=(16, 8))
    apply_theme()
    style_axis(ax, "Global Policy Rate Map (February 2026)", 18)
    ax.grid(False)

    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    rate_data = {
        COUNTRY_ISO[r["country_name"]]: r["policy_rate_pct"]
        for _, r in latest_active.iterrows()
        if r["country_name"] in COUNTRY_ISO
    }
    world["rate"] = world["iso_a3"].map(rate_data)

    cmap = LinearSegmentedColormap.from_list(
        "rates", ["#059669", "#16a34a", "#84cc16", "#eab308", "#f97316", "#ef4444", "#991b1b"]
    )
    bounds = [0, 1, 2, 4, 6, 10, 15, 30]
    norm = BoundaryNorm(bounds, cmap.N)

    world[world["rate"].isna()].plot(ax=ax, color="#f0f0f0", edgecolor="#ccc", linewidth=0.3)
    world[world["rate"].notna()].plot(ax=ax, column="rate", cmap=cmap, norm=norm, edgecolor="#555", linewidth=0.8)

    # Annotate countries
    labels = {
        "ARG": "Argentina\n29.0%", "BRA": "Brazil\n15.0%", "COL": "Colombia\n10.25%",
        "CHL": "Chile\n4.5%", "ISL": "Iceland\n7.25%", "HUN": "Hungary\n6.25%",
        "CZE": "Czech\n3.5%", "GBR": "UK\n3.75%", "DNK": "DNK\n1.6%",
        "CHE": "Swiss\n0%", "IND": "India\n5.25%", "IDN": "IDN\n4.75%",
        "CHN": "China\n3.0%", "JPN": "Japan\n0.75%", "ISR": "Israel\n4.0%",
        "AUS": "Australia\n3.85%", "CAN": "Canada\n2.25%",
    }
    for iso, (lat, lon) in COUNTRY_COORDS.items():
        if iso in rate_data:
            ax.annotate(
                labels.get(iso, ""), (lon, lat), fontsize=9, fontweight="bold",
                color="#1a1a2e", ha="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#bbb", alpha=0.88),
            )

    ax.set_xlim(-170, 180)
    ax.set_ylim(-60, 85)
    ax.set_xticks([])
    ax.set_yticks([])

    cbar = plt.colorbar(
        ScalarMappable(cmap=cmap, norm=norm), ax=ax, shrink=0.5,
        aspect=20, pad=0.01, orientation="horizontal", boundaries=bounds, ticks=bounds,
    )
    cbar.set_label("Policy Rate (%)", fontsize=12, fontweight="bold")

    return save_chart(fig, "world_map_choropleth.jpg")


def plot_combined_lollipop(df, latest_active):
    """Generate grouped lollipop chart by continent with IQR summary."""
    fig, ax = plt.subplots(figsize=(16, 14))
    apply_theme()

    y_data = []
    pos = 0
    for cont in CONTINENT_ORDER:
        sub = latest_active[latest_active["continent"] == cont].sort_values("policy_rate_pct", ascending=False)
        col = CONTINENT_COLORS[cont]
        hist = df[(df["continent"] == cont) & (df["policy_rate_pct"] <= 100)]
        med = hist["policy_rate_pct"].median()
        q1 = hist["policy_rate_pct"].quantile(0.25)
        q3 = hist["policy_rate_pct"].quantile(0.75)
        avg = sub["policy_rate_pct"].mean()

        y_data.append({"pos": pos, "label": f"■ {cont}", "type": "header", "cont": cont})
        pos += 1
        for _, r in sub.iterrows():
            y_data.append({"pos": pos, "label": f"   {r['country_name']}", "type": "country",
                           "cont": cont, "rate": r["policy_rate_pct"]})
            pos += 1
        y_data.append({"pos": pos, "type": "summary", "cont": cont,
                        "label": f"   hist. median: {med:.1f}%  |  IQR: [{q1:.1f}–{q3:.1f}%]  |  current avg: {avg:.1f}%"})
        pos += 1.3

    for d in y_data:
        if d["type"] == "country":
            c = CONTINENT_COLORS[d["cont"]]
            ax.hlines(y=d["pos"], xmin=0, xmax=d["rate"], color=c, alpha=0.4, linewidth=3)
            ax.scatter(d["rate"], d["pos"], color=c, s=120, zorder=5, edgecolors="white", linewidth=1.5)
            ax.annotate(f'{d["rate"]}%', (d["rate"] + 0.4, d["pos"]),
                        fontsize=11, fontweight="bold", color=c, ha="left", va="center")
        elif d["type"] == "header":
            ax.axhspan(d["pos"] - 0.4, d["pos"] + 0.4, xmin=0, xmax=1,
                        color=CONTINENT_COLORS[d["cont"]], alpha=0.06, zorder=0)

    ax.set_yticks([d["pos"] for d in y_data])
    ax.set_yticklabels([d["label"] for d in y_data], fontsize=11)
    for tick, d in zip(ax.get_yticklabels(), y_data):
        if d["type"] == "header":
            tick.set_fontweight("bold"); tick.set_fontsize(14); tick.set_color(CONTINENT_COLORS[d["cont"]])
        elif d["type"] == "summary":
            tick.set_fontsize(9); tick.set_fontstyle("italic"); tick.set_color("#888")
        else:
            tick.set_color("#333")

    ax.invert_yaxis()
    ax.set_xlabel("Policy Rate (%)", fontsize=15, fontweight="bold")
    ax.set_xlim(-0.5, 34)
    ax.set_title("Current Policy Rates Grouped by Continent\nwith Historical Distribution Summary",
                  fontsize=18, fontweight="bold", pad=15, color="#0f172a")

    handles = [mpatches.Patch(color=c, label=n, alpha=0.7) for n, c in CONTINENT_COLORS.items()]
    ax.legend(handles=handles, loc="lower right", fontsize=11, framealpha=0.95)

    return save_chart(fig, "combined_lollipop_continent.jpg")


def main():
    print("DESCRIPTIVE ANALYSIS")
    print("=" * 50)
    df = load_clean_data()
    la = get_active_countries(df)

    plot_world_map(df, la)
    plot_combined_lollipop(df, la)

    print("\nDone.")


if __name__ == "__main__":
    main()

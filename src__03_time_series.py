"""
03_time_series.py
Time series trend charts with phase annotations.

Outputs:
  - time_series_8_economies.jpg
  - regime_transition_heatmap.jpg
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import numpy as np, pandas as pd
import sys, os, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    load_clean_data, apply_theme, style_axis, save_chart,
    PALETTE, COLORS, TIMESERIES_COUNTRIES,
)


def plot_time_series(df):
    """8-economy time series with COVID and hiking phase markers."""
    apply_theme()
    fig, ax = plt.subplots(figsize=(16, 8))

    for c, col in zip(TIMESERIES_COUNTRIES, PALETTE):
        sub = df[(df["country_name"] == c) & (df["year"] >= 2015)].sort_values("date")
        ax.plot(sub["date"], sub["policy_rate_pct"], color=col, linewidth=2.5, label=c, alpha=0.9)

    ax.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2020-06-01"), alpha=0.08, color=COLORS["red"])
    ax.axvspan(pd.Timestamp("2022-03-01"), pd.Timestamp("2022-06-01"), alpha=0.08, color=COLORS["yellow"])
    ax.annotate("COVID-19", (pd.Timestamp("2020-04-15"), 15.5), fontsize=12,
                color=COLORS["red"], fontweight="bold", ha="center")
    ax.annotate("Hiking Cycle", (pd.Timestamp("2022-04-15"), 15.5), fontsize=12,
                color=COLORS["yellow"], fontweight="bold", ha="center")

    ax.set_xlabel("Year", fontsize=14, fontweight="bold")
    ax.set_ylabel("Policy Rate (%)", fontsize=14, fontweight="bold")
    ax.set_title("Policy Rate Trends — 8 Major Economies (2015–2026)", fontsize=18, fontweight="bold", pad=15)
    ax.legend(fontsize=11, loc="upper left", framealpha=0.95, ncol=2)
    return save_chart(fig, "time_series_8_economies.jpg")


def plot_regime_heatmap(df):
    """Regime transition heatmap (14 countries × 9 years)."""
    apply_theme()
    fig, ax = plt.subplots(figsize=(14, 8))
    style_axis(ax, "Monetary Policy Regime Transitions (2018–2026)", 18)
    ax.grid(False)

    countries = [
        "United Kingdom", "Japan", "Australia", "Canada", "India", "Brazil",
        "China", "Indonesia", "Hungary", "Switzerland", "Chile", "Colombia",
        "Iceland", "Czech Republic",
    ]
    short = ["UK", "JP", "AU", "CA", "IN", "BR", "CN", "ID", "HU", "CH", "CL", "CO", "IS", "CZ"]
    years = list(range(2018, 2027))
    regime_map = {
        "Near Zero": 0, "Accommodative": 1, "Neutral": 2,
        "Restrictive": 3, "Very Restrictive": 4, "Emergency High": 5,
    }
    regime_colors = ["#059669", "#16a34a", "#eab308", "#f97316", "#ef4444", "#991b1b"]

    matrix = np.full((len(countries), len(years)), np.nan)
    for i, c in enumerate(countries):
        for j, yr in enumerate(years):
            sub = df[(df["country_name"] == c) & (df["year"] == yr)]
            if len(sub) > 0:
                reg = sub.iloc[-1]["rate_regime"]
                if reg in regime_map:
                    matrix[i, j] = regime_map[reg]

    ax.imshow(matrix, cmap=ListedColormap(regime_colors), aspect="auto", vmin=0, vmax=5)
    ax.set_xticks(range(len(years))); ax.set_xticklabels(years, fontsize=12)
    ax.set_yticks(range(len(short))); ax.set_yticklabels(short, fontsize=11)

    labels = {0: "NZ", 1: "Ac", 2: "Ne", 3: "Re", 4: "VR", 5: "EH"}
    for i in range(len(countries)):
        for j in range(len(years)):
            v = matrix[i, j]
            if not np.isnan(v):
                ax.text(j, i, labels[int(v)], ha="center", va="center", fontsize=9,
                        color="white" if v >= 3 else "#1a1a2e", fontweight="bold")

    handles = [mpatches.Patch(color=c, label=l) for l, c in zip(regime_map.keys(), regime_colors)]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=3, fontsize=10)
    return save_chart(fig, "regime_transition_heatmap.jpg")


def main():
    print("TIME SERIES ANALYSIS")
    print("=" * 50)
    df = load_clean_data()
    plot_time_series(df)
    plot_regime_heatmap(df)
    print("\nDone.")


if __name__ == "__main__":
    main()

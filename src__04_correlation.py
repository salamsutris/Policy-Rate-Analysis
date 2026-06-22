"""
04_correlation.py
Cross-country correlation, rolling continental correlation, and lead-lag analysis.

Outputs:
  - correlation_heatmap.jpg
  - rolling_correlation.jpg
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import numpy as np, pandas as pd
import sys, os, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))
from utils import load_clean_data, apply_theme, style_axis, save_chart, COLORS


CORR_COUNTRIES = [
    "United Kingdom", "Japan", "Australia", "Canada", "India",
    "Brazil", "China", "Indonesia", "Hungary", "Switzerland",
]
SHORT_NAMES = {
    "United Kingdom": "UK", "Japan": "JP", "Australia": "AU", "Canada": "CA",
    "India": "IN", "Brazil": "BR", "China": "CN", "Indonesia": "ID",
    "Hungary": "HU", "Switzerland": "CH",
}


def plot_correlation_heatmap(df):
    """Cross-country Pearson correlation heatmap (2015-2026)."""
    apply_theme()
    fig, ax = plt.subplots(figsize=(12, 10))
    style_axis(ax, "Cross-Country Correlation (2015–2026)", 18)
    ax.grid(False)

    pivot = df[
        df["country_name"].isin(CORR_COUNTRIES) & (df["year"] >= 2015)
    ].pivot_table(index="date", columns="country_name", values="policy_rate_pct")

    corr = pivot.corr()
    corr.columns = [SHORT_NAMES[c] for c in corr.columns]
    corr.index = [SHORT_NAMES[c] for c in corr.index]

    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    cmap = LinearSegmentedColormap.from_list("c", [COLORS["red"], "#f5f5f5", COLORS["blue"]])
    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f", cmap=cmap, center=0, square=True,
        linewidths=1.5, linecolor="white",
        annot_kws={"size": 11, "color": "#1a1a2e", "fontweight": "bold"},
        ax=ax, vmin=-1, vmax=1, cbar_kws={"shrink": 0.8},
    )
    return save_chart(fig, "correlation_heatmap.jpg")


def plot_rolling_correlation(df):
    """Rolling 24-month correlation between continental medians."""
    apply_theme()
    fig, ax = plt.subplots(figsize=(16, 8))
    style_axis(ax, "Rolling 24-Month Continental Correlation", 18)

    monthly = df[df["year"] >= 2000].groupby(["date", "continent"])["policy_rate_pct"].median().reset_index()
    pivot = monthly.pivot(index="date", columns="continent", values="policy_rate_pct").dropna()

    pairs = [
        ("Asia", "Europe", COLORS["yellow"]),
        ("Asia", "North America", COLORS["orange"]),
        ("Europe", "North America", COLORS["blue"]),
        ("Europe", "South America", COLORS["purple"]),
        ("Asia", "South America", COLORS["red"]),
    ]
    for c1, c2, col in pairs:
        if c1 in pivot.columns and c2 in pivot.columns:
            r = pivot[c1].rolling(24).corr(pivot[c2])
            ax.plot(r.index, r.values, color=col, linewidth=2,
                    label=f"{c1[:4]}↔{c2[:4]}", alpha=0.85)

    ax.axhline(0, color="#999", linewidth=1)
    ax.axhline(0.7, color=COLORS["green"], linewidth=0.8, linestyle="--", alpha=0.4)
    ax.axhline(-0.7, color=COLORS["red"], linewidth=0.8, linestyle="--", alpha=0.4)

    # Crisis shading
    for s, e, c in [("2008-09", "2009-06", "#555"), ("2020-03", "2020-12", COLORS["red"]),
                     ("2022-03", "2023-06", COLORS["yellow"])]:
        ax.axvspan(pd.Timestamp(s + "-01"), pd.Timestamp(e + "-01"), alpha=0.05, color=c)

    ax.set_xlabel("Year", fontsize=13)
    ax.set_ylabel("Correlation", fontsize=13)
    ax.set_ylim(-1.1, 1.15)
    ax.legend(fontsize=10, loc="lower left", ncol=2, framealpha=0.95)
    return save_chart(fig, "rolling_correlation.jpg")


def main():
    print("CORRELATION ANALYSIS")
    print("=" * 50)
    df = load_clean_data()
    plot_correlation_heatmap(df)
    plot_rolling_correlation(df)
    print("\nDone.")


if __name__ == "__main__":
    main()

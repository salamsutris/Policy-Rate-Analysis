"""
05_forecasting.py
Linear regression, Holt's ES, and polynomial regression forecasts.

Outputs:
  - linear_{country}.jpg (6 files)
  - holt_{country}.jpg (6 files)
  - forecast_comparison.jpg
"""

import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from scipy import stats as sst
import sys, os, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    load_clean_data, apply_theme, save_chart,
    FORECAST_COUNTRIES, holt_linear_es,
)


def forecast_linear(df, country, color):
    """Generate linear regression forecast chart for one country."""
    apply_theme()
    fig, ax = plt.subplots(figsize=(12, 7))

    sub = df[(df["country_name"] == country) & (df["year"] >= 2018)].sort_values("date")
    y = sub["policy_rate_pct"].values
    recent = sub[sub["year"] >= 2023]
    if len(recent) < 6:
        recent = sub.tail(24)

    xr = np.arange(len(recent))
    yr = recent["policy_rate_pct"].values
    slope, intercept, r_val, _, se = sst.linregress(xr, yr)

    future = pd.date_range(sub["date"].max() + pd.DateOffset(months=1), periods=60, freq="MS")
    xf = np.arange(len(recent), len(recent) + 60)
    yf = np.clip(slope * xf + intercept, 0, y.max() * 1.5)
    yu = np.clip(yf + 1.96 * se * np.sqrt(xf), 0, y.max() * 2)
    yl = np.clip(yf - 1.96 * se * np.sqrt(xf), 0, y.max() * 2)

    ax.plot(sub["date"], y, color=color, linewidth=3, label="Historical", zorder=3)
    ax.plot(future, yf, color=color, linewidth=2.5, linestyle="--", label="Forecast", zorder=3)
    ax.fill_between(future, yl, yu, alpha=0.12, color=color, label="95% CI")
    ax.axvline(sub["date"].max(), color="#aaa", linewidth=1.2, linestyle=":", alpha=0.7)

    sign = "+" if intercept >= 0 else "−"
    ax.text(0.03, 0.97,
            f"Linear Regression (OLS)\n"
            f"ŷ = {slope:.4f}·t {sign} {abs(intercept):.2f}\n"
            f"R² = {r_val**2:.4f},  SE = {se:.4f}\n"
            f"Current: {y[-1]:.2f}%  →  2031: {max(0, yf[-1]):.2f}%",
            transform=ax.transAxes, fontsize=12, va="top", fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8fafc", edgecolor="#ddd", alpha=0.95))

    ax.set_xlabel("Year", fontsize=14, fontweight="bold")
    ax.set_ylabel("Policy Rate (%)", fontsize=14, fontweight="bold")
    ax.set_title(f"{country} — Linear Regression Forecast", fontsize=17, fontweight="bold", pad=12)
    ax.legend(fontsize=12, loc="best", framealpha=0.95)

    fname = country.replace(" ", "_").lower()
    return save_chart(fig, f"linear_{fname}.jpg")


def forecast_holt(df, country, color):
    """Generate Holt's ES forecast chart for one country."""
    apply_theme()
    fig, ax = plt.subplots(figsize=(12, 7))

    sub = df[(df["country_name"] == country) & (df["year"] >= 2018)].sort_values("date")
    y = sub["policy_rate_pct"].values
    fc, up, lo, level, trend = holt_linear_es(y)
    future = pd.date_range(sub["date"].max() + pd.DateOffset(months=1), periods=60, freq="MS")

    fc = np.clip(fc, 0, y.max() * 1.5)
    up = np.clip(up, 0, y.max() * 2)
    lo = np.clip(lo, 0, y.max() * 2)

    ax.plot(sub["date"], y, color=color, linewidth=3, label="Historical", zorder=3)
    ax.plot(sub["date"], level, color="#aaa", linewidth=1.2, linestyle=":", alpha=0.5, label="Level")
    ax.plot(future, fc, color=color, linewidth=2.5, linestyle="--", label="Forecast", zorder=3)
    ax.fill_between(future, lo, up, alpha=0.12, color=color, label="95% PI")
    ax.axvline(sub["date"].max(), color="#aaa", linewidth=1.2, linestyle=":", alpha=0.7)

    td = "↑" if trend[-1] > 0.01 else "↓" if trend[-1] < -0.01 else "→"
    ax.text(0.03, 0.97,
            f"Holt's Linear ES\n"
            f"Lₜ = α·Yₜ + (1−α)·(Lₜ₋₁+Tₜ₋₁)\n"
            f"α = 0.3,  β = 0.1\n"
            f"Trend: {trend[-1]:+.4f}/mo ({td})\n"
            f"Current: {y[-1]:.2f}%  →  2031: {max(0, fc[-1]):.2f}%",
            transform=ax.transAxes, fontsize=12, va="top", fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8fafc", edgecolor="#ddd", alpha=0.95))

    ax.set_xlabel("Year", fontsize=14, fontweight="bold")
    ax.set_ylabel("Policy Rate (%)", fontsize=14, fontweight="bold")
    ax.set_title(f"{country} — Holt's ES Forecast", fontsize=17, fontweight="bold", pad=12)
    ax.legend(fontsize=12, loc="best", framealpha=0.95)

    fname = country.replace(" ", "_").lower()
    return save_chart(fig, f"holt_{fname}.jpg")


def plot_forecast_comparison(df):
    """Grouped bar chart comparing 3 model forecasts for 6 countries."""
    apply_theme()
    fig, ax = plt.subplots(figsize=(16, 9))

    BL, GR, YL = "#2563eb", "#059669", "#d97706"
    summary = []
    for country, col in FORECAST_COUNTRIES:
        sub = df[(df["country_name"] == country) & (df["year"] >= 2018)].sort_values("date")
        y = sub["policy_rate_pct"].values
        cur = y[-1]
        rc = sub[sub["year"] >= 2023]
        if len(rc) < 6: rc = sub.tail(24)
        sl, ic, rv, _, _ = sst.linregress(np.arange(len(rc)), rc["policy_rate_pct"].values)
        lin = max(0, sl * (len(rc) + 60) + ic)
        hf, _, _, _, _ = holt_linear_es(y)
        hv = max(0, hf[-1])
        co = np.polyfit(np.arange(len(sub)), y, 3)
        pv = max(0, np.poly1d(co)(len(sub) + 60))
        summary.append({"c": country, "cur": cur, "lin": lin, "holt": hv, "poly": pv})

    x = np.arange(len(summary))
    w = 0.18
    ax.bar(x - 1.5 * w, [s["cur"] for s in summary], w, label="Current (Feb 2026)", color="#64748b", edgecolor="white")
    ax.bar(x - 0.5 * w, [s["lin"] for s in summary], w, label="Linear Reg. (2031)", color=BL, edgecolor="white")
    ax.bar(x + 0.5 * w, [s["holt"] for s in summary], w, label="Holt's ES (2031)", color=GR, edgecolor="white")
    ax.bar(x + 1.5 * w, [s["poly"] for s in summary], w, label="Polynomial (2031)", color=YL, edgecolor="white")

    for bars in [ax.containers[0], ax.containers[1], ax.containers[2], ax.containers[3]]:
        for bar in bars:
            h = bar.get_height()
            if h > 0.5:
                ax.annotate(f"{h:.1f}", (bar.get_x() + bar.get_width() / 2, h),
                            ha="center", va="bottom", fontsize=9, fontweight="bold", color="#333")

    ax.set_xticks(x)
    ax.set_xticklabels([s["c"] for s in summary], fontsize=13, fontweight="bold")
    ax.set_ylabel("Policy Rate (%)", fontsize=14, fontweight="bold")
    ax.set_title("Forecast Comparison: Current vs. 2031 Estimates", fontsize=20, fontweight="bold", pad=15)
    ax.legend(fontsize=12, loc="upper right", framealpha=0.95)
    return save_chart(fig, "forecast_comparison.jpg")


def main():
    print("FORECASTING ANALYSIS")
    print("=" * 50)
    df = load_clean_data()

    for country, color in FORECAST_COUNTRIES:
        forecast_linear(df, country, color)
        forecast_holt(df, country, color)

    plot_forecast_comparison(df)
    print("\nDone.")


if __name__ == "__main__":
    main()

"""
Shared constants, color palettes, themes, and helper functions
used across all analysis scripts.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# ═══════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
OUTPUT_DIR = os.path.join(ROOT_DIR, "outputs")
RAW_CSV = os.path.join(DATA_DIR, "Buku1.csv")
CLEAN_CSV = os.path.join(DATA_DIR, "cleaned.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════
# COLOR PALETTE
# ═══════════════════════════════════════════════
COLORS = {
    "blue": "#2563eb",
    "red": "#dc2626",
    "green": "#059669",
    "yellow": "#d97706",
    "purple": "#7c3aed",
    "pink": "#db2777",
    "orange": "#ea580c",
    "cyan": "#0891b2",
    "indigo": "#4f46e5",
    "lime": "#16a34a",
}

PALETTE = list(COLORS.values())

CONTINENT_COLORS = {
    "South America": COLORS["red"],
    "Europe": COLORS["blue"],
    "Asia": COLORS["yellow"],
    "North America": COLORS["green"],
    "Oceania": COLORS["purple"],
}

CONTINENT_ORDER = [
    "South America", "Europe", "Asia", "Oceania", "North America"
]

# Country ISO mapping for spatial analysis
COUNTRY_ISO = {
    "Argentina": "ARG", "Brazil": "BRA", "Colombia": "COL",
    "Chile": "CHL", "Iceland": "ISL", "Hungary": "HUN",
    "Czech Republic": "CZE", "United Kingdom": "GBR",
    "Denmark": "DNK", "Switzerland": "CHE", "India": "IND",
    "Indonesia": "IDN", "China": "CHN", "Japan": "JPN",
    "Israel": "ISR", "Hong Kong": "HKG", "Australia": "AUS",
    "Canada": "CAN",
}

# Coordinates for map annotations
COUNTRY_COORDS = {
    "ARG": (-38, -62), "BRA": (-10, -52), "COL": (4, -72),
    "CHL": (-33, -76), "ISL": (65, -18), "HUN": (47, 20),
    "CZE": (50, 15), "GBR": (54, -4), "DNK": (56, 10),
    "CHE": (47, 8), "IND": (22, 80), "IDN": (-3, 118),
    "CHN": (36, 103), "JPN": (37, 140), "ISR": (31, 35),
    "AUS": (-26, 134), "CAN": (58, -98),
}

# ═══════════════════════════════════════════════
# MATPLOTLIB THEME (white background, print-ready)
# ═══════════════════════════════════════════════
def apply_theme():
    """Apply consistent matplotlib theme for all charts."""
    plt.rcParams.update({
        "figure.facecolor": "#ffffff",
        "axes.facecolor": "#ffffff",
        "text.color": "#1a1a2e",
        "axes.labelcolor": "#1a1a2e",
        "xtick.color": "#444444",
        "ytick.color": "#444444",
        "axes.edgecolor": "#cccccc",
        "grid.color": "#e8e8e8",
        "grid.alpha": 0.8,
        "font.family": "DejaVu Sans",
        "font.size": 12,
        "axes.grid": True,
        "grid.linewidth": 0.5,
    })


def style_axis(ax, title="", fontsize=18):
    """Apply consistent styling to a matplotlib axis."""
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_color("#d0d0d0")
        spine.set_linewidth(0.8)
    if title:
        ax.set_title(
            title, fontsize=fontsize, fontweight="bold",
            color="#1a1a2e", pad=12, loc="left"
        )
    ax.tick_params(colors="#555", labelsize=11)
    ax.grid(True, alpha=0.3, linewidth=0.5, color="#e0e0e0")


def rate_to_color(rate):
    """Map a policy rate to a color from green (low) to red (high)."""
    if rate <= 1:
        return "#059669"
    elif rate <= 3:
        return "#16a34a"
    elif rate <= 5:
        return COLORS["yellow"]
    elif rate <= 8:
        return COLORS["orange"]
    elif rate <= 15:
        return COLORS["red"]
    else:
        return "#991b1b"


# ═══════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════
def load_raw_data():
    """Load and clean the raw BIS CSV file."""
    with open(RAW_CSV, "r", encoding="utf-8-sig") as f:
        header = f.readline().strip()
        data_lines = []
        for line in f:
            line = line.strip()
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            line = line.replace('""', '"')
            data_lines.append(line)

    with open(CLEAN_CSV, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for line in data_lines:
            f.write(line + "\n")

    return load_clean_data()


def load_clean_data():
    """Load the cleaned CSV into a DataFrame."""
    df = pd.read_csv(CLEAN_CSV, quoting=1)
    df = df.dropna(subset=["country_name"])
    df["date"] = pd.to_datetime(df["date"])
    return df


def get_active_countries(df, cutoff="2024-01-01"):
    """Return latest data for countries active since cutoff."""
    latest = df.sort_values("date").groupby("country_name").last().reset_index()
    return latest[latest["date"] >= pd.Timestamp(cutoff)]


def save_chart(fig, filename, dpi=300):
    """Save figure to outputs directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    size_kb = os.path.getsize(path) / 1024
    print(f"  ✅ {filename} ({size_kb:.0f} KB)")
    return path


# ═══════════════════════════════════════════════
# FORECASTING HELPERS
# ═══════════════════════════════════════════════
def holt_linear_es(y, alpha=0.3, beta=0.1, h=60):
    """
    Holt's Linear Exponential Smoothing.

    Parameters:
        y     : array of observed values
        alpha : level smoothing parameter (0 < alpha < 1)
        beta  : trend smoothing parameter (0 < beta < 1)
        h     : forecast horizon (months ahead)

    Returns:
        forecast : h-step ahead forecasts
        upper    : 95% prediction interval upper bound
        lower    : 95% prediction interval lower bound
        level    : smoothed level series
        trend    : smoothed trend series
    """
    n = len(y)
    level = np.zeros(n)
    trend = np.zeros(n)
    level[0] = y[0]
    trend[0] = y[1] - y[0] if n > 1 else 0

    for t in range(1, n):
        level[t] = alpha * y[t] + (1 - alpha) * (level[t - 1] + trend[t - 1])
        trend[t] = beta * (level[t] - level[t - 1]) + (1 - beta) * trend[t - 1]

    forecast = np.array([level[-1] + (i + 1) * trend[-1] for i in range(h)])

    residuals = y[1:] - (level[:-1] + trend[:-1])
    sigma = np.std(residuals) if len(residuals) > 0 else 1.0
    steps = np.arange(1, h + 1)
    upper = forecast + 1.96 * sigma * np.sqrt(steps)
    lower = forecast - 1.96 * sigma * np.sqrt(steps)

    return forecast, upper, lower, level, trend


# Forecast-eligible countries (6 selected for presentation)
FORECAST_COUNTRIES = [
    ("United Kingdom", COLORS["blue"]),
    ("Japan", COLORS["red"]),
    ("Australia", COLORS["green"]),
    ("India", COLORS["purple"]),
    ("Brazil", COLORS["pink"]),
    ("China", COLORS["orange"]),
]

# Time series display countries (8 major economies)
TIMESERIES_COUNTRIES = [
    "United Kingdom", "Japan", "Australia", "Canada",
    "India", "Brazil", "China", "Indonesia",
]

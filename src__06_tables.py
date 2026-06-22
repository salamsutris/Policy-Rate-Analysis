"""
06_tables.py
Publication-quality tables with LaTeX mathtext equations.

Outputs:
  - methodology_equations_table.jpg
  - forecast_results_table.jpg
  - correlation_results_table.jpg
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from utils import save_chart, COLORS

BL, RD, GR, YL, PR = COLORS["blue"], COLORS["red"], COLORS["green"], COLORS["yellow"], COLORS["purple"]
NV = "#0f172a"


def plot_methodology_table():
    """Generate methodology equations table with LaTeX mathtext."""
    fig, ax = plt.subplots(figsize=(20, 16))
    ax.axis("off")
    ax.text(0.5, 0.98, "Mathematical Framework", fontsize=24, fontweight="bold",
            ha="center", va="top", color=NV, transform=ax.transAxes)

    headers = ["#", "Method", "Formula", "Parameters", "Application"]
    cx = [0.01, 0.04, 0.20, 0.64, 0.80]
    cw = [0.03, 0.16, 0.44, 0.16, 0.20]
    rh, sy = 0.085, 0.92

    for i, (h, x) in enumerate(zip(headers, cx)):
        ax.add_patch(mpatches.Rectangle((x, sy), cw[i], 0.035, facecolor=NV, edgecolor="white"))
        ax.text(x + cw[i] / 2, sy + 0.0175, h, fontsize=13, fontweight="bold",
                color="white", ha="center", va="center", transform=ax.transAxes)

    rows = [
        {"n": "1", "m": "Pearson\nCorrelation",
         "f": [r"$r_{XY} = \frac{\sum(X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum(X_i-\bar{X})^2 \cdot \sum(Y_i-\bar{Y})^2}}$"],
         "p": "Range: [-1, +1]\n|r| > 0.7 = strong", "u": "Cross-country\nsynchronization", "bg": "#eff6ff"},
        {"n": "2", "m": "Rolling\nCorrelation",
         "f": [r"$r_t = \mathrm{Corr}(X_{[t-w+1:t]},\ Y_{[t-w+1:t]})$"],
         "p": "Window:\nw = 24 months", "u": "Time-varying\naccordion pattern", "bg": "#fff"},
        {"n": "3", "m": "Cross-Corr.\nLag Analysis",
         "f": [r"$k^* = \arg\max_{k \in \{0,...,6\}}\ |r(X_t, Y_{t+k})|$"],
         "p": "Lag range:\nk = 0 to 6 mo", "u": "Lead-lag\nidentification", "bg": "#eff6ff"},
        {"n": "4", "m": "Linear\nRegression",
         "f": [r"$\hat{R}_t = \hat{\beta} \cdot t + \hat{\alpha}$",
               r"$R^2 = 1 - SS_{res}/SS_{tot}$",
               r"CI: $\hat{R}_{t+h} \pm 1.96 \cdot SE \cdot \sqrt{h}$"],
         "p": "Fitted: 2023-26\nh = 60 months", "u": "Forecast:\nstable trends", "bg": "#fff"},
        {"n": "5", "m": "Holt's\nLinear ES",
         "f": [r"$L_t = \alpha Y_t + (1-\alpha)(L_{t-1}+T_{t-1})$",
               r"$T_t = \beta(L_t - L_{t-1}) + (1-\beta)T_{t-1}$",
               r"$\hat{R}_{t+h} = L_t + h \cdot T_t$"],
         "p": "a = 0.3 (level)\nb = 0.1 (trend)\nh = 60 months", "u": "Forecast:\nadaptive level\n& trend", "bg": "#eff6ff"},
        {"n": "6", "m": "Polynomial\n(Degree 3)",
         "f": [r"$\hat{R}_t = a t^3 + b t^2 + c t + d$",
               r"OLS on $[t^3, t^2, t, 1]$"],
         "p": "Fitted: 2018-26\nDegree: 3", "u": "Cycle shape\n(extrap. risk)", "bg": "#fff"},
        {"n": "7", "m": "Descriptive\nStatistics",
         "f": [r"$\tilde{R} = R_{(\frac{n+1}{2})}$  (median)",
               r"$IQR = Q_3 - Q_1$",
               r"$s = \sqrt{\frac{1}{n-1}\sum(R_i-\bar{R})^2}$"],
         "p": "Median used\n(mean distorted\n9x by outliers)", "u": "Central tendency\n& dispersion", "bg": "#eff6ff"},
        {"n": "8", "m": "Sync\nScore",
         "f": [r"$S(t) = \frac{\max(C_{hike}, C_{cut})}{C_{total}} \times 100\%$"],
         "p": "Per year\n5 continents", "u": "Continental\nalignment", "bg": "#fff"},
    ]

    for idx, row in enumerate(rows):
        y = sy - (idx + 1) * rh - 0.035
        for i, x in enumerate(cx):
            ax.add_patch(mpatches.Rectangle((x, y), cw[i], rh, facecolor=row["bg"], edgecolor="#e0e0e0", linewidth=0.5))
        ax.text(cx[0] + cw[0] / 2, y + rh / 2, row["n"], fontsize=14, fontweight="bold",
                color=BL, ha="center", va="center", transform=ax.transAxes)
        ax.text(cx[1] + cw[1] / 2, y + rh / 2, row["m"], fontsize=12, fontweight="bold",
                color=NV, ha="center", va="center", transform=ax.transAxes, linespacing=1.4)
        n_lines = len(row["f"])
        fy_start = y + rh / 2 + (n_lines - 1) * 0.013
        for fi, fl in enumerate(row["f"]):
            ax.text(cx[2] + cw[2] / 2, fy_start - fi * 0.026, fl, fontsize=15,
                    color=NV, ha="center", va="center", transform=ax.transAxes)
        ax.text(cx[3] + cw[3] / 2, y + rh / 2, row["p"], fontsize=10, color="#555",
                ha="center", va="center", transform=ax.transAxes, linespacing=1.4)
        ax.text(cx[4] + cw[4] / 2, y + rh / 2, row["u"], fontsize=10, color="#555",
                ha="center", va="center", transform=ax.transAxes, linespacing=1.4)

    return save_chart(fig, "methodology_equations_table.jpg")


def main():
    print("PUBLICATION TABLES")
    print("=" * 50)
    plot_methodology_table()
    print("\nDone.")


if __name__ == "__main__":
    main()

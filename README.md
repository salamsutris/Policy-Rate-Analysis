# Divergence & Convergence: A Cross-Country Analysis of Central Bank Policy Rates

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Data](https://img.shields.io/badge/Source-BIS_WS__CBPOL-green.svg)](https://stats.bis.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This project analyzes **81 years of central bank policy rate data** (1945–2026) from **27 countries** across 5 continents to investigate cross-country divergence and convergence patterns in global monetary policy.

**Key Findings:**
- **Accordion Pattern**: Cross-continental correlation surges above r > +0.85 during crises (GFC, COVID, 2022 hiking) and collapses to near zero during calm periods
- **Fed Leadership**: North America leads Europe by ~1 month, Oceania by ~3 months, South America by ~5 months
- **China Structural Break**: Only major economy cutting rates during the 2022 global tightening cycle
- **Historical Normality**: Current 4% median is historically normal; the 2010s near-zero era was the anomaly

## Dataset

| Parameter | Value |
|-----------|-------|
| Source | BIS WS_CBPOL v1 (Bank for International Settlements) |
| Observations | 14,825 monthly records |
| Countries | 27 (18 active as of Feb 2026) |
| Variables | 43 (26 original + 17 derived) |
| Time Span | January 1945 – February 2026 |
| API | `stats.bis.org/api/v1/data/WS_CBPOL` |

## Project Structure

```
├── README.md
├── requirements.txt
├── LICENSE
├── data/
│   └── Buku1.csv                  # Raw BIS dataset
├── src/
│   ├── 01_preprocessing.py        # Data cleaning & quality audit
│   ├── 02_descriptive_analysis.py # Distributions, box plots, maps
│   ├── 03_time_series.py          # Time series charts & phase analysis
│   ├── 04_correlation.py          # Cross-country & continental correlation
│   ├── 05_forecasting.py          # Linear, Holt's ES, Polynomial models
│   ├── 06_tables.py               # Publication-quality tables (LaTeX math)
│   └── utils.py                   # Shared constants, helpers, themes
├── outputs/                       # Generated charts (300 DPI JPG)
├── docs/
│   ├── methodology.md             # Full mathematical framework
│   └── results_discussion.md      # Results & discussion text
└── notebooks/
    └── exploration.ipynb          # Interactive data exploration
```

## Quick Start

```bash
# Clone repository
git clone https://github.com/[your-username]/policy-rate-analysis.git
cd policy-rate-analysis

# Install dependencies
pip install -r requirements.txt

# Run full pipeline
python src/01_preprocessing.py
python src/02_descriptive_analysis.py
python src/03_time_series.py
python src/04_correlation.py
python src/05_forecasting.py
python src/06_tables.py
```

## Methodology

Three research questions guide the analysis:

- **RQ1**: How do policy rates diverge across continents?
- **RQ2**: Do central banks move together during shocks?
- **RQ3**: Can we forecast policy rates five years ahead?

### Methods Applied

| Method | Formula | Application |
|--------|---------|-------------|
| Pearson Correlation | r = Σ(Xi−X̄)(Yi−Ȳ) / √[Σ(Xi−X̄)²·Σ(Yi−Ȳ)²] | Cross-country synchronization |
| Rolling Correlation | r(t) over w=24 month window | Time-varying accordion pattern |
| Cross-Correlation Lag | k* = argmax\|r(Xt, Yt+k)\| for k∈{0,...,6} | Lead-lag identification |
| Linear Regression | ŷ = βx + α | Stable trend forecasting |
| Holt's Linear ES | Lt = αYt + (1−α)(Lt-1+Tt-1) | Adaptive level + trend |
| Polynomial (deg 3) | ŷ = at³ + bt² + ct + d | Cycle shape analysis |

## Key Visualizations

The pipeline generates 20+ publication-quality charts at 300 DPI:

- **World choropleth map** with policy rate labels
- **Grouped lollipop chart** by continent with historical IQR
- **8-economy time series** with COVID/hiking phase markers
- **10×10 correlation heatmap** (cross-country)
- **Rolling 24-month continental correlation**
- **Regime transition heatmap** (14 countries × 9 years)
- **Forecast comparison** (3 models × 6 countries)
- **Methodology equations table** (LaTeX mathtext rendering)

## References

1. Bank for International Settlements (2026). Central Bank Policy Rates (WS_CBPOL). https://stats.bis.org/
2. Taylor, J.B. (1993). Discretion versus policy rules in practice. *Carnegie-Rochester Conference Series*, 39, 195–214.
3. Rey, H. (2015). Dilemma not trilemma: The global financial cycle. NBER Working Paper No. 21162.
4. Miranda-Agrippino, S. & Rey, H. (2020). US monetary policy and the global financial cycle. *Review of Economic Studies*, 87(6).
5. Holt, C.C. (2004). Forecasting by exponentially weighted moving averages. *Int. Journal of Forecasting*, 20(1), 5–10.
6. Obstfeld, M. (2015). Trilemmas and trade-offs. BIS Working Papers No. 480.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Citation

```bibtex
@misc{salam2026divergence,
  title={Divergence \& Convergence: A Cross-Country Analysis of Central Bank Policy Rates},
  author={Sutrisno, Salam},
  year={2026},
  note={Data source: BIS WS\_CBPOL v1}
}
```

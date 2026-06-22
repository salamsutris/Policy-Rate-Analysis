"""
01_preprocessing.py
Data cleaning, quality audit, and preprocessing report.

Input:  data/Buku1.csv (raw BIS export)
Output: data/cleaned.csv + console audit report
"""

import pandas as pd
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from utils import load_raw_data, CLEAN_CSV

def main():
    print("=" * 70)
    print("PREPROCESSING & DATA QUALITY AUDIT")
    print("=" * 70)

    # Step 1: Clean CSV format (BOM, row quoting, escaped quotes)
    print("\n[1/5] Cleaning CSV format...")
    df = load_raw_data()
    print(f"  Loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"  Saved cleaned file to: {CLEAN_CSV}")

    # Step 2: Basic structure
    print(f"\n[2/5] Dataset structure:")
    print(f"  Countries:      {df['country_name'].nunique()}")
    print(f"  Date range:     {df['date'].min().strftime('%Y-%m')} to {df['date'].max().strftime('%Y-%m')}")
    print(f"  Year range:     {int(df['year'].min())}–{int(df['year'].max())} ({int(df['year'].max()-df['year'].min())+1} years)")
    print(f"  Continents:     {df['continent'].nunique()}")

    # Step 3: Missing values
    print(f"\n[3/5] Missing values:")
    total_cells = df.shape[0] * df.shape[1]
    total_null = df.isnull().sum().sum()
    print(f"  Total null cells: {total_null:,} / {total_cells:,} ({total_null/total_cells*100:.2f}%)")
    for col in df.columns:
        n = df[col].isnull().sum()
        if n > 10:
            print(f"    {col}: {n:,} ({n/len(df)*100:.1f}%)")

    # Step 4: Duplicates
    print(f"\n[4/5] Duplicates:")
    print(f"  Full row duplicates:    {df.duplicated().sum()}")
    print(f"  Country+date duplicates: {df.duplicated(subset=['country_name','date']).sum()}")

    # Step 5: Outlier analysis
    print(f"\n[5/5] Outlier analysis (hyperinflation):")
    rates = df["policy_rate_pct"]
    print(f"  Min:    {rates.min():.2f}%")
    print(f"  Max:    {rates.max():,.2f}%")
    print(f"  Mean:   {rates.mean():.2f}% (WITH hyperinflation)")
    print(f"  Median: {rates.median():.2f}% (robust)")

    normal = df[df["policy_rate_pct"] <= 100]["policy_rate_pct"]
    print(f"  Mean (≤100%): {normal.mean():.2f}%")
    print(f"  Distortion factor: {rates.mean()/normal.mean():.1f}×")
    print(f"  Rows >100%: {(rates > 100).sum()} ({(rates > 100).sum()/len(df)*100:.2f}%)")

    # Panel balance
    print(f"\n  Panel balance:")
    active = df.groupby("country_name").agg(
        start=("date", "min"), end=("date", "max"), months=("date", "count")
    ).sort_values("months", ascending=False)
    for _, r in active.iterrows():
        print(f"    {r.name:20s} {r['start'].strftime('%Y-%m')} → {r['end'].strftime('%Y-%m')} ({r['months']} months)")

    print(f"\n{'='*70}")
    print("PREPROCESSING COMPLETE")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()

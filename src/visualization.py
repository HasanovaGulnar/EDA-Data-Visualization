from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "analysis_data.csv"
FIGURES = ROOT / "reports" / "figures"

sns.set_theme(style="whitegrid")


def save_plot(filename):
    plt.tight_layout()
    plt.savefig(
        FIGURES / filename,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date")
    parser.add_argument("--target")
    args = parser.parse_args()

    FIGURES.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA)

    numeric = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # 1. Missing values
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values()

    if not missing.empty:
        plt.figure(figsize=(10, 6))
        missing.plot(kind="barh")
        plt.title("Missing Values by Column")
        plt.xlabel("Missing Count")
        save_plot("missing_values.png")

    # 2. Numeric distributions
    for i, col in enumerate(numeric[:6], 1):
        values = df[col].replace(
            [np.inf, -np.inf], np.nan
        ).dropna()

        if values.empty:
            continue

        plt.figure(figsize=(9, 5))
        sns.histplot(
            values,
            kde=values.nunique() > 1,
            bins=30
        )
        plt.title(f"Distribution: {col}")
        plt.xlabel(col)
        save_plot(f"histogram_{i}.png")

        plt.figure(figsize=(9, 4))
        sns.boxplot(x=values)
        plt.title(f"Outlier Analysis: {col}")
        save_plot(f"boxplot_{i}.png")

    # 3. Correlation heatmap
    valid_numeric = [
        c for c in numeric
        if df[c].nunique() > 1
    ]

    if len(valid_numeric) >= 2:
        corr = df[valid_numeric].corr()

        plt.figure(figsize=(11, 8))
        sns.heatmap(
            corr,
            annot=len(valid_numeric) <= 10,
            fmt=".2f",
            cmap="coolwarm",
            center=0
        )
        plt.title("Correlation Heatmap")
        save_plot("correlation_heatmap.png")

    # 4. Categorical variables
    for i, col in enumerate(categorical[:4], 1):
        counts = (
            df[col]
            .value_counts()
            .head(10)
            .sort_values()
        )

        if counts.empty:
            continue

        plt.figure(figsize=(10, 6))
        counts.plot(kind="barh")
        plt.title(f"Top Categories: {col}")
        plt.xlabel("Count")
        save_plot(f"categories_{i}.png")

    # 5. Target vs category
    if args.target:
        if args.target not in df.columns:
            raise ValueError("Target column not found.")

        if args.target not in numeric:
            raise ValueError("Target must be numeric.")

        if categorical:
            group = categorical[0]

            if df[group].nunique() <= 20:
                summary = (
                    df.groupby(group)[args.target]
                    .mean()
                    .sort_values()
                )

                plt.figure(figsize=(10, 6))
                summary.plot(kind="barh")
                plt.title(
                    f"Average {args.target} by {group}"
                )
                plt.xlabel(f"Mean {args.target}")
                save_plot("target_by_category.png")

    # 6. Time series
    if args.date:
        if args.date not in df.columns:
            raise ValueError("Date column not found.")

        df[args.date] = pd.to_datetime(
            df[args.date],
            errors="coerce"
        )

        valid = df.dropna(subset=[args.date]).copy()

        if not valid.empty:
            valid["month"] = (
                valid[args.date].dt.to_period("M")
                .dt.to_timestamp()
            )

            if args.target:
                if args.target not in numeric:
                    raise ValueError(
                        "Target must be numeric."
                    )

                monthly = valid.groupby("month")[
                    args.target
                ].sum()

                ylabel = f"Monthly sum of {args.target}"
            else:
                monthly = (
                    valid.groupby("month").size()
                )
                ylabel = "Monthly record count"

            plt.figure(figsize=(11, 5))
            monthly.plot(marker="o")
            plt.title("Monthly Trend")
            plt.ylabel(ylabel)
            plt.xlabel("Month")
            save_plot("monthly_trend.png")

    print("Visualizations completed.")
    print(f"Figures saved to: {FIGURES}")


if __name__ == "__main__":
    main()

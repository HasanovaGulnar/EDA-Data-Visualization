from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"


def load_data():
    files = sorted(RAW.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            "CSV dataset tapilmadi. Fayli data/raw qovluguna qoy."
        )

    path = files[0]
    print(f"Loading dataset: {path.name}")

    try:
        df = pd.read_csv(path, sep=None, engine="python")
    except UnicodeDecodeError:
        df = pd.read_csv(
            path,
            sep=None,
            engine="python",
            encoding="cp1252"
        )

    if df.empty:
        raise ValueError("Dataset bosdur.")

    df.columns = df.columns.astype(str).str.strip()

    if not df.columns.is_unique:
        raise ValueError("Tekrarlanan sutun adlari var.")

    return df


def statistical_test(df, target, group):
    if not target or not group:
        return [
            "## Hypothesis testing",
            "Hipotez testi teyin edilmeyib.",
            "Datasetin meqsedine uygun hipotez evvelceden secilmelidir."
        ]

    if target not in df.columns or group not in df.columns:
        raise ValueError("Target ve ya group sutunu tapilmadi.")

    if not pd.api.types.is_numeric_dtype(df[target]):
        raise ValueError("Target numeric sutun olmalidir.")

    sample = df[[target, group]].dropna()
    groups = list(sample.groupby(group))

    if len(groups) != 2:
        raise ValueError(
            "Welch t-test ucun group sutununda "
            "tam olaraq iki qrup olmalidir."
        )

    a = groups[0][1][target]
    b = groups[1][1][target]

    if min(len(a), len(b)) < 2:
        raise ValueError("Her qrupda en azi 2 musahide olmalidir.")

    if a.var() == 0 and b.var() == 0:
        raise ValueError("Her iki qrupda variasiya sifirdir.")

    result = stats.ttest_ind(
        a,
        b,
        equal_var=False,
        nan_policy="omit"
    )

    p = result.pvalue

    return [
        "## Exploratory hypothesis test",
        f"Target: {target}",
        f"Groups: {groups[0][0]} / {groups[1][0]}",
        "",
        "H0: Iki qrupun populyasiya ortalamalari beraberdir.",
        "H1: Populyasiya ortalamalari ferqlidir.",
        "",
        f"Group 1 mean: {a.mean():.4f}",
        f"Group 2 mean: {b.mean():.4f}",
        f"Welch t-statistic: {result.statistic:.4f}",
        f"p-value: {p:.6g}",
        "",
        (
            "p < 0.05: H0 redd edilir."
            if p < 0.05
            else "p >= 0.05: H0 redd edilmir."
        ),
        "",
        "Qeyd: Bu netice exploratory xarakterlidir. "
        "Musteqillik, numune secimi ve uygun test "
        "sertleri ayrica yoxlanilmalidir."
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target")
    parser.add_argument("--group")
    args = parser.parse_args()

    PROCESSED.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    df = load_data()

    print("\nDATASET SHAPE")
    print(df.shape)

    print("\nDATA TYPES")
    print(df.dtypes)

    print("\nMISSING VALUES")
    print(df.isna().sum())

    print("\nDUPLICATES")
    print(df.duplicated().sum())

    numeric = df.select_dtypes(include=np.number)

    lines = [
        "# Exploratory Data Analysis Report",
        "",
        "## 1. Dataset overview",
        f"- Rows: {len(df)}",
        f"- Columns: {df.shape[1]}",
        f"- Duplicate rows: {df.duplicated().sum()}",
        "",
        "## 2. Column data types",
        df.dtypes.to_frame("dtype").to_markdown()
        if False else df.dtypes.to_string(),
        "",
        "## 3. Missing values",
        df.isna().sum().to_string(),
        "",
        "## 4. Descriptive statistics",
        numeric.describe().to_string()
        if not numeric.empty
        else "No numeric columns.",
        "",
        "## 5. Potential outliers (IQR method)"
    ]

    for col in numeric.columns:
        values = numeric[col].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = ((values < lower) | (values > upper)).sum()

        lines.append(
            f"- {col}: {outliers} potential outliers "
            f"({outliers / len(values):.2%})"
        )

    if numeric.shape[1] >= 2:
        lines.extend([
            "",
            "## 6. Correlation matrix",
            numeric.corr().to_string(),
            "",
            "Correlation is not evidence of causation."
        ])

    lines.extend(["", *statistical_test(df, args.target, args.group)])

    lines.extend([
        "",
        "## Further investigation",
        "- Examine missing-value mechanisms.",
        "- Investigate potential outliers before removing them.",
        "- Check whether duplicates are legitimate transactions.",
        "- Consider sampling bias and data leakage.",
        "- Interpret results in the dataset's business context."
    ])

    (REPORTS / "eda_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    df.to_csv(
        PROCESSED / "analysis_data.csv",
        index=False
    )

    print("\nEDA completed.")
    print("Report: reports/eda_report.md")


if __name__ == "__main__":
    main()

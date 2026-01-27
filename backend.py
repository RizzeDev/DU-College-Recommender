import pandas as pd
import re

TOTAL_CANDIDATES = 1550000
df = pd.read_csv("JEE.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")


# ---------------- FORCE NUMERIC CONVERSION ----------------
def to_number(series):
    return (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.extract(r"(\d+)", expand=False)
        .astype(float)
    )

# Try converting ALL columns to numeric where possible
numeric_scores = {}

for col in df.columns:
    converted = to_number(df[col])
    numeric_scores[col] = converted.notna().sum()
    df[col] = converted if converted.notna().sum() > 0 else df[col]

# Pick the column with MOST numeric values as closing rank
closing_col = max(numeric_scores, key=numeric_scores.get)

# Pick first two non-numeric columns as college & branch
text_cols = [c for c in df.columns if c != closing_col]

college_col = text_cols[0]
branch_col = text_cols[1] if len(text_cols) > 1 else text_cols[0]

college_data = df[[college_col, branch_col, closing_col]].dropna()
college_data.columns = ["college", "branch", "closing_rank"]

# ---------------- PERCENTILE ----------------
def predict_percentile_from_marks(marks):
    marks = max(0, min(300, marks))

    if marks <= 100:
        percentile = 85 * marks / 100
    elif marks <= 200:
        percentile = 85 + (marks - 100) * 0.14
    else:
        percentile = 99.5

    return round(percentile, 2)

def percentile_to_air(percentile):
    return int(((100 - percentile) / 100) * TOTAL_CANDIDATES) + 1

def percentile_and_air_2026(marks):
    p = predict_percentile_from_marks(marks)
    return p, percentile_to_air(p)

# ---------------- COLLEGE FILTER ----------------
def best_suited_by_air(user_air):
    eligible = college_data[college_data["closing_rank"] >= user_air]
    return eligible.sort_values("closing_rank").head(30)

def show_all_cutoffs():
    return college_data

# ---------------- TREND ----------------
def get_trend_data():
    return pd.DataFrame({
        "Year": list(range(2015, 2026)),
        "Cutoff_Percentile": [
            82.5, 84.2, 85.1, 86.8, 88.0,
            89.5, 90.2, 91.0, 92.3, 93.8, 94.6
        ]
    })

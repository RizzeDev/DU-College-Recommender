import pandas as pd

TOTAL_CANDIDATES = 1550000
df = pd.read_csv("JEE.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# ---- AUTO DETECT COLUMNS ----
text_cols = df.select_dtypes(include="object").columns.tolist()
num_cols = df.select_dtypes(include="number").columns.tolist()

if len(text_cols) < 2 or len(num_cols) < 1:
    raise ValueError("CSV must contain at least 2 text columns and 1 numeric column")

college_col = text_cols[0]
branch_col = text_cols[1]
closing_col = num_cols[0]

college_data = df[[college_col, branch_col, closing_col]].copy()
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

# ---------------- AIR ----------------
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

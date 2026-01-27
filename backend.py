import pandas as pd

TOTAL_CANDIDATES = 1550000

df = pd.read_csv("JEE.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("CSV COLUMNS:", df.columns.tolist())

# ---- AUTO COLUMN MAPPING ----
def find_column(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

college_col = find_column(['college', 'college_name', 'institute', 'institute_name'])
branch_col = find_column(['branch', 'course', 'program', 'branch_name'])
closing_col = find_column(['closing_rank', 'closing_rank_gen', 'cr', 'rank', 'closing'])

if not all([college_col, branch_col, closing_col]):
    raise ValueError(
        f"Required columns not found.\n"
        f"Found columns: {df.columns.tolist()}"
    )

college_data = df[[college_col, branch_col, closing_col]].copy()
college_data.columns = ['college', 'branch', 'closing_rank']

# ---------------- PERCENTILE ----------------
def predict_percentile_from_marks(marks):
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
    eligible = college_data[college_data['closing_rank'] >= user_air]
    return eligible.sort_values('closing_rank').head(30)

def show_all_cutoffs():
    return college_data

def get_trend_data():
    return pd.DataFrame({
        "Year": list(range(2015, 2026)),
        "Cutoff_Percentile": [
            82.5, 84.2, 85.1, 86.8, 88.0,
            89.5, 90.2, 91.0, 92.3, 93.8, 94.6
        ]
    })

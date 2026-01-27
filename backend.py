import pandas as pd

TOTAL_CANDIDATES = 1550000
df = pd.read_csv("JEE.csv")

long_df = df.melt(
    id_vars=["College"],
    var_name="Branch",
    value_name="Closing_Rank"
)

long_df = long_df.dropna()
long_df["Closing_Rank"] = long_df["Closing_Rank"].astype(int)

college_data = long_df.rename(columns={
    "College": "college",
    "Branch": "branch",
    "Closing_Rank": "closing_rank"
})

# ---------------- PERCENTILE PREDICTION ----------------
def predict_percentile_from_marks(marks):
    marks = max(0, min(300, marks))
    
    if marks >= 240:
        percentile = 99.95 + (marks-240)*0.01      # 240-280 -> 99.95-99.99+
    elif marks >= 210:
        percentile = 99.5 + (marks-210)*(0.4/30)  # 210-240 -> 99.5-99.9
    elif marks >= 180:
        percentile = 99 + (marks-180)*(0.5/30)    # 180-210 -> 99-99.5
    elif marks >= 160:
        percentile = 98 + (marks-160)*(1/20)      # 160-180 -> 98-99
    elif marks >= 140:
        percentile = 97 + (marks-140)*(1/20)      # 140-160 -> 97-98
    elif marks >= 120:
        percentile = 95 + (marks-120)*(2/20)      # 120-140 -> 95-97
    elif marks >= 100:
        percentile = 90 + (marks-100)*(5/20)      # 100-120 -> 90-95
    elif marks >= 70:
        percentile = 80 + (marks-70)*(10/30)      # 70-100 -> 80-90
    else:
        percentile = marks*80/70                   # 0-70 -> 0-80

    return round(min(percentile, 100), 2)

# ---------------- AIR CALCULATION ----------------
def percentile_to_air(percentile):
    """
    Converts percentile to All India Rank (AIR).
    """
    air = int(((100 - percentile) / 100) * TOTAL_CANDIDATES) + 1
    return air

def percentile_and_air_2026(marks):
    """
    Returns both percentile and AIR for given marks.
    """
    percentile = predict_percentile_from_marks(marks)
    air = percentile_to_air(percentile)
    return percentile, air

# ---------------- COLLEGE RECOMMENDATION ----------------
def best_suited_by_air(user_air):
    """
    Returns colleges where closing rank is >= user's AIR.
    """
    eligible = college_data[college_data["closing_rank"] >= user_air]
    return eligible.sort_values("closing_rank").head(30)

def show_all_cutoffs():
    """
    Shows all college-branch cutoffs.
    """
    return college_data

# ---------------- TREND DATA ----------------
def get_trend_data():
    """
    Returns past cutoff trend data for graph.
    """
    return pd.DataFrame({
        "Year": list(range(2015, 2026)),
        "Cutoff_Percentile": [
            82.5, 84.2, 85.1, 86.8, 88.0,
            89.5, 90.2, 91.0, 92.3, 93.8, 94.6
        ]
    })



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
    """
    Predicts percentile based on marks using a simple but slightly more realistic approximation.
    Easy to explain to Class 12 teachers.
    """
    marks = max(0, min(300, marks)) 

    if marks <= 100:
        percentile = 85 * marks / 100                # linear growth up to 100 marks
    elif marks <= 200:
        percentile = 85 + (marks - 100) * 0.145     # slightly steeper for 100-200 marks
    else:
        percentile = 99 + (marks - 200) * 0.01      # tiny growth after 200 marks

    return round(percentile, 2)

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

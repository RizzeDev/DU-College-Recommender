import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

TOTAL_CANDIDATES = 1550000

# ---------------- LOAD DATA ----------------
df = pd.read_csv("JEE.csv")

long_df = df.melt(
    id_vars=["College"],
    var_name="Branch",
    value_name="Closing_Rank"
)

long_df = long_df.dropna()
long_df["Closing_Rank"] = long_df["Closing_Rank"].astype(int)

# ---------------- PERCENTILE ESTIMATION ----------------
def predict_percentile_from_marks(marks):
    marks = max(0, min(300, marks))

    if marks >= 260:
        percentile = 99.7 + (marks - 240) * (0.3 / 60)
    elif marks >= 210:
        percentile = 99.5 + (marks - 210) * (0.2 / 30)
    elif marks >= 180:
        percentile = 99 + (marks - 180) * (0.5 / 30)
    elif marks >= 160:
        percentile = 98 + (marks - 160) * (1 / 20)
    elif marks >= 140:
        percentile = 97 + (marks - 140) * (1 / 20)
    elif marks >= 120:
        percentile = 95 + (marks - 120) * (2 / 20)
    elif marks >= 100:
        percentile = 90 + (marks - 100) * (5 / 20)
    elif marks >= 70:
        percentile = 80 + (marks - 70) * (10 / 30)
    else:
        percentile = (marks / 70) * 80

    return round(min(percentile, 99.99), 2)


# ---------------- AIR CALCULATION ----------------
def percentile_to_air(percentile):
    air = int(((100 - percentile) / 100) * TOTAL_CANDIDATES) + 1
    return air

def percentile_and_air_2026(marks):
    percentile = predict_percentile_from_marks(marks)
    air = percentile_to_air(percentile)
    return percentile, air

# ---------------- COLLEGE RECOMMENDATION ----------------
def best_suited_by_air(user_air):
    eligible = college_data[college_data["closing_rank"] >= user_air]
    return eligible.sort_values("closing_rank").head(30)

def show_all_cutoffs():
    return college_data

# ---------------- TREND DATA (2015–2025 ONLY) ----------------
def get_trend_data():
    return pd.DataFrame({
        "Year": list(range(2015, 2026)),
        "Cutoff_Percentile": [
            82.5, 84.2, 85.1, 86.8, 88.0,
            89.5, 90.2, 91.0, 92.3, 93.8, 94.6
        ]
    })

# ---------------- LINEAR REGRESSION (AI) ----------------
def predict_cutoff_2026():
    years = np.array([
        2015, 2016, 2017, 2018, 2019,
        2020, 2021, 2022, 2023, 2024, 2025
    ]).reshape(-1, 1)

    cutoffs = np.array([
        82.5, 84.2, 85.1, 86.8, 88.0,
        89.5, 90.2, 91.0, 92.3, 93.8, 94.6
    ])

    model = LinearRegression()
    model.fit(years, cutoffs)

    predicted_2026 = model.predict([[2026]])[0]
    return round(predicted_2026, 2)





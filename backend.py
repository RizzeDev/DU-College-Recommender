import pandas as pd

# ---------------- DATA ----------------
TOTAL_CANDIDATES = 1550000
df = pd.read_csv("JEE.csv")

college_data = df[['College', 'Branch', 'Closing_Rank']]

# ---------------- PERCENTILE PREDICTION ----------------
def predict_percentile_from_marks(marks):
    marks = max(0, min(300, marks))

    if marks <= 100:
        percentile = 85 * marks / 100
    elif marks <= 120:
        percentile = 85 + (marks - 100) * (95 - 85) / 20
    elif marks <= 130:
        percentile = 95 + (marks - 120) * (96 - 95) / 10
    elif marks <= 150:
        percentile = 96 + (marks - 130) * (97 - 96) / 20
    elif marks <= 180:
        percentile = 97 + (marks - 150) * (98 - 97) / 30
    elif marks <= 200:
        percentile = 98 + (marks - 180) * (99 - 98) / 20
    else:
        percentile = 99 + (marks - 200) * (99.99 - 99) / 100

    return round(min(percentile, 99.99), 2)

# ---------------- AIR CALCULATION ----------------
def percentile_to_air(percentile):
    air = int(((100 - percentile) / 100) * TOTAL_CANDIDATES) + 1
    return air

# ---------------- MAIN FUNCTION ----------------
def percentile_and_air_2026(marks, total_candidates):
    percentile = predict_percentile_from_marks(marks)
    air = percentile_to_air(percentile)
    return percentile, air

# ---------------- COLLEGE RECOMMENDATION ----------------
def best_suited_by_air(user_air):
    eligible = college_data[college_data['Closing_Rank'] >= user_air]
    return eligible.sort_values(by='Closing_Rank').head(30)

def show_all_cutoffs():
    return college_data

# ---------------- TREND DATA (FOR GRAPH) ----------------
def get_trend_data():
    data = {
        "Year": list(range(2015, 2026)),
        "Cutoff_Percentile": [
            82.5, 84.2, 85.1, 86.8, 88.0,
            89.5, 90.2, 91.0, 92.3, 93.8, 94.6
        ]
    }
    return pd.DataFrame(data)

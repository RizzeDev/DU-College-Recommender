import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

TOTAL_CANDIDATES = 1475000  # JEE 2025 approx

def rank_to_percentile(rank):
    if pd.isna(rank) or rank <= 0:
        return 0.0
    return round(100 - (rank / TOTAL_CANDIDATES * 100), 2)

df = pd.read_csv("JEE.csv")

df['Cutoff_2025'] = df['Closing_Rank'].apply(rank_to_percentile)

college_data = df[['College', 'Branch', 'Cutoff_2025']]

def best_suited(percentile):
    lower = college_data[college_data['Cutoff_2025'] < percentile].copy()
    lower['diff'] = percentile - lower['Cutoff_2025']
    return lower.sort_values(by='diff').head(30).drop(columns=['diff'])

def show_all_cutoffs():
    return college_data

def get_trend_data():
    data = {
        "Year": list(range(2015, 2026)),
        "Cutoff_Percentile": [82.5, 84.2, 85.1, 86.8, 88.0, 89.5, 90.2, 91.0, 92.3, 93.8, 94.6]
    }
    return pd.DataFrame(data)


trend_df = get_trend_data()

X = trend_df[['Year']]
y = trend_df['Cutoff_Percentile']
model = LinearRegression()
model.fit(X, y)

def predict_2026():
    return round(float(model.predict([[2026]])), 2)

def best_suited_2026(user_percentile):
    predicted = predict_2026()
    recommended = best_suited(user_percentile)
    return predicted, recommended

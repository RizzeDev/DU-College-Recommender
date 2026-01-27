import streamlit as st
import backend as bk
import altair as alt

st.set_page_config(page_title="Delhi College Rec System", layout="wide")

st.title("Delhi College Recommendation System 🏫🧑🏻‍🎓")
st.write("Suggests colleges based on your JEE percentile.")

TOTAL_CANDIDATES_2026 = 1550000

tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "Percentile Predictor",
    "Best Matches",
    "All Colleges",
    "Cutoff Trend",
    "AI Prediction 2026"
])

# ---------------- TAB 0 ----------------
with tab0:
    st.header("JEE Main Percentile & AIR Predictor (2026)")

    # Number input for marks
    marks = st.number_input(
        "Enter your JEE Marks out of 300", 0, 300, 0,
        help="Enter your expected or obtained marks in JEE Main."
    )

    if st.button("Predict Result"):
        percentile, air = bk.percentile_and_air_2026(marks)

        col1, col2 = st.columns(2)
        col1.metric("Predicted Percentile", f"{percentile} %")
        col2.metric("Estimated AIR", air)

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("Best Matches for Your Percentile")

    percentile = st.slider(
        "Select Your JEE Percentile",
        90.0, 100.0, 90.0, 0.5,
        help="Adjust to see colleges you may get based on your percentile."
    )

    user_air = int(((100 - percentile) / 100) * TOTAL_CANDIDATES_2026) + 1

    result = bk.best_suited_by_air(user_air)
    st.dataframe(result.reset_index(drop=True), use_container_width=True)

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("All Colleges Cutoffs")
    st.dataframe(bk.show_all_cutoffs(), use_container_width=True)

# ---------------- TAB 3 ----------------
with tab3:
    st.subheader("JEE Mains Cutoff Trend (2015–2025)")
    trend = bk.get_trend_data()

    chart = (
        alt.Chart(trend)
        .mark_line(point=True)
        .encode(
            x="Year:O",
            y=alt.Y("Cutoff_Percentile:Q", scale=alt.Scale(domain=[80, 100])),
            tooltip=["Year", "Cutoff_Percentile"]
        )
    )

    st.altair_chart(chart, use_container_width=True)

# ---------------- TAB 4 ----------------
with tab4:
    st.subheader("AI Prediction for JEE 2026")
    st.info("Predicted cutoff will be around **94–95 percentile** based on past trends.")


# ----------------- FOOTER -------------------
st.markdown("Project by Class 12 Students. Subject: Artificial Intelligence (843)")

st.sidebar.title("Project Info")
st.sidebar.markdown("""
**Team Members**
- Ritesh Pathak  
- Eshan Awasthi  
- Pratyush Singh  
- Aditi Mishra  
- Ryan Naqvi  

**School:** AMITY INTERNATIONAL SCHOOL, MAYUR VIHAR, DELHI
""")


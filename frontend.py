import streamlit as st
import backend as bk
import altair as alt

st.set_page_config(page_title="Delhi College Rec System", layout="wide")

st.title("Delhi College Recommendation System 🏫🧑🏻‍🎓")
st.write("Suggests colleges based on your JEE percentile.")


tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "Percentile Predictor",
    "Best Matches",
    "All Colleges",
    "Cutoff Trend",
    "AI Prediction 2026"
])

# ----------------- TAB 0 -------------------
with tab0:
    st.header("JEE Main Percentile & AIR Predictor (2026)")

    st.write("Enter your expected JEE Main marks to get an idea of your percentile and rank.")

    marks = st.number_input(
        "Marks out of 300",
        min_value=0,
        max_value=300,
        value=0
    )

    TOTAL_CANDIDATES_2026 = 1550000

    if st.button("Predict Result"):
        percentile, air = bk.percentile_and_air_2026(
            marks,
            TOTAL_CANDIDATES_2026
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Predicted Percentile")
            st.write(f"{percentile} %")
            st.caption(
                "Percentile is predicted using historical JEE marks vs percentile trends "
                "with piecewise linear interpolation for 2026."
            )

        with col2:
            st.subheader("Estimated AIR")
            st.write(f"{air}")

        st.write(
            "Note: This is only an estimate based on historical trends. "
            "Actual JEE results may vary depending on shift difficulty."
        )

# ----------------- TAB 1 -------------------
with tab1:
    percentile = st.slider("Select Your JEE Percentile", 85, 100, 90)
    st.subheader("Best Matches for Your Percentile")
    result = bk.best_suited(percentile)
    st.dataframe(result.reset_index(drop=True), use_container_width=True)

# ----------------- TAB 2 -------------------
with tab2:
    st.subheader("All Colleges Cutoffs")
    st.dataframe(bk.show_all_cutoffs(), use_container_width=True)

# ----------------- TAB 3 -------------------
with tab3:
    st.subheader("JEE Mains Cutoff Trend for JEE Advance (2015–2025)")
    trend = bk.get_trend_data()

    chart = (
        alt.Chart(trend)
        .mark_line(point=True)
        .encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y(
                "Cutoff_Percentile:Q",
                title="Percentile (80–100)",
                scale=alt.Scale(domain=[80, 100])
            ),
            tooltip=["Year", "Cutoff_Percentile"]
        )
        .properties(width=700, height=400, title="Cutoff Trend")
    )
    st.altair_chart(chart, use_container_width=False)

# ----------------- TAB 4 -------------------
with tab4:
    st.subheader("AI Prediction for JEE 2026 Cutoff")

    predicted = bk.predict_2026()
    st.info(f"Predicted Cutoff Percentile for 2026: **{predicted}%**")

# ----------------- Footer ------------------- 
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




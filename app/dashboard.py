"""
AI Trading Scanner Dashboard

Displays scanner results by trading profile.
"""

import streamlit as st
import pandas as pd
from scanner_runner import run_scanner
from profile_manager import (
    set_active_profile,
    get_active_profile_name
)

from results_manager import (
    load_results,
    get_available_results
)

from chart import create_candlestick_chart
from providers.yahoo import get_history

# -----------------------------
# Page setup
# -----------------------------

st.set_page_config(
    page_title="AI Trading Scanner",
    layout="wide"
)


st.title("🔥 AI Trading Scanner Dashboard")


# -----------------------------
# Profile selector
# -----------------------------

profiles = get_available_results()


if not profiles:

    st.warning(
        "No scanner results found. Run scanner first."
    )

    st.stop()


profiles = [
    "scalp",
    "premarket_scalp",
    "breakout",
    "swing",
    "quality"
]

current_profile = get_active_profile_name()

selected_profile = st.selectbox(
    "Trading Profile",
    profiles,
    index=profiles.index(current_profile)
)

if st.button("🚀 Run Scanner"):

    set_active_profile(selected_profile)

    with st.spinner("Running scanner..."):
        run_scanner()

    st.success("Scanner completed!")

    st.rerun()

# -----------------------------
# Load results

# -----------------------------

df = load_results(
    selected_profile
)


if df.empty:

    st.warning(
        "No results available"
    )

    st.stop()



# -----------------------------
# Summary
# -----------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Profile",
        selected_profile.upper()
    )


with col2:

    st.metric(
        "Stocks Found",
        len(df)
    )


with col3:

    if "Rank_Score" in df.columns:

        st.metric(
            "Best Score",
            df["Rank_Score"].max()
        )



# -----------------------------
# Main table
# -----------------------------

st.subheader(
    "Top Candidates"
)


columns = [
    "Symbol",
    "Price",
    "Signal",
    "Rank_Score",
    "RSI",
    "RVOL",
    "Entry",
    "Stop_Loss",
    "Target_1",
    "Target_2"
]


available_columns = [
    c for c in columns
    if c in df.columns
]


display_df = df[available_columns].copy()

display_df.insert(
    0,
    "Rank",
    range(1, len(display_df) + 1)
)

styled_df = (
    display_df.style
    .set_properties(**{
        "text-align": "center"
    })
    .set_table_styles([
        {
            "selector": "th",
            "props": [("text-align", "center")]
        }
    ])
)

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True
)


# -----------------------------
# Stock details
# -----------------------------

st.subheader(
    "Stock Details"
)


symbol = st.selectbox(
    "Select Symbol",
    df["Symbol"].tolist()
)


stock = df[
    df["Symbol"] == symbol
].iloc[0]


for column in [
    "Price",
    "Signal",
    "Rank_Score",
    "RSI",
    "RVOL",
    "Entry",
    "Stop_Loss",
    "Target_1",
    "Target_2",
    "Score_Breakdown"
]:

    if column in stock:

        st.write(
            f"**{column}:**",
            stock[column]
        )

# -----------------------------
# Chart
# -----------------------------

st.subheader(
    "📈 Technical Chart"
)


history = get_history(symbol)


if history is not None:

    chart = create_candlestick_chart(
        history,
        symbol,
        stock
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

else:

    st.warning(
        "No chart data available"
    )

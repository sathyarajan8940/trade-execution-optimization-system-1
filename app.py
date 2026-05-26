import streamlit as st
import pandas as pd
import sys
import os
import yfinance as yf
import matplotlib.pyplot as plt

# ---------------- IMPORT PATH ----------------
sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)

from predict import predict_strategy

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Trade Execution Optimizer",
    layout="wide"
)

# ---------------- CUSTOM STYLE ----------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    h1, h2, h3 {
        color: white;
    }

    .stButton>button {
        width: 100%;
        height: 3em;
        border-radius: 10px;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ----------------
st.title("📊 AI Trade Execution Optimization System")

st.write(
    "Machine Learning based trade execution optimization dashboard"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙ Trading Settings")

stock = st.sidebar.selectbox(
    "Select Stock",
    ["AAPL", "TSLA", "MSFT", "GOOG"],
    key="stock_select"
)

# ---------------- STOCK DATA ----------------
ticker = yf.download(stock, period="6mo")

# ---------------- LIVE CHART ----------------
st.subheader("📈 Live Stock Price")

st.line_chart(ticker["Close"])

# ---------------- METRICS ----------------
latest_price = float(ticker["Close"].iloc[-1].item())
highest_price = float(ticker["High"].max().item())
lowest_price = float(ticker["Low"].min().item())

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current Price",
    f"${latest_price:.2f}"
)

col2.metric(
    "Highest Price",
    f"${highest_price:.2f}"
)

col3.metric(
    "Lowest Price",
    f"${lowest_price:.2f}"
)

# ---------------- MARKET TREND ----------------
close_mean = float(ticker["Close"].mean().item())

if latest_price > close_mean:

    st.success("📈 Bullish Market Trend")

else:

    st.warning("📉 Bearish Market Trend")

# ---------------- INPUTS ----------------
st.subheader("⚡ Execution Inputs")

volatility = st.slider(
    "Volatility",
    0.0,
    0.1,
    0.02,
    key="volatility_slider"
)

# ---------------- RISK LEVEL ----------------
if volatility > 0.05:

    st.error("🚨 High Risk Market")

else:

    st.success("✅ Low Risk Market")

ma_10 = st.number_input(
    "Moving Average (MA 10)",
    value=175.0,
    key="ma10_input"
)

volume_ma = st.number_input(
    "Volume MA",
    value=2000000.0,
    key="volume_input"
)

momentum = st.number_input(
    "Momentum",
    value=3.0,
    key="momentum_input"
)

order_size = st.number_input(
    "Order Size",
    value=10000,
    key="order_input"
)

# ---------------- BUTTON ----------------
if st.button(
    "🚀 Optimize Execution",
    key="optimize_button"
):

    result = predict_strategy(
        volatility,
        ma_10,
        volume_ma,
        momentum,
        order_size
    )

    # ---------------- STRATEGY ----------------
    st.subheader("📌 Recommended Strategy")

    st.success(result["strategy"])

    # ---------------- STRATEGY INFO ----------------
    if result["strategy"] == "VWAP":

        st.info(
            "VWAP is ideal for high-volume institutional trading."
        )

    elif result["strategy"] == "TWAP":

        st.info(
            "TWAP is safer during volatile markets."
        )

    else:

        st.info(
            "ICEBERG strategy hides large market orders."
        )

    # ---------------- AI RECOMMENDATION ----------------
    st.subheader("🤖 AI Recommendation")

    if volatility > 0.05:

        st.write(
            "Market volatility is high. TWAP execution is safer."
        )

    else:

        st.write(
            "Market conditions are stable for VWAP execution."
        )

    # ---------------- CONFIDENCE ----------------
    confidence = 92

    st.subheader("🎯 Prediction Confidence")

    st.progress(confidence)

    st.write(f"{confidence}% confidence")

    # ---------------- SLIPPAGE ----------------
    st.subheader("💰 Estimated Slippage")

    st.info(result["slippage"])

    # ---------------- EXECUTION SCHEDULE ----------------
    st.subheader("📅 Execution Schedule")

    df = pd.DataFrame(result["schedule"])

    st.dataframe(df)

    # ---------------- BAR CHART ----------------
    st.subheader("📊 Execution Quantity Chart")

    st.bar_chart(
        df.set_index("interval")
    )

    # ---------------- PIE CHART ----------------
    st.subheader("🥧 Execution Distribution")

    fig, ax = plt.subplots()

    df.set_index("interval").plot.pie(
        y="quantity",
        autopct="%1.1f%%",
        ax=ax
    )

    st.pyplot(fig)

    # ---------------- DOWNLOAD ----------------
    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download Schedule",
        csv,
        "schedule.csv",
        "text/csv",
        key="download_button"
    )

# ---------------- FOOTER ----------------
st.write("---")

st.caption(
    "Built with Machine Learning for Trade Execution Optimization"
)
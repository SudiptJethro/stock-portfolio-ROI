# stock_roi_app.py
import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

st.title("📈 Stock Portfolio ROI Calculator")

amount_invested = st.number_input("Enter the total Invested amount in $USD:", min_value=0.0)

tickers = []
weights = []

st.write("### Enter 5 stock tickers and their weights (e.g., 0.2 for 20%)")

for i in range(5):
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input(f"Stock {i+1} Ticker", key=f"ticker_{i}").upper()
    with col2:
        weight = st.number_input(f"Weight for Stock {i+1}", key=f"weight_{i}", min_value=0.0, max_value=1.0)
    
    tickers.append(ticker)
    weights.append(weight)

start_date = st.date_input("Start date", value=datetime(2023, 1, 1))
end_date = datetime.today().strftime('%Y-%m-%d')

if st.button("Calculate"):
    if len(set(tickers)) != 5 or abs(sum(weights) - 1.0) > 0.01:
        st.error("Please ensure 5 unique tickers and that weights sum to 1.0")
    else:
        try:
            data = yf.download(tickers, start=start_date, end=end_date,auto_adjust=False)['Adj Close'].dropna()
            normalized_prices = data / data.iloc[0]
            allocated = normalized_prices * weights * amount_invested
            portfolio_value = allocated.sum(axis=1)

            initial_value = portfolio_value.iloc[0]
            final_value = portfolio_value.iloc[-1]
            roi = ((final_value - initial_value) / initial_value) * 100
            profit = final_value - initial_value

            st.success(f"Initial Investment: ${initial_value:,.2f}")
            st.success(f"Final Portfolio Value: ${final_value:,.2f}")
            st.success(f"Total Return (Profit): ${profit:,.2f}")
            st.success(f"ROI: {roi:.2f}%")

            st.write("### 📊 Portfolio Performance Chart")
            fig, ax = plt.subplots(figsize=(12, 6))
            for ticker in tickers:
                ax.plot(normalized_prices[ticker], label=ticker)
            ax.plot(portfolio_value / initial_value, label='Portfolio', linewidth=2, color='black', linestyle='--')
            ax.set_title('Stock Prices and Portfolio Value Over Time')
            ax.set_xlabel('Date')
            ax.set_ylabel('Normalized Value')
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"\"Something went wrong: {e}\"" )

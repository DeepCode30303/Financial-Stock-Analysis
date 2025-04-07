import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import scipy.optimize as sco

def show_risk_analysis_page(ticker_list):
    st.header("Risk Analysis")

    # Ticker Selection Bar: Use ticker names as in Portfolio, then convert to symbols
    risk_ticker_names = st.multiselect(
        "Select tickers for risk analysis",
        options=ticker_list['symbol_name'].tolist(),
        default=st.session_state.selected_tickers,
        help="You can add more tickers here for risk analysis."
    )
    if not risk_ticker_names:
        st.warning("Please select at least one ticker for risk analysis.")
        return
    
    # Convert selected ticker names into their symbols
    risk_tickers = ticker_list[ticker_list['symbol_name'].isin(risk_ticker_names)]['symbol'].tolist()

    # Retrieve date range from session state
    start_date = st.session_state.sel_dtl
    end_date = st.session_state.sel_dt2

    # Download risk tickers data
    try:
        risk_data = yf.download(risk_tickers, start=start_date, end=end_date)['Close']
        # Convert to long format for easier manipulation
        risk_data = risk_data.reset_index().melt(id_vars='Date', var_name='ticker', value_name='price')
        # Sort data and calculate daily returns
        risk_data.sort_values(['ticker', 'Date'], inplace=True)
        risk_data['price pct daily'] = risk_data.groupby('ticker')['price'].pct_change()
    except Exception as e:
        st.error(f"Error downloading data for risk tickers: {e}")
        return

    # Download benchmark data (S&P 500)
    try:
        benchmark_data = yf.download('^GSPC', start=start_date, end=end_date)['Close'].reset_index()
        benchmark_data.columns = ['Date', 'Close']
        benchmark_returns = benchmark_data.set_index('Date')['Close'].pct_change().dropna()
    except Exception as e:
        st.error(f"Error downloading S&P 500 data: {e}")
        return

    # Pivot risk data to have tickers as columns and Date as index
    risk_pivot = risk_data.pivot_table(index='Date', columns='ticker', values='price pct daily').dropna()
    if risk_pivot.empty:
        st.warning("No data available for the selected tickers and date range.")
        return

    # ------------------- Minimum Variance Portfolio Optimization -------------------
    def min_variance_weights(cov_matrix):
        n = cov_matrix.shape[0]
        def objective(w, cov_matrix):
            return w.T @ cov_matrix @ w
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
        bounds = tuple((0, 1) for _ in range(n))
        initial_guess = np.repeat(1/n, n)
        result = sco.minimize(objective, initial_guess, args=(cov_matrix,), method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x

    # Calculate the covariance matrix and optimal weights
    cov_matrix = risk_pivot.cov()
    optimal_weights = min_variance_weights(cov_matrix)
    optimal_weights_series = pd.Series(optimal_weights, index=cov_matrix.columns)

    # ------------------- Risk Metrics -------------------
    # 1. Individual ticker risk (annualized standard deviation in %)
    ticker_risks = (risk_pivot.std() * np.sqrt(252) * 100).round(2)
    # 2. Cumulative portfolio risk computed from the weighted portfolio returns using optimal weights
    weighted_returns = risk_pivot.multiply(optimal_weights_series, axis=1).sum(axis=1)
    cumulative_risk = (weighted_returns.std() * np.sqrt(252) * 100).round(2)
    # 3. Benchmark risk (annualized, in %)
    benchmark_risk = (benchmark_returns.std() * np.sqrt(252) * 100).round(2)

    st.subheader("Risk Metrics")
    st.write("Individual Ticker Risks (Annualized Standard Deviation in %):")
    st.write(ticker_risks)
    st.write("Cumulative Portfolio Risk (Optimal Weights, Annualized %):", cumulative_risk)
    st.write("Benchmark (S&P 500) Risk (Annualized %):", benchmark_risk)

    # ---------------- Performance Comparison ----------------
    st.subheader("Performance Comparison")
    # Cumulative returns for the optimal portfolio
    weighted_portfolio_returns = (weighted_returns + 1).cumprod() - 1
    portfolio_cumulative = pd.DataFrame({
        'Date': weighted_portfolio_returns.index, 
        'Optimal Portfolio': weighted_portfolio_returns.values
    })

    # Cumulative returns for benchmark
    benchmark_cumulative = (benchmark_returns + 1).cumprod() - 1
    benchmark_cumulative = benchmark_cumulative.reset_index()
    benchmark_cumulative.columns = ['Date', 'Benchmark']

    # Merge and plot
    combined_returns = pd.merge(portfolio_cumulative, benchmark_cumulative, on='Date', how='outer')
    combined_returns = combined_returns.melt(id_vars='Date', var_name='Asset', value_name='Cumulative Return')
    fig = px.line(combined_returns, x='Date', y='Cumulative Return', color='Asset',
                  title='Cumulative Performance: Optimal Portfolio vs. Benchmark')
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Portfolio Composition Pie Chart ----------------
    st.subheader("Portfolio Composition")
    # Use the latest available price to calculate composition weights
    latest_date = risk_data['Date'].max()
    latest_prices = risk_data[risk_data['Date'] == latest_date].groupby('ticker')['price'].last()
    total_value = latest_prices.sum()
    composition_df = pd.DataFrame({
        'Ticker': latest_prices.index,
        'Allocation (%)': ((latest_prices / total_value) * 100).round(2)
    })
    fig_pie = px.pie(composition_df, values='Allocation (%)', names='Ticker',
                     title='Suggested Investment Allocation (Based on Latest Prices)',
                     hover_data={'Allocation (%)':':.2f'})
    fig_pie.update_traces(textposition='inside', textinfo='percent+label', hovertemplate='%{label}: %{value:.2f}%')
    st.plotly_chart(fig_pie, use_container_width=True)
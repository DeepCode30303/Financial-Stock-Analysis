import streamlit as st
import yfinance as yf
import plotly.express as px
import numpy as np
from datetime import date, datetime
from stocknews import StockNews

def show_stock_details_page():
    st.title('Stock Dashboard')

    # Get parameters from session state
    ticker = st.session_state.ticker_details
    start_date_str = st.session_state.sel_dtl.strftime('%Y-%m-%d')
    end_date_str = st.session_state.sel_dt2.strftime('%Y-%m-%d')

    # Convert string dates to date objects
    try:
        startdate = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        enddate = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        st.error("Invalid date format in parameters")
        startdate = date(2020, 1, 1)
        enddate = date.today()

    # Show the parameters received
    st.sidebar.markdown("## Parameters Received")
    st.sidebar.write(f"Ticker: {ticker}")
    st.sidebar.write(f"Start Date: {startdate}")
    st.sidebar.write(f"End Date: {enddate}")

    # Allow changing parameters in the sidebar
    with st.sidebar:
        with st.form("input_form"):
            new_ticker = st.text_input('Enter Ticker', ticker, key="ticker_input")
            new_startdate = st.date_input('Start Date', value=startdate, key="start_date_input")
            new_enddate = st.date_input('End Date', value=enddate, key="end_date_input")
            submitted = st.form_submit_button("Apply")

    # Use new parameters if form was submitted
    if submitted:
        ticker = new_ticker
        startdate = new_startdate
        enddate = new_enddate

    # --- Input Validation ---
    if not ticker:
        st.error("Please enter a ticker symbol.")
        st.stop()

    if (enddate - startdate).days < 2:
        st.error("Please select a date range with at least 2 days difference.")
        st.stop()

    if enddate > date.today():
        st.error("End Date cannot be in the future.")
        st.stop()

    # --- Download Data with Error Handling ---
    try:
        data = yf.download(ticker, start=startdate.strftime("%Y-%m-%d"),
                           end=enddate.strftime("%Y-%m-%d"))
    except Exception as e:
        st.error(f"Error downloading data for {ticker}: {e}")
        st.stop()

    if data.empty:
        st.error("No data found. Please check the ticker symbol and date range.")
        st.stop()

    # --- Plotting Stock Prices ---
    try:
        fig = px.line(data, x=data.index, y=data['Close'].squeeze(),
                     title=f"{ticker} Price Chart")
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error plotting data: {e}")

    # Create tabs
    pricingdata, fundamentaldata, news_tab = st.tabs(['Pricing Data', 'Fundamental Data', 'News'])

    # ---------------- Pricing Data Tab ----------------
    with pricingdata:
        st.header('Price Movements')
        data2 = data.copy()
        data2['% Change'] = data2['Close'].pct_change()
        data2.dropna(inplace=True)
        st.write(data2)

        annual_returns = data2['% Change'].mean() * 252 * 100
        st.write('Annual Returns:', f"{annual_returns:.2f} %")

        stdev = np.std(data2['% Change']) * np.sqrt(252)
        st.write('Standard Deviation:', f"{stdev * 100:.2f} %")

        risk_adjusted = annual_returns / (stdev * 100) if stdev != 0 else 0
        st.write('Risk Adjusted Returns:', f"{risk_adjusted:.2f} %")

    # ---------------- Fundamental Data Tab ----------------
    with fundamentaldata:
        st.subheader('Balance Sheet')
        ticker_obj = yf.Ticker(ticker)
        bs = ticker_obj.balance_sheet
        if bs is not None and not bs.empty:
            st.write(bs)
        else:
            st.write("No balance sheet data available.")

        st.subheader('Income Statement')
        inc_stmt = ticker_obj.financials
        if inc_stmt is not None and not inc_stmt.empty:
            st.write(inc_stmt)
        else:
            st.write("No income statement data available.")

        st.subheader('Cash Flow Statement')
        cf = ticker_obj.cashflow
        if cf is not None and not cf.empty:
            st.write(cf)
        else:
            st.write("No cash flow data available.")

    # ---------------- News Tab ----------------
    with news_tab:
        st.header(f'News for {ticker}')
        try:
            sn = StockNews(ticker, save_news=False)
            df_news = sn.read_rss()

            if not df_news.empty:
                for i, row in df_news.head(10).iterrows():
                    st.subheader(f'News {i+1}')
                    st.write("Published:", row['published'])
                    st.write("Title:", row['title'])
                    st.write("Summary:", row['summary'])
                    st.write(f"Title Sentiment: {row['sentiment_title']}")
                    st.write(f"News Sentiment: {row['sentiment_summary']}")
            else:
                st.write("No news available for this ticker.")
        except Exception as e:
            st.error(f"Error fetching news: {e}")
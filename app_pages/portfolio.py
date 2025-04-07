import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import datetime as dt

def show_portfolio_page(ticker_list):
    with st.sidebar:
        sel_tickers = st.multiselect('Portfolio Builder', placeholder="Search tickers", 
                                     options=ticker_list.symbol_name, 
                                     default=st.session_state.selected_tickers)
        sel_tickers_list = ticker_list[ticker_list.symbol_name.isin(sel_tickers)].symbol

        cols = st.columns(4)
        for i, ticker in enumerate(sel_tickers_list):
            try:
                cols[i % 4].image('https://logo.clearbit.com/' + yf.Ticker(ticker).info['website'].replace('https://.', ''), width=65)
            except:
                cols[i % 4].subheader(ticker)

        cols = st.columns(2)
        sel_dtl = cols[0].date_input('Start Date', value=st.session_state.sel_dtl, format='YYYY-MM-DD')
        sel_dt2 = cols[1].date_input('End Date', value=st.session_state.sel_dt2, format='YYYY-MM-DD')

        if len(sel_tickers) != 0:
            yfdata = yf.download(list(sel_tickers_list), start=sel_dtl, end=sel_dt2)['Close'].reset_index().melt(
                id_vars=['Date'], var_name='ticker', value_name='price')
            yfdata['price_start'] = yfdata.groupby('ticker').price.transform('first')
            yfdata['price pct daily'] = yfdata.groupby('ticker').price.pct_change()
            yfdata['price_pct'] = (yfdata.price - yfdata.price_start) / yfdata.price_start
            st.session_state.yfdata = yfdata
        else:
            yfdata = pd.DataFrame()

        st.sidebar.button("Update Data", key="update_data_button")

        # Update session state
        st.session_state.selected_tickers = sel_tickers
        st.session_state.sel_dtl = sel_dtl
        st.session_state.sel_dt2 = sel_dt2

    # Main content area
    if len(sel_tickers) == 0:
        st.info('Select ticker to view points')
    else:
        st.subheader('All Stocks')
        if not yfdata.empty:
            fig = px.line(yfdata, x='Date', y='price_pct', color='ticker', markers=True)
            fig.add_hline(y=0, line_dash='dash', line_color='white')
            fig.update_layout(xaxis_title=None, yaxis_title=None)
            fig.update_yaxes(tickformat=',.0%')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No tickers selected or no data available.")

        st.subheader('Individual Stocks')
        cols = st.columns(3)
        for i, ticker in enumerate(sel_tickers_list):
            try:
                cols[i % 3].image('https://logo.clearbit.com/' + yf.Ticker(ticker).info['website'].replace('https://.', ''), width=65)
            except:
                cols[i % 3].subheader(ticker)

            cols2 = cols[i % 3].columns(3)
            cols2[0].metric(label='50-Day Average', value=round(yfdata[yfdata.ticker == ticker].price.tail(50).mean(), 2))
            cols2[1].metric(label='1 year Low', value=round(yfdata[yfdata.ticker == ticker].price.tail(365).mean(), 2))
            cols2[2].metric(label='1 year High', value=round(yfdata[yfdata.ticker == ticker].price.tail(365).max(), 2))

            # Pass current dates
            if cols[i % 3].button(f"Details for {ticker}", key=f"details_{ticker}_{i}"):
                params = {
                    'ticker': ticker,
                    'start_date': sel_dtl.strftime("%Y-%m-%d"),
                    'end_date': sel_dt2.strftime("%Y-%m-%d")
                }
                st.query_params = params
                st.session_state.selected_menu = "Stock Details"
                st.session_state.ticker_details = ticker
                st.rerun()

            fig = px.line(yfdata[yfdata.ticker == ticker], x='Date', y='price_pct', markers=True)
            fig.update_layout(xaxis_title=None, yaxis_title=None)
            cols[i % 3].plotly_chart(fig, use_container_width=True)
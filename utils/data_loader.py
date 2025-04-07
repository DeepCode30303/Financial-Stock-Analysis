import pandas as pd
import streamlit as st
import financedatabase as fd
from urllib.parse import urlencode

# Load ticker list data
@st.cache_data
def load_data():
    ticker_list = pd.concat([fd.ETFs().select().reset_index()[['symbol', 'name']],
                            fd.Equities().select().reset_index()[['symbol', 'name']]])
    ticker_list = ticker_list[ticker_list.symbol.notna()]
    ticker_list['symbol_name'] = ticker_list['symbol'] + ' - ' + ticker_list['name']
    return ticker_list

# Function to create query parameters for navigation
def create_query_params(ticker, start_date, end_date):
    params = {
        'ticker': ticker,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d")
    }
    return f"?{urlencode(params)}"
import sys
import os
sys.path.append(os.path.abspath('.'))

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import datetime as dt

# Import modules
from auth.login import is_user_authenticated, show_login_page, show_signup_page
from utils.data_loader import load_data
from app_pages.portfolio import show_portfolio_page
from app_pages.stock_details import show_stock_details_page
from app_pages.calculator import show_calculator_page
from app_pages.risk_analysis import show_risk_analysis_page


# App config
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Load ticker data
ticker_list = load_data()

def main():
    if 'show_login' not in st.session_state:
        st.session_state.show_login = True  # set default to login

    if not is_user_authenticated():
        if st.session_state.show_login:
            show_login_page()
        else:
            show_signup_page()
    else:
        st.title('Portfolio Analysis')
        # --- Navigation Menu ---
        menu_options = ["Portfolio", "Stock Details", "Calculator", "Risk Analysis"]
        selected = option_menu(
            menu_title="Navigate",
            options=menu_options,
            icons=["house", "info-circle", "calculator", "fa-solid fa-chart-line"],
            orientation="horizontal",
            key="main_menu"
        )

        # Add a logout button
        if st.button("Logout", key="logout_button"):
            st.session_state.authenticated = False
            st.session_state.show_login = True  # Reset show_login state, go to login
            st.rerun()

        # Initialize session state
        if 'selected_tickers' not in st.session_state:
            st.session_state.selected_tickers = []
        if 'sel_dtl' not in st.session_state:
            st.session_state.sel_dtl = dt.datetime(2024, 1, 1).date()
        if 'sel_dt2' not in st.session_state:
            st.session_state.sel_dt2 = dt.date.today()
        if 'yfdata' not in st.session_state:
            st.session_state.yfdata = pd.DataFrame()
        if 'selected_menu' not in st.session_state:
            st.session_state.selected_menu = "Portfolio"
        if 'ticker_details' not in st.session_state:
            st.session_state.ticker_details = ""

        # Show selected page
        if selected == "Portfolio":
            show_portfolio_page(ticker_list)
        elif selected == "Calculator":
            show_calculator_page(ticker_list)
        elif selected == "Stock Details":
            show_stock_details_page()
        elif selected == "Risk Analysis":
            show_risk_analysis_page(ticker_list)

if __name__ == "__main__":
    main()
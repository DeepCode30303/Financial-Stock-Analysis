import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
import yfinance as yf

def show_calculator_page(ticker_list):
    sel_tickers = st.session_state.selected_tickers
    sel_tickers_list = ticker_list[ticker_list.symbol_name.isin(sel_tickers)].symbol
    yfdata = st.session_state.yfdata
    
    container = st.container()
    with container:
        cols_tab2 = st.columns((0.2, 0.8))
        total_inv = 0
        amounts = {}
        for i, ticker in enumerate(sel_tickers_list):
            cols = cols_tab2[1].columns((0.1, 0.3))
            try:
                cols[0].image('https://logo.clearbit.com/' + yf.Ticker(ticker).info['website'].replace('https://.', ''), width=65)
            except:
                cols[0].subheader(ticker)

            amount = cols[1].number_input('', key=ticker, step=50)
            total_inv += amount
            amounts[ticker] = amount

        cols_tab2[1].subheader('Total Investment:' + str(total_inv))
        cols_goal = cols_tab2[1].columns((0.06, 0.20, 0.7))
        cols_goal[0].text('')
        cols_goal[0].subheader('Goal: ')
        goal = cols_goal[1].number_input('', key='goal', step=50)

        # Create a new dataframe for the calculator
        if not yfdata.empty:
            calculator_df = yfdata.copy()
            calculator_df['amount'] = calculator_df['ticker'].map(amounts) * (1 + calculator_df['price_pct'])

            dfsum = calculator_df.groupby('Date').amount.sum().reset_index()
            fig = px.area(dfsum, x='Date', y='amount')
            fig.add_hline(y=goal, line_color='rgb(57,255,20)', line_dash='dash', line_width=3)
            
            if dfsum[dfsum.amount >= goal].shape[0] == 0:
                cols_tab2[1].warning("You won't reach your goal")
            else:
                fig.add_vline(x=dfsum[dfsum.amount >= goal].Date.iloc[0], line_color='rgb(57,255,20)', line_dash='dash', line_width=3)
                fig.add_trace(go.Scatter(x=[dfsum[dfsum.amount >= goal].Date.iloc[0] + dt.timedelta(days=7)], y=[goal * 1.1],
                                        text=[dfsum[dfsum.amount >= goal].Date.dt.date.iloc[0]],
                                        mode='text',
                                        name='Goal',
                                        textfont=dict(color='rgb(57,255,20)', size=20)))
            fig.update_layout(xaxis_title=None, yaxis_title=None)
            cols_tab2[1].plotly_chart(fig, use_container_width=True)
        else:
            cols_tab2[1].warning("Select stocks in the Portfolio section to use the Calculator.")
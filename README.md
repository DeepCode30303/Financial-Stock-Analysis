# Financial-Stock-Analysis Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Tech Stack](#tech-stack)
5. [Installation Guide](#installation-guide)
6. [User Guide](#user-guide)
7. [API References](#api-references)
8. [Code Structure](#code-structure)
9. [Future Enhancements](#future-enhancements)
10. [Technical Challenges](#technical-challenges)
11. [Glossary](#glossary)

## Project Overview

The Portfolio Analysis Application is a web-based platform that provides investors with tools to analyze stock portfolios, track performance, and make informed investment decisions. Built using Streamlit, the application combines financial data analysis with an intuitive user interface, allowing users to:

- Track portfolio performance
- Analyze individual stocks
- Calculate potential returns on investments
- Evaluate portfolio risk metrics
- Compare performance against benchmarks
- Access financial news and sentiment analysis

This application is designed to be accessible for both beginner and advanced investors, combining powerful analytical capabilities with an easy-to-use interface.

## Features

### Authentication System
- User registration with secure password hashing
- Login functionality with session management
- Password complexity validation
- Input validation for usernames and credentials

### Portfolio Management
- Multi-stock portfolio tracking
- Visual representation of performance over time
- Comparison of multiple stocks in a single view
- Customizable date ranges for analysis
- Individual stock performance metrics (50-day average, yearly highs/lows)

### Stock Details Analysis
- Detailed individual stock dashboard
- Price movement analysis with standard deviation and risk metrics
- Fundamental data views (balance sheet, income statement, cash flow)
- News integration with sentiment analysis
- Customizable parameters for stock analysis

### Investment Calculator
- Investment amount simulation for each stock
- Goal setting and tracking
- Visual representation of potential portfolio growth
- Goal achievement date prediction

### Risk Analysis
- Portfolio risk evaluation
- Minimum variance portfolio optimization
- Individual ticker risk assessment
- Benchmark comparison (S&P 500)
- Suggested investment allocation based on risk profiles
- Performance comparison charts

## System Architecture

The application follows a modular design pattern with clear separation of concerns:

```
project_root/
├── app.py              # Main application entry point
├── auth/               # Authentication module
│   ├── __init__.py     # Package initialization
│   ├── login.py        # Login/signup functionality
│   └── db.py           # Database operations
├── app_pages/              # Application pages
│   ├── __init__.py     # Package initialization
│   ├── portfolio.py    # Portfolio view
│   ├── stock_details.py # Stock analysis
│   ├── calculator.py   # Investment calculator
│   └── risk_analysis.py # Risk evaluation
└── utils/              # Utility functions
    ├── __init__.py     # Package initialization
    └── data_loader.py  # Data loading utilities
```

### Data Flow

1. User authenticates through the auth module
2. Main app (`app.py`) handles navigation and session state
3. Data is loaded via `utils/data_loader.py` and cached
4. Selected page modules render specific functionality
5. Financial data is retrieved from external APIs (yfinance, stocknews)
6. Visualizations are generated using Plotly
7. User interactions modify session state and trigger re-renders

## Tech Stack

- **Frontend & Backend**: Streamlit (Python-based web application framework)
- **Data Processing**: Pandas, NumPy
- **Data Visualization**: Plotly Express, Plotly Graph Objects
- **Financial Data**: yfinance, financedatabase
- **News & Sentiment**: stocknews
- **Database**: SQLite (for user authentication)
- **Authentication**: Custom implementation with hashlib
- **Optimization**: SciPy

## Installation Guide

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. Clone the repository or download the source code:
```bash
git clone <repository-url>
cd portfolio-analysis-app
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

5. Access the application at http://localhost:8501 in your web browser.

## User Guide

### Getting Started

1. **Registration**:
   - Click on "Go to Sign Up" on the login page
   - Enter a lowercase username, your name, and a secure password
   - Password must contain letters, numbers, and special characters
   - Click "Sign Up" to create your account

2. **Login**:
   - Enter your username and password
   - Click "Login" to access the application

3. **Navigation**:
   - Use the horizontal menu at the top to switch between sections:
     - Portfolio: For overall portfolio tracking
     - Stock Details: For individual stock analysis
     - Calculator: For investment projections
     - Risk Analysis: For portfolio risk assessment

### Portfolio Management

1. **Adding Stocks**:
   - Use the "Portfolio Builder" dropdown in the sidebar
   - Search and select multiple stocks to add to your portfolio
   - Set date ranges using the date pickers

2. **Analyzing Performance**:
   - View collective performance in the "All Stocks" chart
   - Examine individual stock performances in cards below
   - Click "Details for [ticker]" to view in-depth analysis

### Stock Analysis

1. **Viewing Stock Details**:
   - Access via clicking "Details for [ticker]" or from main navigation
   - Adjust parameters using the sidebar form if needed
   - Navigate tabs for pricing data, fundamentals, and news

2. **Interpreting Metrics**:
   - Price Movements: Historical price data and volatility
   - Fundamental Data: Balance sheet, income statement, cash flow
   - News: Latest articles with sentiment analysis

### Investment Calculator

1. **Setting Investment Amounts**:
   - Enter investment amount for each stock in your portfolio
   - Set a financial goal in the "Goal" field
   - View projected growth based on historical performance

2. **Goal Analysis**:
   - Green dotted line shows your goal amount
   - Vertical green line (if present) shows estimated goal achievement date
   - Warning appears if goal isn't achieved within the selected timeframe

### Risk Analysis

1. **Configuring Risk Assessment**:
   - Select stocks for risk analysis (defaults to portfolio selections)
   - View individual ticker risk metrics
   - Examine optimal portfolio weights for risk minimization

2. **Interpreting Results**:
   - Compare portfolio risk against benchmark
   - Review performance comparison chart
   - Analyze suggested investment allocation pie chart

## API References

The application uses several external APIs and libraries:

### Yahoo Finance (yfinance)
- Used to retrieve historical stock prices, ticker information, and fundamental data
- Documentation: https://pypi.org/project/yfinance/

### Finance Database
- Used to obtain a comprehensive list of stocks and ETFs
- Documentation: https://pypi.org/project/financedatabase/

### Stock News API
- Used to fetch news articles and sentiment analysis for stocks
- Documentation: https://pypi.org/project/stocknews/

## Code Structure

### Main Application (app.py)
- **Purpose**: Entry point for the Streamlit application
- **Key Functions**: 
  - `main()`: Initializes the app and handles navigation
  - Session state management for persistence across rerenders

### Authentication (auth/)
- **db.py**:
  - **Purpose**: Database operations for user authentication
  - **Key Functions**:
    - `create_connection()`: Establishes database connection
    - `create_table()`: Sets up users table
    - `hash_password()`: Secures passwords using SHA-256
    - `verify_user()`: Validates login credentials
    - `create_user()`: Registers new users

- **login.py**:
  - **Purpose**: User interface for authentication
  - **Key Functions**:
    - `is_user_authenticated()`: Checks login status
    - `show_login_page()`: Renders login UI
    - `show_signup_page()`: Renders registration UI

### Utilities (utils/)
- **data_loader.py**:
  - **Purpose**: Data loading and transformation
  - **Key Functions**:
    - `load_data()`: Loads and caches ticker list
    - `create_query_params()`: Generates URL parameters

### Pages (pages/)
- **portfolio.py**:
  - **Purpose**: Portfolio visualization and management
  - **Key Functions**: `show_portfolio_page()`

- **stock_details.py**:
  - **Purpose**: Individual stock analysis
  - **Key Functions**: `show_stock_details_page()`

- **calculator.py**:
  - **Purpose**: Investment projection calculations
  - **Key Functions**: `show_calculator_page()`

- **risk_analysis.py**:
  - **Purpose**: Portfolio risk assessment
  - **Key Functions**: 
    - `show_risk_analysis_page()`
    - `min_variance_weights()`: Portfolio optimization algorithm

## Future Enhancements

1. **Data Features**:
   - Real-time data streaming
   - Advanced technical indicators
   - Dividend analysis and tracking
   - ESG (Environmental, Social, Governance) metrics

2. **User Experience**:
   - Portfolio presets (e.g., tech-heavy, dividend focus)
   - Customizable dashboards
   - PDF report generation
   - Email notifications for price alerts

3. **Analysis Tools**:
   - Machine learning-based price prediction
   - Portfolio rebalancing recommendations
   - Tax optimization strategies
   - Stress testing against historical market scenarios

4. **Integrations**:
   - Brokerage account connections
   - Economic calendar integration
   - Export to Excel/CSV
   - Mobile application version

## Technical Challenges

During development, several technical challenges were addressed:

1. **State Management**:
   - Maintaining consistent state across Streamlit rerenders using session state
   - Preserving user selections when navigating between pages

2. **Data Processing**:
   - Efficient handling of multiple stock data retrieval
   - Optimizing calculations for portfolio performance metrics
   - Caching data to improve application performance

3. **User Experience**:
   - Creating intuitive visualizations for complex financial data
   - Balancing information density with usability
   - Handling edge cases in financial calculations

4. **Security**:
   - Implementing secure password hashing and storage
   - Input validation to prevent injection attacks
   - Secure session management

## Glossary

- **Standard Deviation**: A statistical measure of volatility or risk in stock returns
- **Risk-Adjusted Returns**: Performance metric that considers the risk taken to achieve returns
- **Minimum Variance Portfolio**: Portfolio allocation that minimizes overall volatility
- **Cumulative Returns**: Total returns over a specific period, accounting for compounding
- **Moving Average**: Average price over a specific period (e.g., 50-day average)
- **Sentiment Analysis**: Evaluation of news sentiment to gauge market perception
- **Balance Sheet**: Financial statement showing assets, liabilities, and equity
- **Income Statement**: Financial report showing revenues, expenses, and profits
- **Cash Flow Statement**: Report showing cash inflows and outflows

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json
import pandas as pd
import numpy as np
import ssl
import urllib.request



def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    # Create a new SSL context using the default settings
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Use this context when you open the URL
    response = urllib.request.urlopen(url, context=ssl_context)
    data = response.read().decode("utf-8")
    return json.loads(data)





import requests


def get_cash_flow(api_key, symbol):
    # Fetch the cash flow statement
    cash_flow_url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?apikey={api_key}"
    cash_flow_data = get_jsonparsed_data(cash_flow_url)
    df_cash_flow = pd.DataFrame(cash_flow_data)
    df_cash_flow['date'] = pd.to_datetime(df_cash_flow['date'])
    df_cash_flow.set_index('date', inplace=True)
    df_cash_flow.sort_index(ascending=True, inplace=True)
    return df_cash_flow


def get_market_cap(api_key, symbol):
    # Fetch the market cap
    market_cap_url = f"https://financialmodelingprep.com/api/v3/historical-market-capitalization/{symbol}?apikey={api_key}"
    market_cap_data = get_jsonparsed_data(market_cap_url)
    df_market_cap = pd.DataFrame(market_cap_data)
    df_market_cap['date'] = pd.to_datetime(df_market_cap['date'])
    df_market_cap.set_index('date', inplace=True)
    df_market_cap.sort_index(ascending=True, inplace=True)
        # Filter rows for years 2018 through 2022
    df_market_cap = df_market_cap.loc['2018':'2022']
    
    # Filter rows to keep only the last row for each year
    df_market_cap = df_market_cap.groupby(df_market_cap.index.year).last()
    
    return df_market_cap







def analyze_cash_flow(df_cash, df_revenue, df_market_cap):
    # Calculate Operating Cash Flow Margin (Operating Cash Flow / Total Revenue)
    df_cash['operating_cash_flow_margin'] = df_cash['netCashProvidedByOperatingActivities'] / df_revenue['revenue']
    print("Operating Cash Flow Margin: ", df_cash['operating_cash_flow_margin'].iloc[-1])
    print("The Operating Cash Flow Margin is a profitability ratio that measures cash generated from operations as a percentage of sales. It assesses the efficiency of the company's operations.\n")

    # Calculate Free Cash Flow (Operating Cash Flow - Capital Expenditure)
    df_cash['free_cash_flow'] = df_cash['netCashProvidedByOperatingActivities'] - df_cash['capitalExpenditure']
    print("Free Cash Flow: ", df_cash['free_cash_flow'].iloc[-1])
    print("Free Cash Flow (FCF) represents the cash that a company is able to generate after spending the money required to maintain or expand its asset base. It's an important measure because it allows a company to pursue opportunities that enhance shareholder value.\n")
    # Calculate Free Cash Flow Yield (Free Cash Flow / Market Cap)
    df_cash['free_cash_flow_yield'] = df_cash['free_cash_flow'].values / df_market_cap['marketCap'].values
    print("Free Cash Flow Yield: ", df_cash['free_cash_flow_yield'].iloc[-1])
    print("Free Cash Flow Yield (FCFY) is a financial solvency ratio that compares the free cash flow per share a company is expected to earn against its market value per share. The ratio is calculated by taking the free cash flow per share divided by the current market price per share.\n")
    html_string = f"""
    <div class='cash_flow_analysis'>
        <h2>Operating Cash Flow Margin:</h2>
        <p>{df_cash['operating_cash_flow_margin'].iloc[-1]}</p>
        <h2>Free Cash Flow:</h2>
        <p>{df_cash['free_cash_flow'].iloc[-1]}</p>
        <h2>Free Cash Flow Yield:</h2>
        <p>{df_cash['free_cash_flow_yield'].iloc[-1]}</p>
    </div>
    {df_cash.to_html()}
    """

    # Return the updated dataframe
    return html_string


def get_income_statement(api_key, symbol):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?apikey={api_key}"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    print(df.head())
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    return df

def get_balance_sheet(api_key, symbol):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?apikey={api_key}"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    return df

def analyze_company(df_balance, df_income):
    # Merge the two dataframes on date index
    df = pd.merge(df_balance, df_income, left_index=True, right_index=True)

    # Calculate Current Ratio (Current Assets / Current Liabilities)
    df['current_ratio'] = df['totalCurrentAssets'] / df['totalCurrentLiabilities']
    print("Current Ratio: ", df['current_ratio'].iloc[-1])
    print("The current ratio is a liquidity ratio that measures a company's ability to cover its short-term obligations with its current assets.\n")

    # Calculate Debt to Equity Ratio (Total Debt / Total Equity)
    df['debt_equity_ratio'] = df['totalDebt'] / df['totalStockholdersEquity']
    print("Debt to Equity Ratio: ", df['debt_equity_ratio'].iloc[-1])
    print("The debt to equity ratio provides information on a company's leverage, showing the proportion of a company's operations that are financed by debt compared to equity.\n")

    # Calculate Return on Assets (Net Income / Total Assets)
    df['return_on_assets'] = df['netIncome'] / df['totalAssets'] # netIncome_x from income statement
    print("Return on Assets: ", df['return_on_assets'].iloc[-1])
    print("Return on assets (ROA) is a profitability ratio that provides how much profit a company is able to generate from its assets.\n")

    # Calculate Return on Equity (Net Income / Shareholder's Equity)
    df['return_on_equity'] = df['netIncome'] / df['totalStockholdersEquity']
    print("Return on Equity: ", df['return_on_equity'].iloc[-1])
    print("Return on equity (ROE) is a measure of financial performance, and it's considered the return on net assets. ROE is considered a measure of how effectively management is using a company’s assets to create profits.\n")
    
    html_string = f"""
    <div class='company_analysis'>
        <h2>Current Ratio:</h2>
        <p>{df['current_ratio'].iloc[-1]}</p>
        <h2>Debt to Equity Ratio:</h2>
        <p>{df['debt_equity_ratio'].iloc[-1]}</p>
        <h2>Return on Assets:</h2>
        <p>{df['return_on_assets'].iloc[-1]}</p>
        <h2>Return on Equity:</h2>
        <p>{df['return_on_equity'].iloc[-1]}</p>
    </div>
    {df.to_html()}
    """
    return html_string



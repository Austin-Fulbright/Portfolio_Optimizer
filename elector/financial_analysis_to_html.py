

from financial_statement_alys import *



def get_report_html():

    api_key = '144e3e060ffd297fdde52195f9b053cf'
    symbol = 'APPL'
    df_income = get_income_statement(api_key, symbol)
    df_revenue = df_income[['revenue']]
    df_cash = get_cash_flow(api_key, symbol)
    df_market_cap = get_market_cap(api_key, symbol)
    html1 = analyze_cash_flow(df_cash, df_revenue, df_market_cap)
    df_balance = get_balance_sheet(api_key, symbol)
    html2 = analyze_company(df_balance, df_income)

    html_doc = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stock Analysis Report</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <h1>Analysis Report for {tick}</h1>
        {html1}
        {html2}
    </body>
    </html>
    """

    with open('report.html', 'w') as f:
        f.write(html_doc)

    return html_doc




get_report_html()


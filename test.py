from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import EfficientFrontier
from pypfopt import HRPOpt
from pypfopt import CLA
from pypfopt import BlackLittermanModel
from pypfopt import plotting
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the price data
df = pd.read_csv("stock_prices.csv", parse_dates=True, index_col="date")

# Calculate the expected returns
mu = expected_returns.mean_historical_return(df)

# Calculate the covariance matrix
S = risk_models.sample_cov(df)

# Directory to save plots
if not os.path.exists('plots'):
    os.makedirs('plots')

# Use mean-variance optimization
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe() 
weights_df = pd.DataFrame(list(weights.items()),columns = ['Ticker','Weight']) 
weights_df.to_csv("mvo_weights.csv", index=False)
weights_df.plot.pie(y='Weight', labels=weights_df['Ticker'], figsize=(10, 10), autopct='%1.1f%%')
plt.title('Mean Variance Optimization Weights')
plt.savefig('plots/mvo_weights.png')
plt.close()
print("Mean Variance Optimization Weights:", weights)

# Plot the efficient frontier
ef_for_plot = EfficientFrontier(mu, S)
fig, ax = plt.subplots()
plotting.plot_efficient_frontier(ef_for_plot, ax=ax, show_assets=True)
plt.savefig('efficient_frontier.png')

# Create the Hierarchical Risk Parity model
hrp = HRPOpt(df.pct_change().dropna())
hrp_weights = hrp.optimize()
hrp_weights_df = pd.DataFrame(list(hrp_weights.items()),columns = ['Ticker','Weight']) 
hrp_weights_df.to_csv("hrp_weights.csv", index=False)
hrp_weights_df.plot.pie(y='Weight', labels=hrp_weights_df['Ticker'], figsize=(10, 10), autopct='%1.1f%%')
plt.title('Hierarchical Risk Parity Weights')
plt.savefig('plots/hrp_weights.png')
plt.close()
print("Hierarchical Risk Parity Weights:", hrp_weights)

# Create the Black-Litterman model
bl = BlackLittermanModel(S, absolute_views= {"AAPL": 0.10})
bl_weights = bl.bl_weights()
bl_weights_df = pd.DataFrame(list(bl_weights.items()),columns = ['Ticker','Weight']) 
bl_weights_df.to_csv("bl_weights.csv", index=False)

# Fix negative weights for the pie chart
bl_weights_df_fixed = bl_weights_df.copy()
bl_weights_df_fixed.loc[bl_weights_df_fixed['Weight'] < 0, 'Weight'] = 0

# Ensure the weights sum to 1 after the adjustment
bl_weights_df_fixed['Weight'] /= bl_weights_df_fixed['Weight'].sum()

# Now use the fixed dataframe to plot the pie chart
bl_weights_df_fixed.plot.pie(y='Weight', labels=bl_weights_df_fixed['Ticker'], figsize=(10, 10), autopct='%1.1f%%')
plt.title('Black-Litterman Weights')
plt.savefig('plots/bl_weights.png')
plt.close()
print("Black-Litterman Weights:", bl_weights)


# Create the Critical Line Algorithm model
cla = CLA(mu, S)
cla_weights = cla.max_sharpe()
cla_weights_df = pd.DataFrame(list(cla_weights.items()),columns = ['Ticker','Weight']) 
cla_weights_df.to_csv("cla_weights.csv", index=False)

# Fix negative weights for the pie chart
cla_weights_df_fixed = cla_weights_df.copy()
cla_weights_df_fixed.loc[cla_weights_df_fixed['Weight'] < 0, 'Weight'] = 0

# Ensure the weights sum to 1 after the adjustment
cla_weights_df_fixed['Weight'] /= cla_weights_df_fixed['Weight'].sum()

# Now use the fixed dataframe to plot the pie chart
cla_weights_df_fixed.plot.pie(y='Weight', labels=cla_weights_df_fixed['Ticker'], figsize=(10, 10), autopct='%1.1f%%')
plt.title('Critical Line Algorithm Weights')
plt.savefig('plots/cla_weights.png')
plt.close()
print("Critical Line Algorithm Weights:", cla_weights)


# Function to convert CSV to HTML table
def csv_to_html(file_path):
    df = pd.read_csv(file_path)
    return df.to_html(index=False)

# Function to convert image to HTML img
def img_to_html(file_path):
    return f'<img src="{file_path}" alt="Image" width="500" height="600">'


# HTML content
html_content = ""

# Add Mean Variance Optimization results
html_content += "<h1>Mean Variance Optimization</h1>"
html_content += "<p>Mean Variance Optimization is an approach developed by Harry Markowitz, under which the objective is to minimize the portfolio variance and a given level of expected return. It's based on the idea that an investor should take on no more risk than that which is necessary to achieve their desired level of return. In the pie chart, each slice represents the proportion of the total funds that should be invested in a given stock to achieve the highest Sharpe ratio, i.e., the best risk-adjusted return.</p>"
html_content += img_to_html('plots/mvo_weights.png')
html_content += csv_to_html('mvo_weights.csv')

# Add Hierarchical Risk Parity results
html_content += "<h1>Hierarchical Risk Parity</h1>"
html_content += "<p>Hierarchical Risk Parity (HRP) is a modern portfolio theory proposed by Marcos Lopez de Prado, which uses machine learning to construct portfolios. HRP does not require any parameter estimation, making it particularly suited to large datasets where parameter estimation is noisy. The pie chart displays the proportion of the total funds that should be invested in each stock according to the HRP model.</p>"
html_content += img_to_html('plots/hrp_weights.png')
html_content += csv_to_html('hrp_weights.csv')

# Add Black-Litterman results
html_content += "<h1>Black-Litterman</h1>"
html_content += "<p>The Black-Litterman model is a mathematical model for portfolio allocation developed by Fischer Black and Robert Litterman. This model allows investors to combine their unique views regarding the performance of various assets with the market equilibrium in a manner that results in intuitive, diversified portfolios. The pie chart presents the proportion of the total funds that should be invested in each stock according to the Black-Litterman model.</p>"
html_content += img_to_html('plots/bl_weights.png')
html_content += csv_to_html('bl_weights.csv')

# Add Critical Line Algorithm results
html_content += "<h1>Critical Line Algorithm</h1>"
html_content += "<p>The Critical Line Algorithm (CLA) is a method used in portfolio optimization, specifically in finding the optimal portfolio that lies along the efficient frontier. CLA is particularly useful when dealing with a large number of assets and constraints. The pie chart shows the proportion of the total funds that should be invested in each stock according to the CLA model.</p>"
html_content += img_to_html('plots/cla_weights.png')
html_content += csv_to_html('cla_weights.csv')

# Write to HTML file
with open('results.html', 'w') as f:
    f.write(html_content)







from util import *



# Load the price data
df = load_data()
# Calculate the expected returns
mu = get_expected_returns(df)

# Calculate the covariance matrix
S = get_sample_cov(df)

create_directory_if_not_exists('plots')

# Use mean-variance optimization
ef = EfficientFrontier(mu, S)
weights = calculate_and_save_weights('Mean Variance Optimization', ef.max_sharpe, 'data/mvo_weights.csv', 'plots/mvo_weights.png')

# Plot the efficient frontier
ef_for_plot = EfficientFrontier(mu, S)
fig, ax = plt.subplots()
plotting.plot_efficient_frontier(ef_for_plot, ax=ax, show_assets=True)
plt.savefig('plots/efficient_frontier.png')

# Create the Hierarchical Risk Parity model
hrp = HRPOpt(df.pct_change().dropna())
hrp_weights = hrp.optimize()
hrp_weights_df = pd.DataFrame(list(hrp_weights.items()),columns = ['Ticker','Weight']) 
hrp_weights_df.to_csv("data/hrp_weights.csv", index=False)
hrp_weights_df.plot.pie(y='Weight', labels=hrp_weights_df['Ticker'], figsize=(10, 10), autopct='%1.1f%%')
plt.title('Hierarchical Risk Parity Weights')
plt.savefig('plots/hrp_weights.png')
plt.close()
print("Hierarchical Risk Parity Weights:", hrp_weights)

# Create the Black-Litterman model

# Change absolute views to match your own views

bl = BlackLittermanModel(S, absolute_views= {"AAPL": 0.10})
bl_weights = bl.bl_weights()
bl_weights_df = pd.DataFrame(list(bl_weights.items()),columns = ['Ticker','Weight']) 
bl_weights_df.to_csv("data/bl_weights.csv", index=False)

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
cla_weights_df.to_csv("data/cla_weights.csv", index=False)

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

    # Additional part to plot covariance matrix, dendrogram, and weights
plotting.plot_covariance(S, show_tickers=True)
plt.savefig('plots/covariance_matrix.png')
plt.close()

# Plot dendrogram for HRP model
plotting.plot_dendrogram(hrp)
plt.savefig('plots/hrp_dendrogram.png')
plt.close()

# Plot weights for each model
plotting.plot_weights(weights)
plt.savefig('plots/mvo_weights_plot.png')
plt.close()

plotting.plot_weights(hrp_weights)
plt.savefig('plots/hrp_weights_plot.png')
plt.close()

plotting.plot_weights(bl_weights)
plt.savefig('plots/bl_weights_plot.png')
plt.close()

plotting.plot_weights(cla_weights)
plt.savefig('plots/cla_weights_plot.png')
plt.close()

html_content = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>

<div class="section">
    <h1 class="section-title">Mean Variance Optimization</h1>
    <p class="section-desc">Mean Variance Optimization is an approach developed by Harry Markowitz...</p>
    """ + img_to_html('plots/mvo_weights.png', 'img-plot') + csv_to_html('data/mvo_weights.csv', 'table-data') + """
</div>

<div class="section">
    <h1 class="section-title">Hierarchical Risk Parity</h1>
    <p class="section-desc">Hierarchical Risk Parity (HRP) is a modern portfolio theory...</p>
    """ + img_to_html('plots/hrp_weights.png', 'img-plot') + csv_to_html('data/hrp_weights.csv', 'table-data') + """
</div>

<div class="section">
    <h1 class="section-title">Black-Litterman</h1>
    <p class="section-desc">The Black-Litterman model is a mathematical model for portfolio allocation...</p>
    """ + img_to_html('plots/bl_weights.png', 'img-plot') + csv_to_html('data/bl_weights.csv', 'table-data') + """
</div>

<div class="section">
    <h1 class="section-title">Critical Line Algorithm</h1>
    <p class="section-desc">The Critical Line Algorithm (CLA) is a method used in portfolio optimization...</p>
    """ + img_to_html('plots/cla_weights.png', 'img-plot') + csv_to_html('data/cla_weights.csv', 'table-data') + """
</div>

<div class="section">
    <h1 class="section-title">Covariance Matrix</h1>
    <p class="section-desc">The covariance matrix is a matrix that contains the variances and covariances...</p>
    """ + img_to_html('plots/covariance_matrix.png', 'img-plot') + """
</div>

<div class="section">
    <h1 class="section-title">HRP Dendrogram</h1>
    <p class="section-desc">The dendrogram is a tree diagram frequently used to illustrate the arrangement of the clusters...</p>
    """ + img_to_html('plots/hrp_dendrogram.png', 'img-plot') + """
</div>

<div class="section">
    <h1 class="section-title">Model Weights Plots</h1>
    <p class="section-desc">The plots below illustrate the weights assigned to each asset by the respective models.</p>

    <h2 class="subsection-title">Mean Variance Optimization Weights Plot</h2>
    """ + img_to_html('plots/mvo_weights_plot.png', 'img-plot') + """

    <h2 class="subsection-title">Hierarchical Risk Parity Weights Plot</h2>
    """ + img_to_html('plots/hrp_weights_plot.png', 'img-plot') + """

    <h2 class="subsection-title">Black-Litterman Weights Plot</h2>
    """ + img_to_html('plots/bl_weights_plot.png', 'img-plot') + """

    <h2 class="subsection-title">Critical Line Algorithm Weights Plot</h2>
    """ + img_to_html('plots/cla_weights_plot.png', 'img-plot') + """
</div>

</body>
</html>
"""

# Write to HTML file
with open('results/results.html', 'w') as f:
    f.write(html_content)





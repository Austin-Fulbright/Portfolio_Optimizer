from pypfopt import risk_models, expected_returns, EfficientFrontier, HRPOpt, CLA, BlackLittermanModel, plotting
import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data():
    return pd.read_csv("data/stock_prices.csv", parse_dates=True, index_col="date")

def get_expected_returns(df):
    return expected_returns.mean_historical_return(df)

def get_sample_cov(df):
    return risk_models.sample_cov(df)

def create_directory_if_not_exists(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def calculate_and_save_weights(optimization_model, optimization_func, weights_csv, weights_png):
    weights = optimization_func()
    weights_df = pd.DataFrame(list(weights.items()),columns = ['Ticker','Weight']) 
    weights_df.to_csv(weights_csv, index=False)
    weights_df.plot.pie(y='Weight', labels=weights_df['Ticker'], figsize=(10, 10), autopct='%1.1f%%')
    plt.title(f'{optimization_model} Weights')
    plt.savefig(weights_png)
    plt.close()
    print(f"{optimization_model} Weights:", weights)
    
    return weights

def img_to_html(img_path, class_name=''):
    return f'<img src="{img_path}" class="{class_name}">'

def csv_to_html(csv_path, class_name=''):
    df = pd.read_csv(csv_path)
    return df.to_html(classes=class_name)
def create_html_content(img_paths, csv_paths, model_names, html_path):
    section_templates = """
    <div class="section">
        <h1 class="section-title">{model_name}</h1>
        <p class="section-desc">{model_name} is a method used in portfolio optimization...</p>
        {img_html}
        {csv_html}
    </div>
    """
    sections = []
    for img_path, csv_path, model_name in zip(img_paths, csv_paths, model_names):
        img_html = img_to_html(img_path, 'img-plot')
        csv_html = csv_to_html(csv_path, 'table-data')
        sections.append(section_templates.format(model_name=model_name, img_html=img_html, csv_html=csv_html))
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
    """ + "\n".join(sections) + """
    </body>
    </html>
    """
    with open(html_path, 'w') as f:
        f.write(html_content)
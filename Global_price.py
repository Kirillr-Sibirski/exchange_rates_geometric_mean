import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gmean

API_KEY = 'U4NCYKVQRFKWAANL'
BASE_URL = "https://www.alphavantage.co/query"

def fetch_forex_data(base, quote):
    """Fetch historical forex data for the given currency pair from Alpha Vantage."""
    params = {
        'function': 'FX_MONTHLY',
        'from_symbol': base,
        'to_symbol': quote,
        'apikey': API_KEY,
        'datatype': 'json'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print("Failed to fetch data: ", response.status_code)
        return pd.DataFrame()  # Return empty DataFrame on failure
    try:
        data = response.json()['Time Series FX (Monthly)']
    except KeyError:
        print("KeyError - check the API response for error messages:")
        print(response.json())  # Log the entire JSON response to debug
        return pd.DataFrame()

    rows = []
    for date, rate_info in data.items():
        rows.append({'Date': date, 'Rate': float(rate_info['4. close']), 'Base': base, 'Quote': quote})
    return pd.DataFrame(rows)

def process_data(currencies):
    combined_df = pd.DataFrame()
    for base, quote in currencies:
        df = fetch_forex_data(base, quote)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    combined_df['Date'] = pd.to_datetime(combined_df['Date'])
    combined_df.sort_values(by='Date', inplace=True)
    return combined_df

def filter_common_period(df1, df2, df3):
    """Filter dataframes to the common period between them."""
    common_start = max(df1['Date'].min(), df2['Date'].min(), df3['Date'].min())
    common_end = min(df1['Date'].max(), df2['Date'].max(), df3['Date'].max())
    return df1[(df1['Date'] >= common_start) & (df1['Date'] <= common_end)], df2[(df2['Date'] >= common_start) & (df2['Date'] <= common_end)], df3[(df3['Date'] >= common_start) & (df3['Date'] <= common_end)]

def calculate_geometric_mean(df):
    return 1 / df.groupby('Date')['Rate'].transform(gmean)  # Reciprocal of geometric mean

def plot_data(df_usd, df_eur, df_gbp):
    plt.figure(figsize=(15, 10))
    plt.plot(df_usd['Date'], df_usd['Geometric Mean'], label='USD Base')
    plt.plot(df_eur['Date'], df_eur['Geometric Mean'], label='EUR Base')
    plt.plot(df_gbp['Date'], df_gbp['Geometric Mean'], label='GBP Base')
    plt.title('Comparison of Global Currency Values Based on USD, EUR, GBP')
    plt.xlabel('Year')
    plt.ylabel('Price Of The Global Currency (Reciprocal of Geometric Mean)')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # USD based rates
    currencies_usd = [
        ('USD', 'EUR'), ('USD', 'GBP'), ('USD', 'BRL'), ('USD', 'AUD'), 
        ('USD', 'CAD'), ('USD', 'CHF'), ('USD', 'CNY'), ('USD', 'COP'), 
        ('USD', 'ILS'), ('USD', 'INR'), ('USD', 'JPY'), ('USD', 'MXN'), 
        ('USD', 'PHP'), ('USD', 'SEK'), ('USD', 'KRW'), ('USD', 'NZD'), 
        ('USD', 'PLN'), ('USD', 'SGD'), ('USD', 'TRY'), ('USD', 'THB')
    ]
    df_usd = process_data(currencies_usd)
    df_usd['Geometric Mean'] = calculate_geometric_mean(df_usd)

    # EUR based rates
    currencies_eur = [
        ('EUR', 'USD'), ('EUR', 'GBP'), ('EUR', 'BRL'), ('EUR', 'AUD'), 
        ('EUR', 'CAD'), ('EUR', 'CHF'), ('EUR', 'CNY'), ('EUR', 'COP'), 
        ('EUR', 'ILS'), ('EUR', 'INR'), ('EUR', 'JPY'), ('EUR', 'MXN'), 
        ('EUR', 'PHP'), ('EUR', 'SEK'), ('EUR', 'KRW'), ('EUR', 'NZD'), 
        ('EUR', 'PLN'), ('EUR', 'SGD'), ('EUR', 'TRY'), ('EUR', 'THB')
    ]
    df_eur = process_data(currencies_eur)
    df_eur['Geometric Mean'] = calculate_geometric_mean(df_eur)

    # GBP based rates, replacing the previous COP rates
    currencies_gbp = [
        ('GBP', 'USD'), ('GBP', 'EUR'), ('GBP', 'BRL'), ('GBP', 'AUD'),
        ('GBP', 'CAD'), ('GBP', 'CHF'), ('GBP', 'CNY'), ('GBP', 'COP'),
        ('GBP', 'ILS'), ('GBP', 'INR'), ('GBP', 'JPY'), ('GBP', 'MXN'),
        ('GBP', 'PHP'), ('GBP', 'SEK'), ('GBP', 'KRW'), ('GBP', 'NZD'),
        ('GBP', 'PLN'), ('GBP', 'SGD'), ('GBP', 'TRY'), ('GBP', 'THB')
    ]
    df_gbp = process_data(currencies_gbp)
    df_gbp['Geometric Mean'] = calculate_geometric_mean(df_gbp)

    # Filter for common period
    df_usd, df_eur, df_gbp = filter_common_period(df_usd, df_eur, df_gbp)

    plot_data(df_usd, df_eur, df_gbp)

if __name__ == "__main__":
    main()
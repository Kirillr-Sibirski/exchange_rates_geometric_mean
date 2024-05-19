import pandas as pd
import numpy as np
from currency_converter import CurrencyConverter, RateNotFoundError

# Function to calculate geometric mean
def geometric_mean(values):
    product = np.prod(values)
    geometric_mean = product ** (1 / len(values))
    return geometric_mean

# Function to fetch exchange rate data for all currencies
def fetch_all_exchange_rates():
    counterNotFound = 0
    counterFound = 0
    c = CurrencyConverter()
    currencies = c.currencies
    exchange_rates_data = {}
    for base_currency in currencies:
        rates = {}
        for quote_currency in currencies:
            try:
                exchange_rate = c.convert(1, base_currency, quote_currency)
                rates[quote_currency] = exchange_rate
                counterFound+=1
            except RateNotFoundError:
                # Skip currencies that raise RateNotFoundError
                counterNotFound+=1
                print("Rate not found: ",base_currency,"/",quote_currency)
                continue
        exchange_rates_data[base_currency] = rates
    return exchange_rates_data, counterNotFound, counterFound


# Example exchange rate data (replace with API fetch)
exchange_rates_data = fetch_all_exchange_rates()[0]

# Convert exchange rate data to DataFrame
exchange_rates_list = []
for base_currency, rates in exchange_rates_data.items():
    for currency, exchange_rate in rates.items():
        exchange_rates_list.append({'Base Currency': base_currency, 'Quote Currency': currency, 'Exchange Rate': exchange_rate})
exchange_rates_df = pd.DataFrame(exchange_rates_list)

# Calculate geometric mean
geometric_mean_rate = geometric_mean(exchange_rates_df['Exchange Rate'])

# Print the geometric mean
print("Rates not found:",fetch_all_exchange_rates()[1], 
      "\nTotal rates found:",fetch_all_exchange_rates()[2], 
      "\nPercent found of the total amount:",round(fetch_all_exchange_rates()[2]/(fetch_all_exchange_rates()[1]+fetch_all_exchange_rates()[2])*100),"%"
      "\nGeometric mean of exchange rates:", geometric_mean_rate
)

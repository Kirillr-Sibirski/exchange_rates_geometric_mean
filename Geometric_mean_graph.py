import pandas as pd
import numpy as np
from currency_converter import CurrencyConverter, RateNotFoundError
from datetime import date
from dateutil.relativedelta import relativedelta

def geometric_mean(values):
    if not values:
        return None
    log_values = np.log(values)
    mean_log = np.mean(log_values)
    print(np.exp(mean_log))
    return np.exp(mean_log)

def fetch_all_exchange_rates(date):
    c = CurrencyConverter(fallback_on_missing_rate=True, fallback_on_wrong_date=True)
    currencies = c.currencies
    exchange_rates_data = {}
    for base_currency in currencies:
        rates = {}
        for quote_currency in currencies:
            if base_currency != quote_currency:  # Exclude same-currency conversions
                try:
                    exchange_rate = c.convert(1, base_currency, quote_currency, date=date)
                    rates[quote_currency] = exchange_rate
                except RateNotFoundError:
                    continue
        if rates:
            exchange_rates_data[base_currency] = rates
    return exchange_rates_data

def collect_geometric_means(start_date, end_date):
    results = []
    current_date = start_date
    while current_date >= end_date:
        daily_data = fetch_all_exchange_rates(current_date)
        if daily_data:
            exchange_rates_list = []
            for base, rates in daily_data.items():
                exchange_rates_list.extend(rates.values())
            if exchange_rates_list:
                gm = geometric_mean(exchange_rates_list)
                results.append({'Date': current_date, 'Geometric Mean': gm})
        current_date -= relativedelta(months=3)
    return results

start_date = date(2024, 1, 1)  # Assuming typo fixed, and this is the past date
end_date = date(2014, 1, 1)

# Display the table with geometric means
geometric_means_table = pd.DataFrame(collect_geometric_means(start_date, end_date))
print(geometric_means_table)

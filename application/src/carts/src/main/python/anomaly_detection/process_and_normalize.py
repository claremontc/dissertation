# python/anomaly_detection/process_and_normalize.py
import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from prometheus_fetcher import fetch_prometheus_data

QUERY = 'rate(request_duration_seconds_sum{job="cartservice"}[1m])'

data = fetch_prometheus_data(QUERY)

metrics_data = []
for result in data:
    metric = result['value']
    timestamp = metric[0]
    value = float(metric[1])
    metrics_data.append([timestamp, value])

df = pd.DataFrame(metrics_data, columns=['timestamp', 'request_duration_seconds'])

scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(df[['request_duration_seconds']])

print(normalized_data)

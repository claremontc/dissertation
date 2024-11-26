import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import time
import matplotlib.pyplot as plt
import joblib


prometheus_url = 'http://172.21.212.175:31090/api/v1/query_range'
query = 'rate(request_duration_seconds_bucket{kubernetes_namespace="sock-shop"}[1m])'
start_time = int(time.time()) - 3600 
end_time = int(time.time())
step = 60 

params = {
    'query': query,
    'start': start_time,
    'end': end_time,
    'step': step
}


response = requests.get(prometheus_url, params=params)


data = response.json()
if not data['data']['result']:
    print("No data returned from Prometheus query.")
    exit()


df = pd.DataFrame(data['data']['result'][0]['values'], columns=['timestamp', 'value'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
df['value'] = pd.to_numeric(df['value'])


print("Missing values before filling:", df.isnull().sum())


df.ffill(inplace=True)


print("Missing values after filling:", df.isnull().sum())


df['hour'] = df['timestamp'].dt.hour
df['weekday'] = df['timestamp'].dt.weekday


df['mean_duration'] = df['value'].rolling(window=10).mean()  
df['std_duration'] = df['value'].rolling(window=10).std()  


df['mean_duration'] = df['mean_duration'].fillna(0)
df['std_duration'] = df['std_duration'].fillna(0)


median_mean_duration = df['mean_duration'].median()
median_std_duration = df['std_duration'].median()

df['mean_duration'] = df['mean_duration'].replace(0, median_mean_duration)
df['std_duration'] = df['std_duration'].replace(0, median_std_duration)


anomaly_threshold = 0.90  
df['anomaly'] = df['mean_duration'].apply(lambda x: 1 if x > df['mean_duration'].quantile(anomaly_threshold) else 0)


print("Number of anomalies detected:", df['anomaly'].sum())


scaler = MinMaxScaler()
df[['mean_duration', 'std_duration']] = scaler.fit_transform(df[['mean_duration', 'std_duration']])


plt.plot(df['timestamp'], df['mean_duration'])
plt.title("Mean Duration over Time")
plt.xlabel("Timestamp")
plt.ylabel("Mean Duration")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('mean_duration_plot_2.png')  


X = df[['mean_duration', 'std_duration']]
y = df['anomaly']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

joblib.dump((X_train, X_test, y_train, y_test), 'preprocessed_data.pkl')


print("First few rows of training data:")
print(X_train.head())



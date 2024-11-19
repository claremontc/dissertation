
import requests

PROMETHEUS_URL = 'http://172.21.212.175:31090/api/v1/query'

def fetch_prometheus_data(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query}, timeout=30)
    if response.status_code == 200:
        data = response.json()
        print(data)  
        return data['data']['result']
    else:
        print(f"Error fetching data: {response.status_code}")
        return []


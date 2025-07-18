import requests
import time
from datetime import datetime

API_ENDPOINTS = [
    # Add your API endpoints here
    "https://jsonplaceholder.typicode.com/posts/1",
    # ...add more endpoints as needed...
]
MONITOR_INTERVAL = 30  # seconds
MONITOR_API = "http://localhost:5000/metrics"

def monitor():
    while True:
        for endpoint in API_ENDPOINTS:
            start = time.time()
            error = None
            status_code = 0
            try:
                resp = requests.get(endpoint, timeout=10)
                status_code = resp.status_code
            except Exception as e:
                error = str(e)
            elapsed = time.time() - start
            metric = {
                "timestamp": datetime.utcnow().isoformat(),
                "endpoint": endpoint,
                "response_time": elapsed,
                "status_code": status_code,
                "error": error
            }
            try:
                requests.post(MONITOR_API, json=metric, timeout=5)
            except Exception:
                pass  # Don't crash on reporting errors
        time.sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    monitor()

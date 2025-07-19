from flask import Flask, request, jsonify
from prometheus_client import generate_latest, Counter, Gauge, Histogram, Summary
import time

app = Flask(__name__)

# --- Prometheus Metrics ---
# Counter: A cumulative metric that represents a single numerical value that only ever goes up.
REQUEST_COUNT = Counter(
    'app_requests_total', 'Total number of HTTP requests', ['method', 'endpoint']
)

# Gauge: A metric that represents a single numerical value that can arbitrarily go up and down.
IN_PROGRESS_REQUESTS = Gauge(
    'app_in_progress_requests', 'Number of requests currently being processed'
)

# Histogram: Samples observations (e.g., request durations) and counts them in configurable buckets.
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds', 'Request latency in seconds', ['endpoint']
)

# Summary: Similar to Histogram, but calculates configurable quantiles over a sliding time window.
# Not used in this simple example but good to know for future reference.
# REQUEST_SIZE_BYTES = Summary(
#     'app_request_size_bytes', 'Request size in bytes'
# )


@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return "Hello, this is your monitored application!"

@app.route('/slow')
def slow_endpoint():
    with IN_PROGRESS_REQUESTS.track_inprogress():
        start_time = time.time()
        REQUEST_COUNT.labels(method='GET', endpoint='/slow').inc()
        time.sleep(2)  # Simulate some work
        latency = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint='/slow').observe(latency)
        return "This was a slow endpoint."

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

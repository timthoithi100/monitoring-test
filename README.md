# Monitoring Test Application

A simple Flask web application demonstrating Prometheus metrics integration for application monitoring and observability.

## Overview

This project showcases how to instrument a Python Flask application with Prometheus metrics to monitor application performance, request patterns, and system health. It serves as a practical example for implementing observability in web applications.

## Features

- **Flask Web Application**: Lightweight web server with multiple endpoints
- **Prometheus Metrics Integration**: Built-in metrics collection and exposure
- **Multiple Metric Types**: Demonstrates Counter, Gauge, and Histogram metrics
- **Request Monitoring**: Tracks request counts, latency, and in-progress requests
- **Metrics Endpoint**: Exposes metrics in Prometheus format for scraping

## Project Structure

```
monitoring-test/
├── app.py              # Main Flask application with Prometheus metrics
└── README.md           # Project documentation (this file)
```

## Prerequisites

- Python 3.6+
- pip (Python package installer)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/timthoithi100/monitoring-test.git
   cd monitoring-test
   ```

2. **Install dependencies**:
   ```bash
   pip install flask prometheus_client
   ```

## Usage

### Running the Application

Start the Flask application:

```bash
python app.py
```

The application will be available at `http://localhost:8000`

### Available Endpoints

#### Application Endpoints

- **`GET /`** - Home endpoint
  - Returns a simple welcome message
  - Tracked by request counter

- **`GET /slow`** - Slow endpoint simulation
  - Simulates a slow operation (2-second delay)
  - Demonstrates in-progress request tracking
  - Measures and records request latency

#### Monitoring Endpoints

- **`GET /metrics`** - Prometheus metrics endpoint
  - Returns metrics in Prometheus exposition format
  - Used by Prometheus server for scraping metrics data

### Testing the Application

1. **Test the home endpoint**:
   ```bash
   curl http://localhost:8000/
   ```

2. **Test the slow endpoint**:
   ```bash
   curl http://localhost:8000/slow
   ```

3. **View metrics**:
   ```bash
   curl http://localhost:8000/metrics
   ```

## Metrics Explained

### Counter Metrics
- **`app_requests_total`**: Total number of HTTP requests
  - Labels: `method` (HTTP method), `endpoint` (request path)
  - Increments with each request to tracked endpoints

### Gauge Metrics
- **`app_in_progress_requests`**: Number of requests currently being processed
  - Increases when request processing starts
  - Decreases when request processing completes
  - Useful for monitoring application load

### Histogram Metrics
- **`app_request_latency_seconds`**: Request processing time in seconds
  - Labels: `endpoint` (request path)
  - Automatically creates buckets for latency distribution
  - Provides percentile calculations and average response times

## Prometheus Integration

### Setting up Prometheus

1. **Install Prometheus** (example for macOS):
   ```bash
   brew install prometheus
   ```

2. **Configure Prometheus** (`prometheus.yml`):
   ```yaml
   global:
     scrape_interval: 15s

   scrape_configs:
     - job_name: 'flask-app'
       static_configs:
         - targets: ['localhost:8000']
       scrape_interval: 5s
       metrics_path: '/metrics'
   ```

3. **Run Prometheus**:
   ```bash
   prometheus --config.file=prometheus.yml
   ```

4. **Access Prometheus UI**: `http://localhost:9090`

### Example Queries

Use these PromQL queries in the Prometheus UI:

- **Request rate**: `rate(app_requests_total[5m])`
- **Average latency**: `rate(app_request_latency_seconds_sum[5m]) / rate(app_request_latency_seconds_count[5m])`
- **95th percentile latency**: `histogram_quantile(0.95, rate(app_request_latency_seconds_bucket[5m]))`
- **Current in-progress requests**: `app_in_progress_requests`

## Monitoring Best Practices

### Metric Types Usage
- **Counters**: Use for cumulative values that only increase (requests, errors, bytes processed)
- **Gauges**: Use for values that can go up and down (memory usage, active connections, temperature)
- **Histograms**: Use for measuring distributions (request latency, response sizes)

### Labeling Strategy
- Keep labels low-cardinality to avoid performance issues
- Use consistent label names across metrics
- Avoid user-generated content in labels

### Performance Considerations
- Metrics collection adds minimal overhead
- Be mindful of label cardinality explosion
- Consider sampling for high-frequency events

## Docker Support

Create a `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
```

Create `requirements.txt`:
```
flask==2.3.3
prometheus_client==0.17.1
```

Build and run:
```bash
docker build -t monitoring-test .
docker run -p 8000:8000 monitoring-test
```

## Monitoring Stack Integration

### Grafana Dashboard

This application works well with Grafana for visualization:

1. Add Prometheus as a data source
2. Create dashboards with panels for:
   - Request rate over time
   - Latency percentiles
   - Error rates
   - Active requests

### Alerting

Set up alerts in Prometheus/Alertmanager:

```yaml
groups:
  - name: flask-app
    rules:
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(app_request_latency_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
```

## Development

### Adding New Metrics

1. **Import the metric type**:
   ```python
   from prometheus_client import Counter, Gauge, Histogram, Summary
   ```

2. **Define the metric**:
   ```python
   NEW_METRIC = Counter('app_new_metric_total', 'Description', ['label1', 'label2'])
   ```

3. **Instrument your code**:
   ```python
   NEW_METRIC.labels(label1='value1', label2='value2').inc()
   ```

### Extending the Application

Consider adding:
- Database connection metrics
- External API call metrics
- Business logic metrics
- Custom health checks
- Error rate tracking

## Troubleshooting

### Common Issues

1. **Metrics not appearing**:
   - Verify `/metrics` endpoint is accessible
   - Check Prometheus configuration
   - Ensure metrics are being incremented

2. **High memory usage**:
   - Review metric cardinality
   - Implement metric cleanup for dynamic labels
   - Monitor label explosion

3. **Performance impact**:
   - Metrics collection is generally lightweight
   - Consider sampling for high-frequency operations
   - Monitor application performance before/after instrumentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
- [Grafana Documentation](https://grafana.com/docs/)
- [Monitoring Best Practices](https://prometheus.io/docs/practices/naming/)

## Author

Created by [timthoithi100](https://github.com/timthoithi100)

---

For questions or support, please open an issue in the [GitHub repository](https://github.com/timthoithi100/monitoring-test/issues).
# API Performance Monitor

## Overview

API Performance Monitor is a lightweight Python-based system for tracking and analyzing API performance metrics. It enables you to monitor response times, detect API errors, and generate actionable performance insights. The system integrates seamlessly with Grafana for real-time visualization.

## Features

- **Automated API Monitoring:** Periodically checks configured API endpoints.
- **Performance Metrics:** Captures response times, status codes, and error details.
- **Persistent Storage:** Stores all metrics in a local SQLite database.
- **RESTful API:** Exposes endpoints for metrics retrieval and summary statistics.
- **Grafana Integration:** Visualize metrics and trends using Grafana dashboards.

## Technology Stack

- Python (Flask, Requests)
- SQLite
- Grafana

## Getting Started

### 1. Install Dependencies

```sh
pip install -r requirements.txt
```

### 2. Start the Flask API Server

```sh
python app.py
```

### 3. Configure Endpoints to Monitor

- Open `collector.py` and add your target API URLs to the `API_ENDPOINTS` list.

### 4. Start the Metrics Collector

```sh
python collector.py
```

### 5. Integrate with Grafana

- Add a new data source in Grafana using the "SimpleJSON" or "JSON API" plugin.
- Set the URL to `http://localhost:5000/metrics`.
- Build dashboards using the `/metrics` and `/metrics/summary` endpoints for detailed insights.

## API Endpoints

- `GET /`  
  Health check and welcome message.
- `POST /metrics`  
  Submit a new API performance metric.
- `GET /metrics`  
  Retrieve stored metrics (supports filtering and limiting).
- `GET /metrics/summary`  
  Get aggregated statistics per endpoint.

## Best Practices

- For production deployments, use a WSGI server (e.g., Gunicorn) and ensure persistent storage for SQLite.
- Adjust the monitoring interval and endpoints in `collector.py` as needed for your use case.
- Secure the API endpoints if deploying in a public or sensitive environment.

## License

This project is provided for educational and internal monitoring purposes.

## Contact

For questions or contributions, please open an issue or pull request on the repository.
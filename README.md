# GPU AI Ops Lab

Local laboratory to simulate NVIDIA GPU infrastructure observability.

## Components

- NVIDIA GPU simulator written in Python
- Prometheus for metrics collection
- Grafana for dashboards and alerting

## Architecture

```text
NVIDIA Simulator
      ↓
Prometheus
      ↓
Grafana
      ↓
Alert Webhook
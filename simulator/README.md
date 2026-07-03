# GPU AI Ops Lab

GPU AI Ops Lab is a simulated NVIDIA GPU infrastructure designed to reproduce realistic operational scenarios for observability, event processing and AI-driven operations.

It is part of a modular AIOps platform composed of three independent projects:

```
GPU AI Ops Lab
        │
        ▼
AI Event Processor
        │
        ▼
AI Operations Engine
```

The lab continuously generates infrastructure telemetry and operational events that can be consumed by monitoring systems, event processors and AI agents.

---

## Purpose

The objective of this project is to provide a realistic playground for experimenting with:

- NVIDIA GPU infrastructure monitoring
- Prometheus metrics
- Grafana dashboards
- Operational event generation
- Event normalization
- AI-assisted incident analysis
- Root cause analysis
- Automated remediation
- AIOps workflows

Unlike a simple metrics simulator, this laboratory reproduces realistic infrastructure behaviour that can be used to validate complete AI Operations pipelines.

---

## AIOps Platform

This repository belongs to the following ecosystem:

| Repository | Purpose |
|------------|---------|
| GPU AI Ops Lab | Simulates GPU infrastructure, telemetry and incidents |
| AI Event Processor | Normalizes, enriches and correlates operational events |
| AI Operations Engine | Performs AI reasoning, decision making and remediation planning |

Each repository has a single responsibility, allowing every component to evolve independently.

---

## Features

### Infrastructure Simulation

- Multiple DGX nodes
- NVIDIA GPUs
- Rack health
- CDU health
- Power consumption
- GPU utilization
- GPU temperatures
- GPU memory
- Cluster topology

### Observability

- Prometheus exporter
- Grafana dashboards
- Historical metrics
- Infrastructure state

### Event Simulation

- GPU overheating
- ECC errors
- Cooling failures
- Power anomalies
- Future InfiniBand failures
- Future storage incidents

### AI Integration

Designed to integrate with:

- AI Event Processor
- AI Operations Engine

---

## Repository Structure

```
gpu-ai-ops-lab/

├── simulator/
├── scenarios/
├── topology/
├── monitoring/
├── docs/
├── data/
└── docker-compose.yml
```

---

## Requirements

- Python 3.13+
- pip

---

## Installation

Clone the repository:

```bash
git clone https://github.com/raullencinaherrera/gpu-ai-ops-lab.git
cd gpu-ai-ops-lab/simulator
```

Create a virtual environment:

```powershell
py -3.13 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

## Run

```powershell
python app.py
```

The simulator starts on:

```
http://localhost:8000
```

Metrics endpoint:

```
http://localhost:8000/metrics
```

---

## Prometheus

Example configuration:

```yaml
scrape_configs:
  - job_name: gpu-ai-ops-lab

    static_configs:
      - targets:
          - host.docker.internal:8000
```

Example queries:

```promql
nvidia_gpu_temperature_celsius

max(nvidia_gpu_temperature_celsius)

avg(nvidia_gpu_power_watts)
```

---

## Roadmap

Current development focuses on building a complete Digital Twin of an NVIDIA GPU infrastructure.

Planned capabilities include:

- Dynamic cluster topology
- Scenario engine
- Chaos engineering
- Historical event replay
- Predictive failures
- AI-driven recommendations
- Rundeck integration
- Autonomous remediation
- Kubernetes deployment

---

## License

MIT
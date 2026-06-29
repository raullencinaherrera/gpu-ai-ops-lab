# NVIDIA GPU Simulator

Python application that simulates an NVIDIA DGX infrastructure and exposes Prometheus metrics.

## Features

- Simulates multiple DGX nodes
- Simulates GPU temperatures
- Simulates GPU utilization
- Simulates GPU memory usage
- Simulates power consumption
- Simulates rack and CDU health
- Exposes metrics in Prometheus format

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

The simulator will start on:

```
http://localhost:8000
```

Metrics endpoint:

```
http://localhost:8000/metrics
```

---

## Example metrics

- nvidia_gpu_temperature_celsius
- nvidia_gpu_utilization_percent
- nvidia_gpu_memory_used_mb
- nvidia_gpu_power_watts
- nvidia_gpu_health_status
- nvidia_cdu_health_status
- nvidia_rack_temperature_celsius

---

## Connect to Prometheus

Configure your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: "nvidia-simulator"
    static_configs:
      - targets:
          - host.docker.internal:8000
```

Then query metrics such as:

```promql
nvidia_gpu_temperature_celsius
```

or

```promql
max(nvidia_gpu_temperature_celsius)
```
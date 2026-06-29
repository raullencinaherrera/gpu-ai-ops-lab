import random
import time
from dataclasses import dataclass, field
from prometheus_client import Gauge, start_http_server


GPU_TEMP = Gauge(
    "nvidia_gpu_temperature_celsius",
    "Simulated NVIDIA GPU temperature",
    ["site", "rack", "node", "gpu"]
)

GPU_UTIL = Gauge(
    "nvidia_gpu_utilization_percent",
    "Simulated NVIDIA GPU utilization",
    ["site", "rack", "node", "gpu"]
)

GPU_MEMORY = Gauge(
    "nvidia_gpu_memory_used_mb",
    "Simulated NVIDIA GPU memory used",
    ["site", "rack", "node", "gpu"]
)

GPU_POWER = Gauge(
    "nvidia_gpu_power_watts",
    "Simulated NVIDIA GPU power consumption",
    ["site", "rack", "node", "gpu"]
)

GPU_HEALTH = Gauge(
    "nvidia_gpu_health_status",
    "Simulated NVIDIA GPU health: 1 healthy, 0 unhealthy",
    ["site", "rack", "node", "gpu"]
)

CDU_HEALTH = Gauge(
    "nvidia_cdu_health_status",
    "Simulated CDU health: 1 healthy, 0 unhealthy",
    ["site", "rack", "cdu"]
)

RACK_TEMP = Gauge(
    "nvidia_rack_temperature_celsius",
    "Simulated rack ambient temperature",
    ["site", "rack"]
)


@dataclass
class GPU:
    gpu_id: str
    temperature: float = 45.0
    utilization: float = 20.0
    memory_used_mb: float = 4000.0
    power_watts: float = 120.0
    healthy: bool = True

    def update(self, cooling_degraded: bool):
        self.utilization = random.uniform(20, 95)
        self.memory_used_mb = random.uniform(4000, 75000)
        self.power_watts = 100 + (self.utilization * 6)

        base_temp = 38 + (self.utilization * 0.45)

        if cooling_degraded:
            base_temp += random.uniform(12, 22)

        self.temperature = base_temp + random.uniform(-3, 3)

        if self.temperature > 92:
            self.healthy = False
        else:
            self.healthy = True


@dataclass
class DGXNode:
    name: str
    gpus: list[GPU] = field(default_factory=list)

    def update(self, cooling_degraded: bool):
        for gpu in self.gpus:
            gpu.update(cooling_degraded=cooling_degraded)


@dataclass
class CDU:
    name: str
    healthy: bool = True

    def update(self):
        # Fallo ocasional de refrigeración
        if random.random() < 0.03:
            self.healthy = False

        # Recuperación ocasional
        if not self.healthy and random.random() < 0.15:
            self.healthy = True


@dataclass
class Rack:
    name: str
    cdu: CDU
    nodes: list[DGXNode]
    ambient_temperature: float = 22.0

    def update(self):
        self.cdu.update()

        cooling_degraded = not self.cdu.healthy

        if cooling_degraded:
            self.ambient_temperature = random.uniform(32, 42)
        else:
            self.ambient_temperature = random.uniform(20, 26)

        for node in self.nodes:
            node.update(cooling_degraded=cooling_degraded)


@dataclass
class Site:
    name: str
    racks: list[Rack]

    def update(self):
        for rack in self.racks:
            rack.update()

    def export_metrics(self):
        for rack in self.racks:
            CDU_HEALTH.labels(
                site=self.name,
                rack=rack.name,
                cdu=rack.cdu.name
            ).set(1 if rack.cdu.healthy else 0)

            RACK_TEMP.labels(
                site=self.name,
                rack=rack.name
            ).set(rack.ambient_temperature)

            for node in rack.nodes:
                for gpu in node.gpus:
                    labels = {
                        "site": self.name,
                        "rack": rack.name,
                        "node": node.name,
                        "gpu": gpu.gpu_id,
                    }

                    GPU_TEMP.labels(**labels).set(gpu.temperature)
                    GPU_UTIL.labels(**labels).set(gpu.utilization)
                    GPU_MEMORY.labels(**labels).set(gpu.memory_used_mb)
                    GPU_POWER.labels(**labels).set(gpu.power_watts)
                    GPU_HEALTH.labels(**labels).set(1 if gpu.healthy else 0)


def build_lab_site() -> Site:
    rack_a01 = Rack(
        name="rack-a01",
        cdu=CDU(name="cdu-a01"),
        nodes=[
            DGXNode(
                name="dgx-01",
                gpus=[GPU(gpu_id=f"gpu-{i}") for i in range(8)]
            ),
            DGXNode(
                name="dgx-02",
                gpus=[GPU(gpu_id=f"gpu-{i}") for i in range(8)]
            ),
        ]
    )

    rack_a02 = Rack(
        name="rack-a02",
        cdu=CDU(name="cdu-a02"),
        nodes=[
            DGXNode(
                name="dgx-03",
                gpus=[GPU(gpu_id=f"gpu-{i}") for i in range(8)]
            ),
            DGXNode(
                name="dgx-04",
                gpus=[GPU(gpu_id=f"gpu-{i}") for i in range(8)]
            ),
        ]
    )

    return Site(
        name="sv11",
        racks=[rack_a01, rack_a02]
    )


if __name__ == "__main__":
    print("Starting NVIDIA GPU digital twin simulator on port 8000...")

    site = build_lab_site()
    start_http_server(8000)

    while True:
        site.update()
        site.export_metrics()
        time.sleep(5)
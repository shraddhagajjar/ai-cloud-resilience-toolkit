from dataclasses import dataclass

@dataclass
class ToolkitConfig:
    cpu_high_threshold: float = 0.85
    mem_high_threshold: float = 0.85
    anomaly_score_threshold: float = 0.60

    min_replicas: int = 2
    max_replicas: int = 20
    scale_up_step: int = 2
    scale_down_step: int = 1

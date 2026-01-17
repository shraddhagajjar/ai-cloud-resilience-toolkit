from dataclasses import dataclass

@dataclass
class ScalingDecision:
    current_replicas: int
    recommended_replicas: int
    reason: str

class AutoScaler:
    """
    Simple autoscaling policy driven by utilization + anomaly score.
    Keeps logic intentionally transparent for auditability.
    """

    def __init__(self, config):
        self.cfg = config

    def recommend(self, cpu: float, mem: float, anomaly_score: float, current_replicas: int) -> ScalingDecision:
        scale_up = (
            cpu >= self.cfg.cpu_high_threshold
            or mem >= self.cfg.mem_high_threshold
            or anomaly_score >= self.cfg.anomaly_score_threshold
        )

        scale_down = (cpu < 0.40) and (mem < 0.40) and (anomaly_score < 0.30)

        if scale_up:
            target = min(self.cfg.max_replicas, current_replicas + self.cfg.scale_up_step)
            reason = "Scale up: high utilization and/or elevated anomaly score."
        elif scale_down:
            target = max(self.cfg.min_replicas, current_replicas - self.cfg.scale_down_step)
            reason = "Scale down: sustained low utilization and low anomaly score."
        else:
            target = current_replicas
            reason = "Hold: metrics within normal range."

        return ScalingDecision(
            current_replicas=current_replicas,
            recommended_replicas=target,
            reason=reason
        )

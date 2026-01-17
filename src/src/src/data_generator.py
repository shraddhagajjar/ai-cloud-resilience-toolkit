import numpy as np
import pandas as pd

def generate_synthetic_metrics(n: int = 500, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic cloud infrastructure metrics for experimentation
    and algorithm validation purposes.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n)

    cpu = np.clip(rng.normal(0.55, 0.12, n), 0, 1)
    mem = np.clip(rng.normal(0.50, 0.15, n), 0, 1)
    latency = np.clip(rng.normal(120, 25, n), 30, 500)
    error_rate = np.clip(rng.normal(0.01, 0.01, n), 0, 0.3)
    rps = np.clip(rng.normal(800, 180, n), 50, 3000)

    # Inject controlled anomaly windows
    for start in [120, 260, 410]:
        end = min(start + 20, n)
        cpu[start:end] = np.clip(cpu[start:end] + 0.35, 0, 1)
        latency[start:end] += 180
        error_rate[start:end] += 0.06

    return pd.DataFrame({
        "timestamp": t,
        "cpu": cpu,
        "mem": mem,
        "latency_ms": latency,
        "error_rate": error_rate,
        "req_per_sec": rps
    })

import pandas as pd
from .anomaly_detector import AnomalyDetector
from .autoscaler import AutoScaler
from .config import ToolkitConfig

FEATURES = ["cpu", "mem", "latency_ms", "error_rate", "req_per_sec"]

def run_pipeline(
    df: pd.DataFrame,
    config: ToolkitConfig,
    start_replicas: int = 4
) -> pd.DataFrame:
    """
    Runs end-to-end analysis:
    1) Fit anomaly model
    2) Score each time step with anomaly_score
    3) Recommend replica count over time
    """
    detector = AnomalyDetector()
    detector.fit(df, FEATURES)

    df = df.copy()
    df["anomaly_score"] = detector.score(df, FEATURES)

    scaler = AutoScaler(config)

    replicas = start_replicas
    recommended = []
    reasons = []

    for _, row in df.iterrows():
        decision = scaler.recommend(
            cpu=float(row["cpu"]),
            mem=float(row["mem"]),
            anomaly_score=float(row["anomaly_score"]),
            current_replicas=int(replicas)
        )
        replicas = decision.recommended_replicas
        recommended.append(replicas)
        reasons.append(decision.reason)

    df["recommended_replicas"] = recommended
    df["decision_reason"] = reasons

    return df

import pandas as pd
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    """
    IsolationForest-based anomaly detection for cloud telemetry.
    Produces anomaly_score in [0,1], where higher = more anomalous.
    """

    def __init__(self, random_state: int = 42, contamination: float = 0.05):
        self.model = IsolationForest(
            n_estimators=200,
            contamination=contamination,
            random_state=random_state
        )
        self._fitted = False

    def fit(self, df: pd.DataFrame, features: list[str]) -> None:
        self.model.fit(df[features])
        self._fitted = True

    def score(self, df: pd.DataFrame, features: list[str]) -> pd.Series:
        if not self._fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")

        # higher decision_function = more normal
        normality = self.model.decision_function(df[features])

        # convert to anomaly score in [0,1]
        s = (normality.max() - normality) / (normality.max() - normality.min() + 1e-9)
        return s.clip(0, 1)

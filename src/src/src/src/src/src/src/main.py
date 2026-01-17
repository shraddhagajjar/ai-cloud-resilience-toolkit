from src.config import ToolkitConfig
from src.data_generator import generate_synthetic_metrics
from src.pipeline import run_pipeline

def main():
    cfg = ToolkitConfig()

    df = generate_synthetic_metrics(n=500, seed=42)
    result = run_pipeline(df, cfg, start_replicas=4)

    result.to_csv("demo_output.csv", index=False)
    print("Demo completed ✅ Output saved to demo_output.csv")

if __name__ == "__main__":
    main()

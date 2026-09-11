import pandas as pd
from esg.scoring import compute_scores
from esg.dashboard import build_dashboard

if __name__ == "__main__":
    df = pd.read_csv("data/esg_metrics.csv")
    scored = compute_scores(df)
    print(scored[["year", "env_score", "social_score", "governance_score", "esg_composite_score"]])
    build_dashboard(scored)

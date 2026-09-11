"""ESG Scoring Engine
Converts raw sustainability metrics into normalized 0-100 pillar scores
and a weighted composite ESG score.
"""
import pandas as pd


def _normalize(series: pd.Series, lower_is_better: bool = False) -> pd.Series:
    """Min-max normalize a column to 0-100."""
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([100] * len(series), index=series.index)
    norm = (series - lo) / (hi - lo) * 100
    return (100 - norm) if lower_is_better else norm


def compute_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Environmental: lower emissions/energy/water is better, higher recycling is better
    df["env_score"] = (
        _normalize(df["carbon_emissions_tons"], lower_is_better=True) * 0.4
        + _normalize(df["energy_use_mwh"], lower_is_better=True) * 0.3
        + _normalize(df["waste_recycled_pct"]) * 0.15
        + _normalize(df["water_usage_kl"], lower_is_better=True) * 0.15
    )

    # Social: higher diversity/community spend is better, fewer incidents is better
    df["social_score"] = (
        _normalize(df["diversity_ratio_pct"]) * 0.4
        + _normalize(df["safety_incidents"], lower_is_better=True) * 0.3
        + _normalize(df["community_spend_inr_lakh"]) * 0.3
    )

    # Governance: higher independence/compliance is better, fewer privacy incidents is better
    df["governance_score"] = (
        _normalize(df["board_independence_pct"]) * 0.35
        + _normalize(df["audit_compliance_pct"]) * 0.35
        + _normalize(df["data_privacy_incidents"], lower_is_better=True) * 0.3
    )

    # Composite (E 40%, S 30%, G 30% — matches README weighting)
    df["esg_composite_score"] = (
        df["env_score"] * 0.4 + df["social_score"] * 0.3 + df["governance_score"] * 0.3
    ).round(1)

    for col in ["env_score", "social_score", "governance_score"]:
        df[col] = df[col].round(1)

    return df

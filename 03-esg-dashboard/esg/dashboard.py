"""Generates an interactive HTML ESG dashboard using Plotly."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def build_dashboard(df: pd.DataFrame, output_path: str = "dashboard.html"):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "ESG Composite Score Over Time",
            "E / S / G Pillar Scores (Latest Year)",
            "Carbon Emissions Trend",
            "Waste Recycled %",
        ),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "bar"}]],
    )

    fig.add_trace(
        go.Scatter(x=df["year"], y=df["esg_composite_score"],
                   mode="lines+markers", name="ESG Score"),
        row=1, col=1,
    )

    latest = df.iloc[-1]
    fig.add_trace(
        go.Bar(x=["Environmental", "Social", "Governance"],
               y=[latest["env_score"], latest["social_score"], latest["governance_score"]],
               marker_color=["#2e7d32", "#1565c0", "#6a1b9a"], name="Pillar Scores"),
        row=1, col=2,
    )

    fig.add_trace(
        go.Scatter(x=df["year"], y=df["carbon_emissions_tons"],
                   mode="lines+markers", name="Emissions (tons)", line=dict(color="firebrick")),
        row=2, col=1,
    )

    fig.add_trace(
        go.Bar(x=df["year"], y=df["waste_recycled_pct"], name="Waste Recycled %",
               marker_color="seagreen"),
        row=2, col=2,
    )

    fig.update_layout(
        title_text=f"ESG Compliance Dashboard — Composite Score: {latest['esg_composite_score']}/100",
        height=700, showlegend=False,
    )

    fig.write_html(output_path)
    print(f"[Dashboard] Saved to {output_path}")
    return output_path

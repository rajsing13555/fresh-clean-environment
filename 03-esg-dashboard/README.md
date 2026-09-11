# 🌍 AI-Powered ESG/Sustainability Data Dashboard

Collects a company's carbon footprint, resource usage, and supply-chain
data, then automatically computes an ESG (Environmental, Social,
Governance) compliance score and renders it as a dashboard.

## Why this matters through 2030
ESG reporting is becoming mandatory across India and globally
(SEBI's BRSR framework, EU CSRD, etc.) between 2025–2030. Companies
will need tooling to automate this reporting — creating a large,
durable job/product market.

## Features
- **Data Ingestion** – load ESG metrics from CSV (emissions, energy,
  diversity, governance indicators)
- **Scoring Engine** – weighted scoring model producing E, S, G, and
  overall composite scores (0–100)
- **Dashboard** – interactive HTML dashboard (Plotly) with trend charts
  and a compliance scorecard
- **Report Export** – generates a shareable Markdown/HTML summary

## Tech Stack
- Python 3.10+
- `pandas` for data processing
- `plotly` for interactive charts
- Plain HTML/CSS for the dashboard shell

## Project Structure
```
03-esg-dashboard/
├── data/
│   └── esg_metrics.csv
├── esg/
│   ├── __init__.py
│   ├── scoring.py
│   └── dashboard.py
├── main.py
├── requirements.txt
└── README.md
```

## Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
# Opens/generates dashboard.html
```

## Scoring Methodology (customizable in esg/scoring.py)
| Pillar | Metrics | Weight |
|---|---|---|
| Environmental | Carbon emissions, energy use, waste, water | 40% |
| Social | Diversity ratio, employee safety, community spend | 30% |
| Governance | Board independence, audit compliance, data privacy incidents | 30% |

## Roadmap / How to extend
- [ ] Connect to real IoT/utility data feeds for live emissions data
- [ ] Map scoring to actual regulatory frameworks (BRSR, CSRD, GRI)
- [ ] Add year-over-year trend forecasting
- [ ] Add PDF export for board/regulator-ready reports

## License
MIT

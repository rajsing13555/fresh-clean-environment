# 🔒 Privacy-Preserving Analytics Tool (Federated Learning)

A simulation of Federated Learning where multiple data-holding
"clients" (e.g. hospitals, banks, branches) train a shared model
**without ever sharing raw data** — only model updates are exchanged
and aggregated centrally.

## Why this matters through 2030
Data privacy laws (India's DPDP Act, GDPR, HIPAA, etc.) are getting
stricter every year. Companies handling sensitive data (healthcare,
finance) increasingly need analytics that never move raw data
off-premise — federated learning is the standard technique for this,
and demand for it will only grow.

## Features
- **Simulated multi-client setup** – N clients, each with a private
  local dataset (never shared)
- **Local Training** – each client trains a small model on its own
  data
- **Federated Averaging (FedAvg)** – server aggregates model *weights*
  (not data) across clients each round
- **Privacy check** – demonstrates that raw data never leaves each
  client's boundary

## Tech Stack
- Python 3.10+
- `numpy` (simple linear model — dependency-free, easy to read)
- Architecture is directly extensible to PyTorch + Flower/PySyft

## Project Structure
```
04-federated-privacy-analytics/
├── federated/
│   ├── __init__.py
│   ├── client.py
│   ├── server.py
│   └── data_simulator.py
├── main.py
├── requirements.txt
└── README.md
```

## Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## How It Works
1. `data_simulator.py` creates N clients, each with its own private
   slice of data (simulating hospitals/banks/branches).
2. Each `client.py` trains a local linear regression model on its own
   data only.
3. `server.py` collects only the **model weights** from each client
   and averages them (FedAvg) — raw data is never transmitted.
4. The averaged global model is sent back to clients for the next round.

## Roadmap / How to extend
- [ ] Swap the toy linear model for a PyTorch neural net
- [ ] Add differential privacy noise to client updates
- [ ] Use a real framework: Flower (`flwr`) or NVIDIA FLARE
- [ ] Add secure aggregation (so even the server can't see individual updates)

## License
MIT

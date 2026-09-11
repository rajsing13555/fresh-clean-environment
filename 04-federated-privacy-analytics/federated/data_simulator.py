"""Simulates multiple private data-holders (e.g. hospitals/bank branches).
Each client's data NEVER leaves its own object.
"""
import numpy as np


def generate_client_data(n_clients: int = 4, samples_per_client: int = 200, seed: int = 42):
    """Generate synthetic private datasets for a linear relationship
    y = 3x1 - 2x2 + 5 + noise, with slightly different noise/offset per client
    (simulating real-world data heterogeneity across institutions).
    """
    rng = np.random.default_rng(seed)
    client_datasets = []
    for i in range(n_clients):
        X = rng.normal(loc=0, scale=1, size=(samples_per_client, 2))
        noise = rng.normal(loc=i * 0.2, scale=0.5, size=samples_per_client)  # heterogeneity
        y = 3 * X[:, 0] - 2 * X[:, 1] + 5 + noise
        client_datasets.append({"client_id": f"client_{i}", "X": X, "y": y})
    return client_datasets

"""Federated Learning Server
Aggregates client model weights using Federated Averaging (FedAvg).
Never sees any client's raw data.
"""
import numpy as np


class FederatedServer:
    def __init__(self, n_features: int):
        self.global_weights = np.zeros(n_features)
        self.global_bias = 0.0

    def aggregate(self, client_updates: list[tuple]):
        """client_updates: list of (weights, bias, n_samples)
        Weighted average by number of local samples (standard FedAvg).
        """
        total_samples = sum(n for _, _, n in client_updates)
        new_weights = np.zeros_like(self.global_weights)
        new_bias = 0.0
        for weights, bias, n in client_updates:
            frac = n / total_samples
            new_weights += weights * frac
            new_bias += bias * frac
        self.global_weights = new_weights
        self.global_bias = new_bias
        return self.global_weights, self.global_bias

    def get_global_model(self):
        return self.global_weights, self.global_bias

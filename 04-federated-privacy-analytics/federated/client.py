"""Federated Learning Client
Trains a local linear regression model on private data.
Only `get_weights()` ever leaves this object — `X` and `y` do not.
"""
import numpy as np


class FederatedClient:
    def __init__(self, client_id: str, X: np.ndarray, y: np.ndarray):
        self.client_id = client_id
        self._X = X          # PRIVATE — never exposed outside this class
        self._y = y          # PRIVATE — never exposed outside this class
        n_features = X.shape[1]
        self.weights = np.zeros(n_features)
        self.bias = 0.0

    def set_weights(self, weights: np.ndarray, bias: float):
        """Receive global model from the server to start a new round."""
        self.weights = weights.copy()
        self.bias = bias

    def local_train(self, epochs: int = 20, lr: float = 0.05):
        """Train locally using gradient descent. Data never leaves this method."""
        n = len(self._y)
        for _ in range(epochs):
            preds = self._X @ self.weights + self.bias
            error = preds - self._y
            grad_w = (2 / n) * (self._X.T @ error)
            grad_b = (2 / n) * np.sum(error)
            self.weights -= lr * grad_w
            self.bias -= lr * grad_b

    def get_weights(self):
        """Only this — weights & bias — is ever shared. No raw data."""
        return self.weights.copy(), self.bias, len(self._y)

import numpy as np
from federated.data_simulator import generate_client_data
from federated.client import FederatedClient
from federated.server import FederatedServer

N_CLIENTS = 4
ROUNDS = 10

if __name__ == "__main__":
    print(f"Simulating {N_CLIENTS} private data-holders (e.g. hospital branches)...")
    datasets = generate_client_data(n_clients=N_CLIENTS)

    clients = [FederatedClient(d["client_id"], d["X"], d["y"]) for d in datasets]
    server = FederatedServer(n_features=2)

    print("\nStarting Federated Learning (raw data never leaves each client)...\n")
    for r in range(1, ROUNDS + 1):
        # 1. Server sends current global model to each client
        gw, gb = server.get_global_model()
        for c in clients:
            c.set_weights(gw, gb)
            c.local_train(epochs=20, lr=0.05)  # local training on PRIVATE data

        # 2. Server collects ONLY weights (no data) and aggregates
        updates = [c.get_weights() for c in clients]
        gw, gb = server.aggregate(updates)

        print(f"Round {r:2d} | Global weights: {np.round(gw, 3)} | bias: {gb:.3f}")

    print("\nTrue underlying relationship: y = 3*x1 - 2*x2 + 5")
    print(f"Learned via FedAvg (no raw data ever shared): "
          f"y ≈ {gw[0]:.2f}*x1 + {gw[1]:.2f}*x2 + {gb:.2f}")

"""Inventory Agent
Monitors stock levels and autonomously generates reorder actions
whenever stock falls below the configured threshold.
"""
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "inventory.csv"


class InventoryAgent:
    def __init__(self, data_path: Path = DATA_PATH):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)

    def check_stock(self) -> pd.DataFrame:
        """Return rows that need reordering."""
        return self.df[self.df["current_stock"] < self.df["reorder_threshold"]]

    def generate_purchase_orders(self) -> list[dict]:
        """Autonomously build purchase-order objects for low-stock items."""
        low_stock = self.check_stock()
        orders = []
        for _, row in low_stock.iterrows():
            orders.append(
                {
                    "sku": row["sku"],
                    "product_name": row["product_name"],
                    "order_qty": int(row["reorder_qty"]),
                    "supplier": row["supplier"],
                    "reason": f"Stock ({row['current_stock']}) below threshold "
                              f"({row['reorder_threshold']})",
                }
            )
        return orders

    def run(self) -> list[dict]:
        orders = self.generate_purchase_orders()
        for o in orders:
            print(f"[InventoryAgent] Auto-drafted PO -> {o['order_qty']}x "
                  f"{o['product_name']} from {o['supplier']} "
                  f"({o['reason']})")
        return orders


if __name__ == "__main__":
    InventoryAgent().run()

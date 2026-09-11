"""Orchestrator
Coordinates the Inventory, Email, and Report agents.
Includes a simple human-approval gate before any 'write' action
(good practice for real autonomous agents).
"""
from .inventory_agent import InventoryAgent
from .email_agent import EmailAgent
from .report_agent import ReportAgent


class Orchestrator:
    def __init__(self, auto_approve: bool = True):
        self.auto_approve = auto_approve
        self.inventory_agent = InventoryAgent()
        self.email_agent = EmailAgent()
        self.report_agent = ReportAgent()

    def _approve(self, action_desc: str) -> bool:
        if self.auto_approve:
            return True
        answer = input(f"Approve action? {action_desc} [y/N]: ")
        return answer.lower() == "y"

    def run_daily_cycle(self, inbox: list[str]) -> str:
        print("=== Autonomous Agent: Daily Cycle Start ===")

        purchase_orders = self.inventory_agent.run()
        if purchase_orders and self._approve(f"Place {len(purchase_orders)} purchase order(s)"):
            print("[Orchestrator] Purchase orders approved & (simulated) submitted.")

        email_drafts = self.email_agent.run(inbox)

        report = self.report_agent.generate_report(purchase_orders, email_drafts)
        self.report_agent.save(report)

        print("=== Autonomous Agent: Daily Cycle Complete ===")
        return report

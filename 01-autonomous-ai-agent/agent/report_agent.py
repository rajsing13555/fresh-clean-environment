"""Report Agent
Aggregates operational data and auto-generates a summary report.
"""
from datetime import date


class ReportAgent:
    def generate_report(self, purchase_orders: list[dict], email_drafts: list[dict]) -> str:
        lines = [
            f"# Daily Operations Report — {date.today().isoformat()}",
            "",
            "## Inventory: Auto-Generated Purchase Orders",
        ]
        if purchase_orders:
            for po in purchase_orders:
                lines.append(
                    f"- {po['order_qty']}x **{po['product_name']}** "
                    f"from {po['supplier']} — _{po['reason']}_"
                )
        else:
            lines.append("- No reorders needed today.")

        lines.append("")
        lines.append("## Customer Support: Drafted Replies")
        if email_drafts:
            for d in email_drafts:
                lines.append(f"- Incoming: {d['incoming'][:60]}...")
        else:
            lines.append("- No pending emails.")

        report = "\n".join(lines)
        print("[ReportAgent] Report generated.")
        return report

    def save(self, report: str, path: str = "daily_report.md"):
        with open(path, "w") as f:
            f.write(report)
        print(f"[ReportAgent] Saved to {path}")


if __name__ == "__main__":
    agent = ReportAgent()
    r = agent.generate_report([], [])
    print(r)

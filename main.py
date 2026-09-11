from agent.orchestrator import Orchestrator

if __name__ == "__main__":
    sample_inbox = [
        "Hi, my order #1234 hasn't arrived yet, it's been 2 weeks. Can you help?",
        "Do you offer bulk discounts for orders over 100 units?",
    ]
    orchestrator = Orchestrator(auto_approve=True)
    report = orchestrator.run_daily_cycle(sample_inbox)
    print("\n" + report)

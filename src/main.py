
from pathlib import Path
from datetime import datetime

from mock_llm import mock_llm_call
from agents import build_agents
from supervisor import run_supervisor


def refund_tool(call_text: str) -> str:
    # fake tool action (for demo purposes)
    return "Refund tool simulated: would process refund after verifying order details."

def callback_tool(call_text: str) -> str:
    return "Callback tool simulated: would schedule a support callback."

TOOLS = {
    "refund": refund_tool,
    "schedule_callback": callback_tool,
}

KB = """
Refund Policy (Demo):
- Refunds allowed within 14 days of purchase if item unused.
- Digital services are refundable only if not activated.
- For damaged items, request must include photo evidence.
"""

SCENARIOS = [
    "Hi, I want a refund. I was charged twice for my subscription.",
    "My order arrived damaged and I need a replacement. What do I do?",
    "I can’t log into my account and the reset link is not working."
]


def main():
    agents = build_agents(mock_llm_call)

    out_dir = Path("transcripts")
    out_dir.mkdir(exist_ok=True)

    for i, user_msg in enumerate(SCENARIOS, 1):
        state = {
            "user_message": user_msg,
            "kb": KB,
        }

        transcript = run_supervisor(state, agents, TOOLS)

        fp = out_dir / f"transcript_{i}.txt"
        fp.write_text(transcript, encoding="utf-8")
        print("\n" + "=" * 60)
        print(transcript)
        print(f"Saved -> {fp}")

if __name__ == "__main__":
    main()

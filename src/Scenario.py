from agents import build_agents
from mock_llm import mock_llm_call
from supervisor import run_supervisor

from pathlib import Path

def refund_tool(call_text: str) -> str:
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


def run_scenario():
    agents = build_agents(mock_llm_call)

    print("=== Customer Care Scenario ===")
    print("Type your issue. Type 'exit' to stop.\n")

    while True:
        user_msg = input("User ; ")

        if user_msg.lower() in ["exit", "quit"]:
            print("Agent ; Thank you for contacting support. Goodbye!")
            break

        state = {
            "user_message": user_msg,
            "kb": KB,
        }

        transcript = run_supervisor(state, agents, TOOLS)

        print("\nAgent ;")
        print(state.get("final_response", transcript))
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    run_scenario()

#python src/Scenario.py
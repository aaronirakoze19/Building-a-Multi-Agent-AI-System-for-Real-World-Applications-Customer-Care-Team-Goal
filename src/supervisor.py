
from typing import Dict, Any

State = Dict[str, Any]


def _parse_intent(text: str) -> str:
    t = (text or "").strip()
    if "Refund/Billing" in t:
        return "Refund/Billing"
    if "Shipping/Damage" in t:
        return "Shipping/Damage"
    if "Account/Login" in t:
        return "Account/Login"
    return "General Inquiry"


def _extract_tool_call(resolver_text: str):
    """
    Very small parser:
    Looks for lines:
      TOOL: refund
      TOOL_INPUT: ...
    """
    tool = None
    tool_input = ""
    for line in (resolver_text or "").splitlines():
        line = line.strip()
        if line.upper().startswith("TOOL:"):
            tool = line.split(":", 1)[1].strip()
        elif line.upper().startswith("TOOL_INPUT:"):
            tool_input = line.split(":", 1)[1].strip()
    return tool, tool_input


def run_supervisor(state: State, agents: dict, tools: dict) -> str:
    """
    Orchestration logic (supervisor):
    Greeter -> Researcher -> Empath -> Resolver -> (optional tool) -> QA -> Final
    Includes shared state updates and human handoff when needed.
    """
    transcript = []
    state.setdefault("actions", [])
    state.setdefault("handoff", False)

    user_msg = state.get("user_message", "")

    transcript.append("=== USER ===")
    transcript.append(user_msg)

    # Greeter / Intent
    greeter_out = agents["greeter"].run(state)
    intent = _parse_intent(greeter_out)
    state["intent"] = intent

    transcript.append("\n--- Greeter Output (Greeter / Intent Classifier) ---")
    transcript.append(f"Intent: {intent}")

    # Researcher (policy / KB)
    researcher_out = agents["researcher"].run(state)
    state["policy_snippet"] = researcher_out

    transcript.append("\n--- Researcher Output (Knowledge Retriever) ---")
    transcript.append(researcher_out)

    # Empath
    empath_out = agents["empath"].run(state)
    state["empathy_line"] = empath_out

    transcript.append("\n--- Empath Output (Tone Adapter) ---")
    transcript.append(empath_out)

    # Resolver
    resolver_out = agents["resolver"].run(state)
    transcript.append("\n--- Resolver Draft (Action Taker) ---")
    transcript.append(resolver_out)

    # Tool use (if requested)
    tool_name, tool_input = _extract_tool_call(resolver_out)
    tool_result = None

    if tool_name:
        tool_fn = tools.get(tool_name)
        if tool_fn:
            tool_result = tool_fn(tool_input)
            state["actions"].append({"tool": tool_name, "input": tool_input, "result": tool_result})

            transcript.append("\n--- Tool Execution ---")
            transcript.append(f"TOOL: {tool_name}")
            transcript.append(f"TOOL_INPUT: {tool_input}")
            transcript.append(f"TOOL_RESULT: {tool_result}")
        else:
            # Tool requested but not available -> escalate
            state["handoff"] = True
            state["handoff_reason"] = f"Requested tool '{tool_name}' not available."

    # Escalation logic (simple example),
    # escalate account/login issues OR missing tool OR anything we mark as handoff.
    if intent == "Account/Login":
        state["handoff"] = True
        state["handoff_reason"] = "Account/Login issues may require human verification."

    if state.get("handoff"):
        escalator_out = agents["escalator"].run(state)
        transcript.append("\n--- Escalation (Human Handoff) ---")
        transcript.append(escalator_out)
        final_response = escalator_out
    else:
        # If no escalation, final response is resolver_out (and include empathy/policy for clarity)
        final_response = (
            f"{empath_out}\n\n"
            f"{researcher_out}\n\n"
            f"{resolver_out}"
        )

    # QA
    state["final_response"] = final_response
    qa_out = agents["qa"].run(state)

    transcript.append("\n--- Quality Review Final (Quality Reviewer) ---")
    transcript.append(qa_out)

    transcript.append("\n=== FINAL CUSTOMER RESPONSE ===")
    transcript.append(final_response)

    return "\n".join(transcript)

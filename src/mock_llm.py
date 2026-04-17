# Predictable LLM stub for offline runs (no API key needed)
def mock_llm_call(role_name: str, system_prompt: str, state: dict) -> str:
    """
    Deterministic mock LLM so you can run WITHOUT API keys/quota.
    Returns predictable outputs for transcripts & grading.
    """
    user = (state.get("user_message") or "").lower()

    if "Greeter" in role_name:
        if any(k in user for k in ["refund", "charged", "billing", "payment", "double charge"]):
            return "Intent: Refund/Billing"
        if any(k in user for k in ["broken", "damaged", "missing", "late delivery", "replacement"]):
            return "Intent: Shipping/Damage"
        if any(k in user for k in ["login", "password", "account", "reset link"]):
            return "Intent: Account/Login"
        return "Intent: General Inquiry"

    if "Researcher" in role_name:
        if any(k in user for k in ["refund", "charged", "billing", "payment", "double charge"]):
            return (
                "Policy found: Refunds are allowed within 14 days of purchase if the item or service "
                "has not been fully used or activated. Billing complaints such as double charges can "
                "be reviewed and may qualify for a refund after verification."
            )
        if any(k in user for k in ["broken", "damaged", "missing", "replacement"]):
            return (
                "Policy found: Damaged item claims must include photo evidence. Once verified, the "
                "customer may receive a replacement or refund depending on the case."
            )
        if any(k in user for k in ["login", "password", "account", "reset link"]):
            return (
                "Policy found: Account and login issues may require identity verification before any "
                "sensitive account action can be completed."
            )
        return "Policy found: General customer support information is available for further assistance."

    if "Empath" in role_name:
        return (
            "I understand your concern, and I’m sorry for the inconvenience. "
            "I’ll do my best to help resolve this for you as quickly as possible."
        )

    if "Resolver" in role_name:
        if any(k in user for k in ["refund", "charged", "billing", "payment", "double charge"]):
            return (
                "TOOL: refund\n"
                "TOOL_INPUT: billing_case\n"
                "Action: A refund request has been prepared and would now move to verification of the "
                "billing details before final approval."
            )
        if any(k in user for k in ["broken", "damaged", "missing", "replacement"]):
            return (
                "Action: Please share photo evidence of the damaged item so that the support team can "
                "verify the issue and arrange a replacement or refund."
            )
        if any(k in user for k in ["login", "password", "account", "reset link"]):
            return (
                "Action: Your issue may need secure account verification. The case should be escalated "
                "to a human support representative for identity confirmation."
            )
        return (
            "Action: Your request has been received. A support response would be prepared based on the "
            "specific details provided."
        )

    if "Escalator" in role_name:
        return (
            "This issue has been escalated for human support because it may require additional "
            "verification or account-sensitive handling. The next step is for a support agent to "
            "review the case and contact the customer."
        )

    if "Quality" in role_name:
        return "QA: PASS - The response is polite, clear, safe, and aligned with policy."

    return "Mock response."

#Mock LLM used for offline execution, grading, and transcript generation.
# Ensures deterministic, cost-free, and reproducible agent behavior


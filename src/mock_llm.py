def mock_llm_call(role_name: str, system_prompt: str, state: dict) -> str:
    """
    Deterministic mock LLM so you can run WITHOUT API keys/quota.
    Returns predictable outputs for transcripts & grading.
    """
    user = (state.get("user_message") or "").lower()

    if "Greeter" in role_name:
        if any(k in user for k in ["refund", "charged", "billing", "payment"]):
            return "Intent: Refund/Billing"
        if any(k in user for k in ["broken", "damaged", "missing", "late delivery"]):
            return "Intent: Shipping/Damage"
        return "Intent: General Inquiry"

    if "Researcher" in role_name:
        return "Policy found: Refunds allowed within 14 days with receipt."

    if "Empath" in role_name:
        return "I understand—sorry about that. I’ll help you sort it out."

    if "Resolver" in role_name:
        return "Action: Refund initiated. Case ID: RFD-1027."

    if "Quality" in role_name:
        return "QA: Response is polite, safe, and follows policy."

    return "Mock response."

#Mock LLM used for offline execution, grading, and transcript generation.
# Ensures deterministic, cost-free, and reproducible agent behavior


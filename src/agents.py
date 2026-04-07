#dataclass is used to reduce reptitive code when defining agent roles
from dataclasses import dataclass

#this is used for tping for clarity and safety in multi-agent interfaces.

from typing import Callable, Dict, Any

#'state' is the shared memory across all agents, it also allows agents to read and build on each other's outputs
State = Dict[str, Any]

#llmcall defines the contract for calling the language model, this intended distraction allows easy swapping of LLm providers. 
LLMCall = Callable[[str, str, State], str]

# "Agent" represents a single specialized role in the system,
#each agent has a clear responsibility enforced by its promt.
@dataclass
class Agent:
    #name of the role (routing and logging)
    role_name: str

    #sytem prompt that constrains agent behavior.
    system_prompt: str

    #Function used to call the LLm with role context to make the output make sense.
    llm_call: LLMCall

    #This execution method is the core for the agent and uses shared state to maintain coordination.
    def run(self, state: State) -> str:
        return self.llm_call(self.role_name, self.system_prompt, state)

    #This factory function helps create all the agents, also cnetralizes role definitons for easy use.
def build_agents(llm_call: LLMCall) -> Dict[str, Agent]:
    """
    Builds all agents (role specialization). Supervisor will orchestrate them.
    """
    #the "greeter" prompt helps determines user intent and routes the request
    greeter_prompt = (
        "You are the Greeter/Intent Classifier.\n"
        "Classify the user's request into ONE intent:\n"
        "- Refund/Billing\n"
        "- Shipping/Damage\n"
        "- Account/Login\n"
        "- General Inquiry\n"
        "Output format: 'Intent: <category>' only."
    )

    #the "researcher" prompt helps find relevant policy (information) from the knowledge base
    researcher_prompt = (
        "You are the Researcher/Knowledge Retriever.\n"
        "Use the knowledge base in state['kb'] to find the relevant policy.\n"
        "Return a short policy snippet and any conditions."
    )

    empath_prompt = (
        "You are the Empath/Tone Adapter.\n"
        "Write a short empathetic acknowledgment and reassure the user."
    )

    resolver_prompt = (
        "You are the Resolver/Action Taker.\n"
        "Propose a concrete resolution.\n"
        "If a tool is needed, specify:\n"
        "TOOL: refund | schedule_callback\n"
        "TOOL_INPUT: <one short line>\n"
        "Then give the final response to the customer."
    )

    escalator_prompt = (
        "You are the Escalator/Human Handoff Coordinator.\n"
        "If the issue is high-risk, unclear, or needs a human, prepare a handoff note.\n"
        "Include: reason, what was tried, what info is needed next."
    )

    qa_prompt = (
        "You are the Quality Reviewer.\n"
        "Check: politeness, policy alignment, safety, and clarity.\n"
        "Return: 'QA: PASS' or 'QA: FAIL' + one improvement line."
    )

    return {
        "greeter": Agent("Greeter", greeter_prompt, llm_call),
        "researcher": Agent("Researcher", researcher_prompt, llm_call),
        "empath": Agent("Empath", empath_prompt, llm_call),
        "resolver": Agent("Resolver", resolver_prompt, llm_call),
        "escalator": Agent("Escalator", escalator_prompt, llm_call),
        "qa": Agent("Quality Reviewer", qa_prompt, llm_call),
    }

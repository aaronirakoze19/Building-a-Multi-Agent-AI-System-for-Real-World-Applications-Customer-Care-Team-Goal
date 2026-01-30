![IMG_0495](https://github.com/user-attachments/assets/21e6f49a-a09c-41cf-9fd9-06d823bdd859)# Building-a-Multi-Agent-AI-System-for-Real-World-Applications-Customer-Care-Team-Goal

This project implements a multi-agent Customer Care Team that handles complex customer inquiries end-to-end, going beyond simple Q&A.

It uses a supervisor-orchestrated multi-agent architecture inspired by Microsoft AutoGen’s conversational style, with clearly specialized agents, shared state, tool use, escalation, and quality review.

The system is designed to be deterministic, offline-runnable, and reproducible using a mock LLM for grading and demonstration.
The system uses specialized AI agents coordinated by a supervisor to classify intent, retrieve policies, respond empathetically, take actions, and perform quality assurance.

Use Case: Customer Care Automation

the goal is to Handle customer issues such as refunds, billing disputes, damaged orders, and account problems through coordinated agent collaboration

#requirments and bnefits

-Customer support requires multiple skills (classification, policy lookup, empathy, action, QA)

-Naturally fits a multi-agent division of labor

-Demonstrates clear benefits over a single-agent approach

-Enables realistic tool usage and escalation scenarios


Agents have specifies roles such as;
<img width="482" height="143" alt="agent and roles" src="https://github.com/user-attachments/assets/3da95dc9-60fa-4eda-aed2-a943a855d3da" />

Agent communication flow shows how the user interacts with an agent thus showing input and output throught the entire process;
<img width="204" height="216" alt="flow" src="https://github.com/user-attachments/assets/02ebad15-d827-4a46-a547-5aee3993ad54" />

#How to run (including LLM provider setup)

1.the virtual environment is needed to set up that scene (on bash)
python -m venv .venv
.venv\Scripts\activate

2. Install dependencies (on bash)
pip install -r requirements.txt

3. after that run the multi-agent sytem (on bash)
python src/main.py

the output will show agent's actions and decsisons are stremed directly streamed to the terminal and also interation trascripits are automatically saved in (on bash) .
/transcripts/
  ├── transcript_1.txt
  ├── transcript_2.txt
  └── transcript_3.txt

Transcripts showing collaboration to create an output to prove that the agent creation and process is eligable

Example 2 : Account Login Problem (transcript 3)

User Request

<img width="578" height="363" alt="transcript and interaction 2" src="https://github.com/user-attachments/assets/65b26b42-31b5-4afe-9d44-472add0aab09" />


“I can’t log into my account and the reset link is not working.”

Agent Collaboration Flow

1.Greeter / Intent Classifier
Classifies the request as a General Inquiry

#(makefile) intent: General Inquiry

2.Reseacher/Knowledge retriever
-this searches available policies and support rules.
-returns the closest relevant policy:

#(pgsql) Policy found: Refunds allowed within 14 days with receipt.

3. Empath / Tone Adapter

-Acknowledges frustration and reassures the user:

#(bash) understand—sorry about that. I’ll help you sort it out.

4. Resolver / Action Taker

.Proposes a concrete resolution 
simulates a refund action:

#(vbnet) Refund initiated. Case ID: RFD-1027.

5. Quality Reviewer

-Reviews the response for safety, tone and policy and compliance:


#(vbnet) QA: Response is polite, safe, and follows policy.



Example 1 
<img width="596" height="366" alt="transcript and interaction 1" src="https://github.com/user-attachments/assets/201d8e8d-84ea-4bc9-b124-4e6b8b34fad0" />

Identifies the user’s issue as Refund/Billing

Example 1: Refund & Billing Issue (Transcript 1)

User Request

“Hi, I want a refund. I was charged twice for my subscription.”

Agent Collaboration Flow

Greeter / Intent Classifier

Identifies the user’s issue as Refund/Billing

Output: 
#(makefile) intent: Refund/Billing

2. Researcher / Knowledge Retriever

-Consults the shared knowledge base (state["kb"])

-Retrieves the relevant refund policy:

#(pgsql) Policy found: Refunds allowed within 14 days with receipt.

3. Empath / Tone Adapter

Produces a polite and reassuring response:

#(bash) I understand—sorry about that. I’ll help you sort it out.

4. Resolver / Action Taker

Proposes a concrete resolution

Simulates a refund action
#(vbnet) Action: Refund initiated. Case ID: RFD-1027.

5. Quality Reviewer

Reviews the response for safety, tone, and policy compliance:
#(vbent) QA: Response is polite, safe, and follows policy.


#Key Challenges & Solutions

Coordination Between Agents

-In a multi-agent system, coordinating several specialized agents can be challenging because agents may repeat work, act out of sequence, or provide conflicting outputs. Without a central controller, the system risks producing fragmented or inconsistent responses that do not fully resolve the user’s issue. This project addresses coordination through a Supervisor agent that controls the execution flow. The supervisor decides which agent acts next, passes shared state between agents, and determines when the task is complete. This ensures smooth collaboration and a clear division of labor across the Greeter, Researcher, Empath, Resolver, Escalator, and Quality Reviewer agents.

Hallucinations & Response Accuracy

-Language models may hallucinate facts, policies, or actions—especially in customer service scenarios involving refunds or account issues. Such errors can mislead users, violate company policies, or create trust issues if unchecked.To reduce hallucinations, the system uses a shared knowledge base and enforces structured prompts for each agent. Additionally, a Quality Reviewer agent performs a final critique to verify policy alignment, tone, and safety before the response is delivered to the customer.


Infinite Loops & Over-Processing

-Multi-agent systems risk entering infinite loops when agents continuously request additional input or re-evaluate decisions. This can lead to unnecessary computation, delayed responses, and poor user experience. The system prevents looping by defining a strict agent sequence and a clear termination condition. Once the Quality Reviewer completes its evaluation and the supervisor confirms goal completion, execution stops immediately.


Cost & API Usage Constraints
-Using real LLM APIs can be expensive, rate-limited, or unavailable during development and grading. This creates barriers to testing, reproducibility, and reliable demonstrations of system behavior. To solve this, the project implements a deterministic mock LLM that simulates agent reasoning without external API calls. This approach ensures cost-free execution, consistent outputs for grading, and the ability to run the system fully offline.

Human-in-the-Loop & Safety Control

-Fully autonomous systems may take sensitive actions—such as issuing refunds or escalating cases—without appropriate oversight. In real-world customer service, such actions often require human approval. This project includes a Human-in-the-Loop design through the Escalator and Resolver agents. Actions are simulated rather than executed, and the system is designed to pause or prepare handoff notes when human review or approval is required.


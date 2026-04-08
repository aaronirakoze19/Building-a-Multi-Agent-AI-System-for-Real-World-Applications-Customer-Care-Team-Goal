Customer care agent (Health care)

This demonstrates a multi-agent artificial intelligence system designed to simulate how a real-world customer care team operates. Instead of using a single AI model to handle everything, the system is structured as a pipeline of specialized agents, each responsible for a specific task. This approach makes the system more organized, reliable, and closer to real-world customer support workflows.

The idea behind the system was to break down the process of handling a customer request into smaller, manageable steps. By doing this, each part of the response is handled carefully rather than being generated all at once, which improves both accuracy and clarity.

Here is a summarized workflow:
<img width="204" height="216" alt="flow" src="https://github.com/user-attachments/assets/597b88bd-1e0d-4bcc-9ac8-f94739ddf22d" />

System Design

The system is built around clearly defined agent roles, where each agent focuses on a specific responsibility. This structure helps reduce confusion and makes the overall process easier to follow and debug.
Screenshots included in the project show the agent roles, the workflow pipeline, and example outputs, helping to visualize how the system operates from input to final response.

System Workflow

When a user submits a request, the system processes it step by step. The Greeter (Intent Classifier) first identifies what the user is asking for, such as a refund or help with logging in. The request is then passed to the Researcher, which retrieves the relevant policy from the knowledge base.
After that, the Empath adjusts the tone of the response so that it sounds polite and user-friendly. The Resolver then takes action based on the policy, such as initiating a refund or suggesting a solution. If the issue is complex or unclear, the Escalator determines whether it should be handled by a human. Finally, the Quality Reviewer checks the response before it is delivered to ensure it is accurate, safe, and aligned with policy.


System Design

The system is built around clearly defined agent roles, where each agent focuses on a specific responsibility. This structure helps reduce confusion and makes the overall process easier to follow and debug.
Screenshots included in the project show the agent roles, the workflow pipeline, and example outputs, helping to visualize how the system operates from input to final response.


Outputs and Demonstration

The project includes sample transcripts that show how the system responds to different user scenarios. These transcripts highlight how each agent contributes to the final response and make it easier to understand the internal flow of the system.
A demo notebook is also included to demonstrate how the system runs in practice, making it easier to test and present the project.


The projected is structured contine in the src folder which includes the agent definitions, the supervisor responsible for coordinating the workflow, and the main script used to run the system.
Supporting folders include demo for the notebook demonstration, transcripts for interaction logs, and Screenshots for images used in documentation. Additional files such as requirements.txt, .env, .gitignore, and the reflection report provide configuration, dependency management, and further explanation of the project.

The basic conclusion for this project is show that shows that using a multi-agent approach makes the system more structured and reliable compared to a single-agent setup. By assigning different responsibilities to different agents, the system is able to handle tasks more effectively and reduce the likelihood of errors.
The addition of a Quality Reviewer adds an extra layer of validation, ensuring that responses meet the required standards before being delivered. Overall, this approach results in a system that is more transparent, easier to manage, and better suited for real-world applications.

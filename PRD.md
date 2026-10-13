# PRD — Autonomous AI Task Worker (Intern Problem Statement)

> Source: intern problem statement. Saved here as the requirements baseline.
> Progress is tracked in `README.md` (Phase status) and per-directory `CONTEXT.md` files.

## Problem

Companies perform many repetitive tasks that involve reading information, deciding what to do next, using websites or applications, and checking whether the task was completed correctly. Today, a person often has to manually move between different tools to complete even a simple request.

Build a prototype of an AI worker that can take a natural language task and autonomously attempt to complete it using a computer. For example, a user might say:

> "Find the latest invoice from Company X, extract the amount and due date, enter it into our internal system, and tell me once it is done."

## Required capabilities

The system should ideally be capable of:

- Understanding the user's end goal rather than requiring every step to be specified.
- Breaking the request into a sequence of actions.
- Using available tools such as a browser, files, APIs, or a simulated company application.
- Observing the result of each action.
- Deciding what to do next based on what happened.
- Remembering relevant information discovered during execution.
- Detecting when an action fails.
- Attempting a reasonable alternative or retry where appropriate.
- Verifying whether the requested outcome was actually achieved.
- Asking the user for clarification or approval when it cannot safely proceed.
- Returning a concise summary and useful evidence of completion.

## Scope

- No production-ready system needed.
- No need to support every website, desktop application, or business workflow.
- May restrict the prototype to a small environment, simulated company application, browser environment, or limited set of tools.
- A narrow prototype that genuinely works beats a broad system where most functionality is mocked.
- Architecture, model, framework, interface, and exact workflow are not prescribed.

## Evaluation criteria

- **Autonomy** — determine and execute meaningful next actions without being told every step.
- **Execution** — actually perform work rather than merely explain what should be done.
- **Reliability** — handle unexpected states, errors, retries, and failures.
- **Verification** — determine whether the requested outcome was actually achieved.
- **Generalization** — how much of the system stays unchanged on a different task.
- **Engineering Quality** — architecture, implementation, code quality, debugging, technical judgment.
- **Product Thinking** — focus on accomplishing the user's actual objective.
- **Technical Understanding** — explain why the system was built the way it was.

Feature count alone is not evaluated.

## Submission requirements

- GitHub repository or equivalent source-code link.
- README with setup and run instructions.
- Short explanation of the architecture.
- Explanation of important technical/design decisions.
- Demo video or accessible live demo showing the prototype working.
- Known limitations.
- What you would build next with additional time.
- Any assumptions made.
- Details of models, APIs, frameworks, external services, or pre-built components used.

AI coding tools are allowed. No real company credentials, confidential information, or unauthorized third-party access — sandbox/mock environments only.

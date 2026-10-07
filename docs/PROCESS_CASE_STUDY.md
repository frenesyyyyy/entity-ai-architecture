# From analysis work to an observable process

## Problem and intended outcome

Comparing AI answers manually involves selecting questions, running them across
providers, tracking failures, normalizing answers and assembling a report. The
automation opportunity is to make these steps repeatable and inspectable while
keeping a person responsible for interpreting and acting on the results.

The intended outcome is less manual collection and more time evaluating evidence.
No measured time saving is asserted here: establishing a baseline and measuring
the change would be part of a real rollout.

## A concrete exception

An analyst requests a fixed question set from two providers. Provider A answers;
provider B times out. The system can still retain A's evidence, but the report must
show B's missing coverage. It must not treat B's timeout as evidence that the brand
was absent, or quietly substitute another provider and call the result comparable.

The synthetic example includes successful answers, a measured non-mention and a
failed call. It reports each provider separately. This is the central lesson:
exception handling changes the meaning of the business result, not just the logs.

## Transfer to internal process automation

| Step | Question to resolve with the process owner | Output |
| --- | --- | --- |
| Discover | Where do handoffs, rework and manual checks occur? | Current process and baseline |
| Define | What inputs, states and acceptance criteria are required? | Contract and accountable owner |
| Automate | Which rules are stable, and which tasks need AI interpretation? | Deterministic workflow with bounded AI stages |
| Handle exceptions | What can retry, what must stop, and what needs a person? | Failure paths and review queue |
| Measure | Did throughput improve without sacrificing quality? | Before/after evidence and operating measures |
| Maintain | Who handles changes and failed runs after launch? | Runbook, tests and ownership |

For a 1KOMMA5 AI Process & Business Excellence discussion, these decisions are
more transferable than the particular brand-analysis domain. A low-code workflow
could orchestrate stable connectors and approvals; custom code is useful where
contracts, provider normalization and validation need precise tests. This is a
design comparison, not a claim that this product uses n8n.

## Measurement plan

- Compare manual handling minutes per accepted report before and after automation.
- Track end-to-end duration separately from active human handling time.
- Record completed, partial and failed runs, with provider coverage and causes.
- Measure rework and human-review acceptance using a representative sample.
- Track API cost per accepted result, including retries and failed attempts.
- Keep measurement questions and context stable when comparing follow-up results.

Pilot with synthetic or consented inputs, inspect exceptions with the process
owner, and expand only when the measured improvement justifies the maintenance cost.

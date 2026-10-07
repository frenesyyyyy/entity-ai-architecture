# Decisions and reliability

## Failed measurement must stay separate from a negative finding

If two of four provider calls fail and neither successful response mentions a
brand, the measured result is zero mentions out of two answers, with 50% coverage.
It is not four negative answers. If all calls fail, the rate is unavailable.
The public example represents that as `null`, alongside explicit coverage counts.

The reviewed implementation includes provider outcome tracking and fault
classification. This is useful because quota exhaustion, malformed requests,
blocked sites and genuine negative observations require different responses.

## Use a queue for work that outlives a request

The private implementation has persistent job states, guarded pending-to-processing
claims, stale-job recovery and bounded attempts. These reduce duplicate claims
and abandoned work. They do not prove exactly-once execution of external calls.
Crash-after-call recovery and idempotency at side-effect boundaries still need
explicit tests. SQLite is an operationally simple choice with a single-writer
trade-off; it is not evidence of unlimited horizontal scalability.

## Make stage ownership explicit

State patches and protected result fields limit where outputs may be written.
That makes concurrent work easier to reason about, but missing allowed fields can
silently discard useful evidence. Contract tests should cover both accepted and
rejected writes and their downstream meaning.

## Fail the right scope

The execution manager isolates stage exceptions and records telemetry. Required
identity/measurement failures can stop publication; some optional failures can
degrade a result. Partial completion must be visible to the user, with unavailable
metrics left unavailable. A generic "success" label would conceal the problem.

## Operational measures and remaining work

The reviewed telemetry structure records stage duration, status and classified
faults, and has fields for retries and cost estimates. A field's presence does not
prove that every integration populates it accurately. Cost accounting needs
reconciliation with provider invoices before it supports margin claims.

Recommended validation work includes timeout and rate-limit injection, malformed
payloads, worker crashes, duplicate submissions and changed measurement panels.
These are proposed checks, not a claim that the entire private system passed them.
The public CI exercises only the synthetic contract and its failure cases.

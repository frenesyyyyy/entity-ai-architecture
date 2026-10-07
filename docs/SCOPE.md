# Scope and evidence

## What was reviewed

This study was prepared from local source inspection on 7 October 2026. It draws
on the private execution manager, node-result contracts, state reducer, telemetry,
provider coverage accounting, queue and worker structure. Implementation details
were checked against executable code rather than copied from earlier pitch text.

The source supports the existence of stage orchestration, guarded queue claims,
state patches, protected result keys, stage telemetry and explicit missing-data
accounting. It does not by itself prove live deployment state, correct behavior on
every input, a production SLA, cost accuracy or a measured business improvement.

## Publication boundary

Only newly written explanations and synthetic demonstration code are included.
Private Git history, product source, scoring rules, provider routing, prompts,
customer identifiers, screenshots with customer data, credentials, operational
logs and commercial terms are excluded. The production repositories remain private.

The example is intentionally small and has no network client. It rejects invalid
observation records, counts only successful measurements and keeps provider groups
separate. It does not prove queue reliability, live provider behavior or model quality.

## Limitations worth discussing

- Providers change output formats, models and availability independently.
- A schema-valid answer can still be wrong; evidence and human evaluation remain necessary.
- A stable question set supports comparability but cannot eliminate model drift.
- Local queue correctness does not imply exactly-once external side effects.
- Large legacy modules and integration-specific paths still create maintenance cost.
- Retry and cost fields need end-to-end verification before supporting operational claims.

AI-assisted preparation does not change these evidence limits. The public material
is designed to support an engineering conversation, not to imply a complete public
implementation or independently audited performance.

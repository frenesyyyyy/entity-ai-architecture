"""Offline contract example. All provider data is synthetic."""

import json


def normalize(provider, question_id, raw):
    """Validate one observation without turning a failure into a negative result."""
    if not provider or not question_id:
        raise ValueError("provider and question_id are required")
    status = raw.get("status")
    if status not in {"measured", "failed"}:
        raise ValueError("unknown observation status")
    mention = raw.get("brand_mentioned")
    evidence = raw.get("evidence")
    if status == "measured":
        if type(mention) is not bool:
            raise ValueError("measured observations require a boolean finding")
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError("measured observations require retained evidence")
        if raw.get("error") is not None:
            raise ValueError("a measured observation cannot carry a failure")
        error = None
    else:
        if mention is not None or evidence is not None:
            raise ValueError("failed observations cannot carry findings")
        error = raw.get("error")
        if error not in {"timeout", "rate_limit", "unavailable"}:
            raise ValueError("failed observations require a classified error")
    return {
        "provider": provider,
        "question_id": question_id,
        "status": status,
        "brand_mentioned": mention,
        "evidence": evidence,
        "error": error,
    }


def summarize(provider, question_ids, observations):
    """Keep providers separate and compute rates only over actual measurements."""
    if not provider or not question_ids or any(not q for q in question_ids):
        raise ValueError("a provider and nonempty question set are required")
    if len(set(question_ids)) != len(question_ids):
        raise ValueError("question IDs must be unique")
    expected = set(question_ids)
    seen = set()
    valid = []
    for row in observations:
        question_id = row["question_id"]
        if row["provider"] != provider or question_id not in expected:
            raise ValueError("observation is outside the measurement scope")
        if question_id in seen:
            raise ValueError("duplicate observations would distort the denominator")
        seen.add(question_id)
        valid.append(normalize(provider, question_id, row))
    measured = [row for row in valid if row["status"] == "measured"]
    mentions = sum(row["brand_mentioned"] for row in measured)
    return {
        "provider": provider,
        "requested": len(expected),
        "measured": len(measured),
        "failed": len(valid) - len(measured),
        "missing": len(expected) - len(seen),
        "mentions": mentions,
        "mention_rate": mentions / len(measured) if measured else None,
        "coverage": len(measured) / len(expected),
        "status": "complete" if len(measured) == len(expected) else "partial",
    }


def demo():
    questions = ["q1", "q2", "q3"]
    rows = [
        normalize("provider-a", "q1", {
            "status": "measured", "brand_mentioned": True,
            "evidence": "Synthetic response: Example Brand is mentioned.",
        }),
        normalize("provider-a", "q2", {
            "status": "measured", "brand_mentioned": False,
            "evidence": "Synthetic response: no mention of the target brand.",
        }),
        normalize("provider-a", "q3", {"status": "failed", "error": "timeout"}),
    ]
    return {
        "schema_version": "illustration-v1",
        "data_kind": "synthetic",
        "question_set_version": "example-panel-v1",
        "observations": rows,
        "provider_summaries": [
            summarize("provider-a", questions, rows),
            summarize("provider-b", questions, []),
        ],
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))

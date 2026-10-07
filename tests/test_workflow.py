import json
from pathlib import Path
import unittest

from examples.workflow import demo, normalize, summarize


class WorkflowTests(unittest.TestCase):
    def test_failure_is_not_a_negative_observation(self):
        summary = demo()["provider_summaries"][0]
        self.assertEqual(summary["mention_rate"], 0.5)
        self.assertEqual(summary["measured"], 2)
        self.assertEqual(summary["failed"], 1)
        self.assertEqual(summary["status"], "partial")

    def test_no_measurements_has_no_rate(self):
        summary = demo()["provider_summaries"][1]
        self.assertIsNone(summary["mention_rate"])
        self.assertEqual(summary["missing"], 3)
        self.assertEqual(summary["coverage"], 0)

    def test_measured_absence_is_zero(self):
        row = normalize("a", "q", {
            "status": "measured", "brand_mentioned": False, "evidence": "Synthetic answer.",
        })
        self.assertEqual(summarize("a", ["q"], [row])["mention_rate"], 0)
        self.assertEqual(summarize("a", ["q"], [row])["status"], "complete")

    def test_all_calls_failed_remains_unavailable(self):
        row = normalize("a", "q", {"status": "failed", "error": "rate_limit"})
        result = summarize("a", ["q"], [row])
        self.assertIsNone(result["mention_rate"])
        self.assertEqual(result["failed"], 1)
        self.assertEqual(result["missing"], 0)

    def test_duplicate_and_cross_provider_rows_are_rejected(self):
        row = demo()["observations"][0]
        with self.assertRaises(ValueError):
            summarize("provider-a", ["q1"], [row, row])
        with self.assertRaises(ValueError):
            summarize("provider-b", ["q1"], [row])
        with self.assertRaises(ValueError):
            summarize("provider-a", ["q2"], [row])

    def test_invalid_question_sets_are_rejected(self):
        for questions in [[], ["q", "q"], [""]]:
            with self.subTest(questions=questions), self.assertRaises(ValueError):
                summarize("a", questions, [])

    def test_malformed_provider_payloads_are_rejected(self):
        for raw in [
            {"status": "unknown"},
            {"status": "measured", "brand_mentioned": "false", "evidence": "answer"},
            {"status": "measured", "brand_mentioned": True},
            {"status": "failed", "error": "timeout", "brand_mentioned": False},
            {"status": "failed", "error": "timeout", "evidence": "invented finding"},
            {"status": "measured", "brand_mentioned": True, "evidence": "answer", "error": "timeout"},
        ]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                normalize("a", "q", raw)

    def test_checked_in_example_matches_demo(self):
        path = Path(__file__).parents[1] / "examples/normalized-output.json"
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), demo())


if __name__ == "__main__":
    unittest.main()

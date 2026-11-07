"""Unit tests for reviewing-pull-requests/scripts/post_review.py (stdlib only)."""

import importlib.util
import pathlib
import unittest

SCRIPT = (pathlib.Path(__file__).resolve().parents[1]
          / "plugins/kemetra-dev/skills/reviewing-pull-requests/scripts/post_review.py")
spec = importlib.util.spec_from_file_location("post_review", SCRIPT)
post_review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(post_review)

REVIEW = """# Review — feat vs abc1234 · 0 Critical · 1 Major · 0 Minor · 0 Trivial · Verdict: Fix before merge

Summary.

### 1. [Major] Functional Correctness — `src/a.ts:10-12` · Quick win
**Round the fee.**
Body.

## Questions
- q

## Not checked
- tests not run — CI
"""


class SplitTest(unittest.TestCase):
    def test_last_finding_excludes_trailing_sections(self) -> None:
        body, findings = post_review.split(REVIEW)
        self.assertEqual(len(findings), 1)
        block, path, start, end = findings[0]
        self.assertEqual((path, start, end), ("src/a.ts", 10, 12))
        self.assertNotIn("## Questions", block)
        self.assertNotIn("## Not checked", block)

    def test_not_checked_without_questions_is_cut(self) -> None:
        review = REVIEW.replace("## Questions\n- q\n\n", "")
        _, findings = post_review.split(review)
        self.assertNotIn("Not checked", findings[0][0])


if __name__ == "__main__":
    unittest.main()

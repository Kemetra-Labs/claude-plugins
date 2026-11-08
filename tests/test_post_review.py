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


class DiffLinesTest(unittest.TestCase):
    def _stub_gh(self, output: str) -> None:
        original = post_review.gh
        post_review.gh = lambda *args, **kwargs: output
        self.addCleanup(setattr, post_review, "gh", original)

    def test_multi_page_file_listing_is_merged(self) -> None:
        # gh --paginate prints one JSON array per page, back to back.
        page1 = '[{"filename": "a.ts", "patch": "@@ -1,1 +1,1 @@\\n+x"}]'
        page2 = '[{"filename": "b.ts", "patch": "@@ -0,0 +5,2 @@\\n+y\\n+z"}]'
        self._stub_gh(page1 + "\n" + page2)
        result = post_review.diff_lines("o/r", 1)
        self.assertEqual(result, {"a.ts": {1}, "b.ts": {5, 6}})

    def test_no_newline_marker_does_not_shift_lines(self) -> None:
        patch = "@@ -1,2 +1,3 @@\\n a\\n-b\\n\\\\ No newline at end of file\\n+b\\n+c"
        self._stub_gh('[{"filename": "f.ts", "patch": "' + patch + '"}]')
        result = post_review.diff_lines("o/r", 1)
        self.assertEqual(result["f.ts"], {1, 2, 3})


if __name__ == "__main__":
    unittest.main()

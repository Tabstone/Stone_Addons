from pathlib import Path
import re
import unittest


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "sync-upstream.yml"


class SyncWorkflowRulesTests(unittest.TestCase):
    def test_waits_for_the_exact_dispatched_metadata_run(self):
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertRegex(
            workflow,
            re.compile(
                r"- name: Dispatch addon metadata workflow\n"
                r"\s+id: dispatch_metadata\n"
                r".*?run_url=\$\(gh workflow run addon-metadata\.yml --ref \"\$PR_BRANCH\"\)\n"
                r".*?run_id=\"\$\{run_url##\*/\}\"\n"
                r".*?echo \"run_id=\$run_id\" >> \"\$GITHUB_OUTPUT\"",
                re.DOTALL,
            ),
        )
        self.assertIn(
            'RUN_ID: ${{ steps.dispatch_metadata.outputs.run_id }}',
            workflow,
        )

        wait_step = workflow.split("- name: Wait for addon metadata workflow", 1)[1]
        wait_step = wait_step.split("- name: Merge pull request", 1)[0]
        self.assertIn('gh run view "$RUN_ID" --json status,conclusion', wait_step)
        self.assertNotIn("gh run list", wait_step)


if __name__ == "__main__":
    unittest.main()

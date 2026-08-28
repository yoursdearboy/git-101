from __future__ import annotations

import importlib.util
import csv
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "create_course_project", ROOT / "bin" / "create_course_project.py"
)
assert SPEC and SPEC.loader
course_project = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(course_project)


def git(target: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=target,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class CourseProjectTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def make(self, state: str) -> Path:
        target = self.root / state
        course_project.copy_starter(target)
        course_project.build_local_state(target, state)
        return target

    def test_starter_matches_manifest_and_has_no_commits(self) -> None:
        target = self.make("starter")
        expected = json.loads(course_project.MANIFEST.read_text(encoding="utf-8"))
        actual = {
            item.relative_to(target).as_posix()
            for item in target.rglob("*")
            if item.is_file() and ".git" not in item.relative_to(target).parts
        }
        self.assertEqual(set(expected), actual)
        self.assertNotEqual(git(target, "rev-parse", "--verify", "HEAD", check=False).returncode, 0)
        self.assertIn("?? analysis.qmd", git(target, "status", "--short").stdout)
        self.assertTrue((target / "penguins.R").exists())
        self.assertTrue((target / "tables.qmd").exists())

    def test_clean_states_have_expected_branch_and_history(self) -> None:
        expected = {
            "baseline": ("main", 1),
            "paper": ("main", 2),
            "histogram": ("main", 3),
            "boxplot-branch": ("boxplot", 4),
            "merged": ("main", 6),
        }
        for state, (branch, commits) in expected.items():
            with self.subTest(state=state):
                target = self.make(state)
                self.assertEqual(git(target, "branch", "--show-current").stdout.strip(), branch)
                self.assertEqual(int(git(target, "rev-list", "--count", "--all").stdout), commits)
                self.assertEqual(git(target, "status", "--porcelain").stdout, "")

    def test_paper_uses_quarto_data_path(self) -> None:
        target = self.make("histogram")
        paper = (target / "paper.qmd").read_text(encoding="utf-8")
        self.assertIn('read.csv("data/penguins.csv")', paper)
        self.assertIn("embed-resources: true", paper)
        self.assertNotIn("%>%", paper)
        self.assertNotIn("png(", paper)
        report = (target / "paper.html").read_text(encoding="utf-8")
        self.assertIn("data:image/png;base64,", report)
        self.assertFalse((target / "paper.R").exists())

    def test_histogram_commit_contains_html_report(self) -> None:
        target = self.make("histogram")
        changed = git(target, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").stdout.splitlines()
        self.assertEqual(changed, ["paper.html", "paper.qmd"])
        self.assertEqual(git(target, "log", "-1", "--format=%s").stdout.strip(), "Собрал HTML-отчёт о длине клюва")

    def test_paper_state_updates_missing_bill_lengths(self) -> None:
        baseline = self.make("baseline")
        paper = self.make("paper")

        def bill_lengths(target: Path) -> list[str]:
            with (target / "data" / "penguins.csv").open(encoding="utf-8", newline="") as source:
                return [row["bill_len"] for row in csv.DictReader(source)]

        self.assertEqual(bill_lengths(baseline).count(""), 2)
        self.assertEqual(bill_lengths(paper).count(""), 0)
        paper_source = (paper / "paper.qmd").read_text(encoding="utf-8")
        self.assertIn("embed-resources: true", paper_source)
        self.assertIn("mean(data$bill_len)", paper_source)
        self.assertNotIn("mean(x)", paper_source)
        changed = git(paper, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").stdout.splitlines()
        self.assertEqual(changed, ["data/penguins.csv", "paper.qmd"])

    def test_dirty_main_contains_only_uncommitted_paper_change(self) -> None:
        target = self.make("dirty-main")
        self.assertEqual(git(target, "branch", "--show-current").stdout.strip(), "main")
        self.assertEqual(git(target, "status", "--short").stdout, " M paper.qmd\n")

    def test_conflict_is_an_unfinished_merge_in_paper(self) -> None:
        target = self.make("conflict")
        self.assertTrue((target / ".git" / "MERGE_HEAD").exists())
        self.assertIn("UU paper.qmd", git(target, "status", "--short").stdout)
        paper = (target / "paper.qmd").read_text(encoding="utf-8")
        self.assertIn("<<<<<<< HEAD", paper)
        self.assertIn(">>>>>>> boxplot", paper)

    def test_merged_state_has_merge_commit(self) -> None:
        target = self.make("merged")
        parents = git(target, "show", "-s", "--format=%P", "HEAD").stdout.split()
        self.assertEqual(len(parents), 2)
        self.assertIn('boxplot(x, ylab = "Bill length, mm")', (target / "paper.qmd").read_text())

    def test_webhook_request_uses_pull_request_event(self) -> None:
        with mock.patch.object(course_project, "run") as mocked_run:
            course_project.add_webhook("owner/repo", "https://example.test/hook", "secret")
        command = mocked_run.call_args.args[0]
        self.assertIn("repos/owner/repo/hooks", command)
        self.assertIn("events[]=pull_request", command)
        self.assertIn("config[secret]=secret", command)

    def test_github_login_uses_browser_when_status_fails(self) -> None:
        failed = subprocess.CompletedProcess([], 1)
        passed = subprocess.CompletedProcess([], 0)
        with mock.patch.object(course_project.shutil, "which", return_value="/usr/bin/gh"), mock.patch.object(
            course_project, "run", side_effect=(failed, passed, passed)
        ) as mocked_run, mock.patch("builtins.print"):
            course_project.ensure_gh_auth()
        self.assertEqual(
            mocked_run.call_args_list[1].args[0],
            ["gh", "auth", "login", "--web", "-h", "github.com", "-p", "https"],
        )

    def test_publish_starts_remote_from_main_and_restores_branch(self) -> None:
        target = self.make("merged")
        git(target, "switch", "-c", "adjust-by-sex")
        completed = subprocess.CompletedProcess([], 0, stdout="adjust-by-sex\n", stderr="")
        with mock.patch.object(course_project, "run", wraps=course_project.run) as mocked_run:
            mocked_run.side_effect = [
                completed,
                subprocess.CompletedProcess([], 0, stdout="", stderr=""),
                subprocess.CompletedProcess([], 0, stdout="", stderr=""),
                subprocess.CompletedProcess([], 0, stdout="", stderr=""),
                subprocess.CompletedProcess([], 0, stdout="", stderr=""),
            ]
            course_project.publish_repository(target, "owner/repo", "private")
        commands = [call.args[0] for call in mocked_run.call_args_list]
        self.assertEqual(commands[1], ["git", "switch", "main"])
        self.assertIn(["git", "switch", "adjust-by-sex"], commands)

    def test_remote_preflight_distinguishes_missing_from_network_error(self) -> None:
        missing = subprocess.CompletedProcess([], 1, stdout="", stderr="GraphQL: Could not resolve to a Repository")
        offline = subprocess.CompletedProcess([], 1, stdout="", stderr="network is unreachable")
        with mock.patch.object(course_project, "run", return_value=missing):
            course_project.ensure_remote_absent("owner/missing")
        with mock.patch.object(course_project, "run", return_value=offline):
            with self.assertRaises(course_project.CourseProjectError):
                course_project.ensure_remote_absent("owner/unknown")

    def test_github_webhook_requires_url_before_authentication(self) -> None:
        with mock.patch.object(course_project, "ensure_gh_auth") as auth:
            result = course_project.main(
                [str(self.root / "webhook"), "--state", "github-webhook", "--repo", "owner/repo"]
            )
        self.assertEqual(result, 1)
        auth.assert_not_called()

    def test_refuses_existing_target(self) -> None:
        target = self.root / "existing"
        target.mkdir()
        self.assertEqual(course_project.main([str(target), "--state", "starter"]), 1)


if __name__ == "__main__":
    unittest.main()

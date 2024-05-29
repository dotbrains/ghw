import unittest
from unittest.mock import patch
import sys
from io import StringIO
from contextlib import redirect_stdout

from src.ghw import main as gh_main


class TestDryRun(unittest.TestCase):
    def test_dry_run_clone(self):
        repo_address = "github.com/octocat/Hello-World"
        test_args = ["ghw.py", "--dry-run", "repo", "clone", repo_address]
        with patch.object(sys, "argv", test_args):
            with StringIO() as buf, redirect_stdout(buf):
                gh_main()
                output = buf.getvalue()
                self.assertIn(
                    "Dry run: would clone github.com/octocat/Hello-World into", output
                )

    def test_dry_run_clone_default(self):
        repo_address = "github.com/octocat/Hello-World"
        test_args = ["ghw.py", "--default", "--dry-run", "repo", "clone", repo_address]
        with patch.object(sys, "argv", test_args):
            with StringIO() as buf, redirect_stdout(buf):
                gh_main()
                output = buf.getvalue()
                self.assertIn(
                    f"Dry run: would execute `gh repo clone {repo_address}`", output
                )

    def test_dry_run_other(self):
        test_args = ["ghw.py", "--dry-run", "auth", "login"]
        with patch.object(sys, "argv", test_args):
            with StringIO() as buf, redirect_stdout(buf):
                gh_main()
                output = buf.getvalue()
                self.assertIn("Dry run: would execute `gh auth login`", output)


if __name__ == "__main__":
    unittest.main()

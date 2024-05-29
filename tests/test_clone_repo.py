import shutil
import unittest
import subprocess
from pathlib import Path
from src.github.clone_repo import clone_repo


class TestCloneRepo(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path("/tmp/gh_test")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.base_dir.exists() and self.base_dir.is_dir():
            shutil.rmtree(self.base_dir)

    def test_clone_repo(self):
        domain, owner, repo = "github.com", "octocat", "Hello-World"
        try:
            clone_repo(domain, owner, repo, self.base_dir)
            target_dir = self.base_dir / domain / owner / repo
            self.assertTrue(target_dir.exists())
        except subprocess.CalledProcessError:
            self.fail(
                "gh command failed. Ensure gh CLI is installed and authenticated."
            )


if __name__ == "__main__":
    unittest.main()

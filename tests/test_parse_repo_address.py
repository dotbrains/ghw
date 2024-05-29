import unittest
from src.ghw import parse_repo_address


class TestParseRepoAddress(unittest.TestCase):
    def test_parse_repo_address(self):
        repo_address = "github.com/octocat/hello-world"
        domain, owner, repo = parse_repo_address(repo_address)

        self.assertEqual(domain, "github.com")
        self.assertEqual(owner, "octocat")
        self.assertEqual(repo, "hello-world")


if __name__ == "__main__":
    unittest.main()

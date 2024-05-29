import shutil
import subprocess
from pathlib import Path

# Find the absolute path of the GitHub CLI
gh_cli_path = shutil.which("gh")
if gh_cli_path is None:
    raise FileNotFoundError(
        "The gh CLI is not installed. Please install it from https://cli.github.com/"
    )


def clone_repo(domain, owner, repo, base_dir):
    """
    Clone a GitHub repository into a specified directory.
    :param domain: The domain of the repository
    :param owner: The owner of the repository
    :param repo: The name of the repository
    :param base_dir: The base directory to clone the repository into
    :return: None
    """
    target_dir = Path(base_dir) / domain / owner / repo
    target_dir.mkdir(parents=True, exist_ok=True)
    clone_url = f"https://{domain}/{owner}/{repo}.git"

    subprocess.run(
        [gh_cli_path, "repo", "clone", clone_url, str(target_dir)], check=True
    )

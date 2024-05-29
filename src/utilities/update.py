import os
import subprocess
from pathlib import Path

import requests


def get_latest_release(repo):
    """
    Get the latest release of a GitHub repository.
    :param repo: The repository in the format owner/repo
    :return: The latest release
    """
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_file(url, dest):
    """
    Download a file from a URL to a destination.
    :param url: The URL of the file
    :param dest: The destination path
    :return: None
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


def get_current_version(cli_path):
    """
    Get the current version of the installed CLI.
    :param cli_path: Path to the CLI executable
    :return: Current version as a string
    """
    try:
        result = subprocess.run(
            [cli_path, "--version"], capture_output=True, text=True, check=True
        )
        # Assuming version output is in the form "cli_name version x.y.z"
        return result.stdout.strip().split(" ")[-1]
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def update_cli():
    """
    Update the GitHub Wrapper CLI to the latest version.
    :return: None
    """
    repo = "dotbrains/ghw"
    current_path = Path(__file__).resolve().parent / "ghw"
    current_version = get_current_version(current_path)

    release = get_latest_release(repo)
    latest_version = release["tag_name"]

    if current_version == latest_version:
        print("CLI is already up to date.")
        return

    asset = next(asset for asset in release["assets"] if asset["name"] == "ghw")
    download_url = asset["browser_download_url"]
    download_path = Path(__file__).resolve().parent / "ghw_latest"

    print(f"Downloading the latest release from {download_url}")
    download_file(download_url, download_path)
    os.replace(download_path, current_path)
    os.chmod(current_path, 0o755)
    print(f"CLI has been updated to version {latest_version}.")

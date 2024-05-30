import argparse
import os
import shutil
import subprocess

from src.github.clone_repo import clone_repo
from src.github.parse_repo_address import parse_repo_address
from src.utilities.obtain_version import obtain_version
from src.utilities.update import update_cli


def parse_arguments():
    """
    Parse the command line arguments.
    :return: The parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="A wrapper for the GitHub CLI with enhanced clone functionality."
    )
    parser.add_argument("command", help="The gh command to run")
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        default=False,
        help="Update the CLI to the latest " "release",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print the command without executing it",
    )
    parser.add_argument(
        "--default",
        action="store_true",
        default=False,
        help="Use the default behavior for the " "clone command",
    )
    parser.add_argument(
        "-d", "--dir", help="The base directory to clone repositories into"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s (version {obtain_version()})",
    )
    parser.add_argument(
        "args", nargs=argparse.REMAINDER, help="Arguments for the gh command"
    )

    return parser.parse_args()


def check_gh_cli_installed():
    """
    Check if the gh CLI is installed.
    :return: None
    """
    try:
        subprocess.run(
            ["gh", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "The gh CLI is not installed. Please install it from https://cli.github.com/"
        ) from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            "The gh CLI is not installed. Please install it from https://cli.github.com/"
        ) from e


def handle_clone_repo(args):
    """
    Handle the cloning of a repository.
    :param args: The parsed arguments
    :return: None
    """
    if len(args.args) < 2:
        raise ValueError(
            "The clone command requires a repository address in the format domain/owner/repo."
        )

    repo_address = args.args[1]
    domain, owner, repo = parse_repo_address(repo_address)
    base_dir = "~/gh"  # Default base directory

    # Check for optional -d/--dir argument
    if "-d" in args.args:
        base_dir = args.args[args.args.index("-d") + 1]
    elif "--dir" in args.args:
        base_dir = args.args[args.args.index("--dir") + 1]

    if os.environ.get("GHW_BASE_DIR"):
        base_dir = os.environ.get("GHW_BASE_DIR")

    if args.dry_run:
        print(f"Dry run: would clone {domain}/{owner}/{repo} into {base_dir}")
        return

    base_dir = os.path.expanduser(base_dir)
    if not os.path.exists(base_dir):
        raise ValueError(f"The base directory '{base_dir}' does not exist.")

    clone_repo(domain, owner, repo, base_dir)


def main():
    """
    The main function.
    :return: None
    """
    args = parse_arguments()
    check_gh_cli_installed()

    # Find the absolute path of the GitHub CLI
    gh_cli_path = shutil.which("gh")
    if gh_cli_path is None:
        raise FileNotFoundError(
            "The gh CLI is not installed. Please install it from https://cli.github.com/"
        )

    if args.update:
        update_cli()
        return

    if (
        args.command == "repo"
        and len(args.args) > 0
        and args.args[0] == "clone"
        and not args.default
    ):
        handle_clone_repo(args)
        return

    if args.dry_run:
        print(f"Dry run: would execute `gh {args.command} {' '.join(args.args)}`")
        return

    # Pass through to the official gh CLI using the absolute path
    subprocess.run([gh_cli_path, args.command] + args.args)


if __name__ == "__main__":
    main()

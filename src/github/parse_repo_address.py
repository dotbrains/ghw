def parse_repo_address(repo_address):
    """
    Parse the repository address into its domain, owner, and repo parts.
    :param repo_address: The repository address
    :return: The domain, owner, and repo parts
    """
    parts = repo_address.split("/")

    if len(parts) != 3:
        raise ValueError(
            "Invalid repository address. Format should be domain/owner/repo."
        )

    domain, owner, repo = parts

    # Remove .git from the repo name if it exists
    if repo.endswith(".git"):
        repo = repo[:-4]

    return domain, owner, repo

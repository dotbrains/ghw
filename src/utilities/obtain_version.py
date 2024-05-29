# Read version from setup.py
import os


def obtain_version():
    """
    Obtain the version from setup.py
    :return: The version
    """
    # Locate the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Move up to the root directory of the project
    root_dir = os.path.abspath(
        os.path.join(current_dir, "../../")
    )  # go up three directories
    setup_path = os.path.join(root_dir, "setup.py")

    if not os.path.exists(setup_path):
        raise FileNotFoundError(f"Could not find setup.py at {setup_path}")

    with open(setup_path) as f:
        for line in f:
            # sometimes version specification is among other text, so a more flexible check is useful
            if "version=" in line:
                return line.split("=")[1].strip().strip("\"'")

    raise ValueError("Could not find version in setup.py")

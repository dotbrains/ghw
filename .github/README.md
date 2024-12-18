# ghw [![Build, Test, and Release](https://github.com/dotbrains/ghw/actions/workflows/release.yml/badge.svg)](https://github.com/dotbrains/ghw/actions/workflows/release.yml)

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/-Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/-macOS-000000?style=flat-square&logo=apple&logoColor=white)
![GitHub CLI](https://img.shields.io/badge/-GitHub_CLI-181717?style=flat-square&logo=github&logoColor=white)
![OpenAI](https://img.shields.io/badge/-OpenAI-FF0084?style=flat-square&logo=openai&logoColor=white)

`ghw` is a command-line tool that acts as a wrapper around the official GitHub CLI (`gh`). It provides enhanced functionality for cloning repositories into a specified directory structure while passing through all other commands to the official `gh` CLI.

## Features

- **Enhanced Cloning**: Clone repositories into a structured directory format based on the domain, owner, and repository name.
- **Pass-Through Commands**: For any commands other than `gh repo clone`, it acts as a pass-through to the official `gh` CLI.
- **Cross-Platform**: PyInstaller can generate executables for different platforms. Ensure you build the executable on the target platform (e.g., build on Linux for a Linux executable).
- **Dry Run**: Perform a dry run of any command to see what would happen without making any changes.
- **Update**: Update the CLI wrapper to the latest release from GitHub.

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/dotbrains/ghw.git
    cd ghw
    ```

	or using `gh`:
	```sh
	gh repo clone dotbrains/ghw
	cd ghw
	```

2. Install the package:
    ```sh
    pip install .
    ```

### Building the Binary

1. Install `PyInstaller`:
    ```sh
    pip install pyinstaller
    ```

2. Build the binary executable:
    ```sh
    pyinstaller --onefile src/ghw.py --name ghw
    ```

3. Move the executable to the project root (optional):
    ```sh
    mv dist/ghw .
    ```

4. Make the executable file executable:
	```sh
	chmod +x ghw
	```

Ensure the `ghw` command is in your PATH:

```sh
export PATH=$PATH:/path/to/ghw
```

## Usage

### Cloning Repositories

To clone a repository into the specified directory structure:

```sh
ghw [--default] [--dry-run] repo clone <domain/owner/repo> [-d <base_directory>]
ghw [--update]
```

- `domain`: The domain of the repository (e.g., `github.com`).
- `owner`: The owner of the repository.
- `repo`: The name of the repository.
- `-d`, `--dir` (optional): The base directory to clone repositories into (default is `~/gh`).
- `--default` (optional): Clone the repository using the default behavior of `gh` CLI.
- `--dry-run` (optional): Print the command without executing it.
- `--update` (optional): Update the CLI to the latest release.

⚠️ **Note**: If `GHW_BASE_DIR` is set in the environment, it will be used as the default base directory.

**Examples**:

```sh
ghw repo clone github.com/octocat/Hello-World -d /path/to/base/dir
```

This will clone the repository into `/path/to/base/dir/github.com/octocat/Hello-World`.

```sh
export GH_BASE_DIR=/path/to/base/dir && ghw repo clone github.com/octocat/Hello-World
```

This will clone the repository into `/path/to/base/dir/github.com/octocat/Hello-World`.

```sh
ghw --default repo clone github.com/octocat/Hello-World -d /path/to/base/dir
```

This will clone the repository into `current-directory/Hello-World`. This is because the `--default` flag is used to clone the repository using the default behavior of `gh` CLI.

```sh
ghw --default --dry-run repo clone github.com/octocat/Hello-World -d /path/to/base/dir
```

This will print the command without executing it because of the use of the `--dry-run` flag.

### Commit using AI

You can use AI services to generate commit messages with the `ghw` CLI tool. The command supports selecting between ChatGPT and Claude for generating messages, with an optional mode for Claude’s Sonnet.

To generate commit messages using AI services, run:

```sh
ghw commit [--chatgpt | --claude [--sonnet]] [--dry-run] [--openai-api-key YOUR_OPENAI_KEY] [--anthropic-api-key YOUR_ANTHROPIC_KEY] [-m "Your commit message"]
```

#### Options

- `--chatgpt` (optional): Use ChatGPT to generate the commit message. This option requires an OpenAI API key.
- `--claude` (optional): Use Claude to generate the commit message. This option requires an Anthropic API key.
- `--sonnet` (optional): Use Claude with the Sonnet mode for generating the commit message. **Requires** `--claude` to be specified.
- `--dry-run` (optional): Print the command and generated commit message without executing it.
- `--openai-api-key` (optional): Specify your OpenAI API key directly for the ChatGPT service. If not provided, the `OPENAI_API_KEY` environment variable will be used.
- `--anthropic-api-key` (optional): Specify your Anthropic API key directly for the Claude service. If not provided, the `ANTHROPIC_API_KEY` environment variable will be used.
- `-m`, `--message` (optional): Specify the commit message directly, bypassing AI generation.

#### Notes

1. **Choose Only One AI Service**: You must select only one of `--chatgpt` or `--claude`. Using both options together will result in an error.
2. **Using Sonnet with Claude**: The `--sonnet` option can only be used if `--claude` is also specified. It will raise an error if used without `--claude`.
3. **Custom Message**: If `-m` or `--message` is provided with a commit message, the specified message will be used directly, and no AI generation will occur.
4. **API Key Requirement**: Each AI service requires its respective API key. If the API key is not provided via command line (`--openai-api-key` or `--anthropic-api-key`), the tool will attempt to use the appropriate environment variable.
5. **Environment Variables**:
	- If not passing API keys directly, ensure `OPENAI_API_KEY` is set for ChatGPT or `ANTHROPIC_API_KEY` is set for Claude in your environment.
6. **Dry Run Mode**: To see the generated commit message without committing, use `--dry-run`. This is useful for previewing the commit message.

#### Environment Variables

To set the API keys as environment variables:

```sh
export OPENAI_API_KEY=YOUR_OPENAI_KEY
export ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY
```

This command provides a streamlined way to generate commit messages with AI, allowing you to select your preferred service or use your own message directly, based on your workflow needs.

### Pass-Through Commands

For any other `gh` commands, it functions as a pass-through to the official `gh` CLI:

```sh
gh <command> [args...]
```

**Examples**:

```sh
ghw auth login
ghw repo view octocat/Hello-World
```

## Development

### Running Tests

To run the tests:

```sh
python -m unittest discover -s tests
```

### Project Structure

```
project_root/
│
├── src/
│   ├── ai/
│   │   ├── services/
│   │   │   ├── chatgpt_service.py
│   │   │   ├── claude_service.py
│   │   ├── ai_service.py
│   │   ├── ai_service_factory.py
│   │   ├── commit.py
│   ├── github/
│   │   ├── clone_repo.py
│   │   ├── parse_repo_address.py
│   ├── utilities/
│   │   ├── obtain_version.py
│   │   ├── update.py
│   ├── ghw.py
│
├── tests/
│   ├── test_clone_repo.py
│   ├── test_dry_run.py
│   ├── test_update.py
│   ├── test_parse_repo_address.py
│
├── .pre-commit-config.yaml
├── build/   # Generated by PyInstaller
├── dist/    # Generated by PyInstaller
├── ghw      # The executable binary
├── setup.py
└── README.md
```

### Explanation:

-  **src/**: This is the main source directory.
- **ai/**: Contains AI-related functionality.
	- **services/**: Contains AI services.
		- `chatgpt_service.py`: ChatGPT service logic.
		- `claude_service.py`: Claude service logic.
	- `ai_service.py`: AI service logic.
	- `ai_service_factory.py`: Factory for creating AI services.
    - `commit.py`: Logic for handling commits using AI services.
- **github/**: Contains GitHub-related functionality.
	- `clone_repo.py`: Logic for cloning repositories.
	- `parse_repo_address.py`: Logic for parsing repository addresses.
- **utilities/**: Contains utility scripts.
	- `obtain_version.py`: Script to obtain version details.
	- `update.py`: Script to handle updates.
- `ghw.py`: The main wrapper script.
-  **tests/**: Contains test scripts.
- `test_clone_repo.py`: Test cases for the clone repo functionality.
- `test_dry_run.py`: Test cases for the dry run functionality.
- `test_update.py`: Test cases for the update functionality.
- `test_parse_repo_address.py`: Test cases for the parse repo address functionality.
- **.pre-commit-config.yaml**: Configuration file for pre-commit hooks.
-  **build/**: Directory for PyInstaller build artifacts.
-  **dist/**: Directory for PyInstaller distribution artifacts.
-  **ghw**: The compiled/executable binary.
-  **setup.py**: The setup script for packaging.
-  **README.md**: Project documentation.

## GitHub Actions Workflow

This project includes a GitHub Actions workflow that automatically builds a new binary and creates a release on GitHub whenever a new tag is pushed that matches the pattern `v*.*.*`.

### How It Works

1. **Trigger**: The workflow is triggered on push events to tags that match the pattern `v*.*.*`.

2. **Build Job**:
	- **Checkout repository**: Clones the repository to the runner.
	- **Set up Python**: Sets up the Python environment with the specified version.
	- **Install dependencies**: Installs `pyinstaller` and other required Python packages.
	- **Install GitHub CLI (Linux only)**: Installs GitHub CLI on Linux runners.
	- **Authenticate GitHub CLI**: Authenticates GitHub CLI using a GitHub token.
	- **Run tests**: Runs unit tests to ensure the code quality.
	- **Inject version and build executable**: Injects the version into the code and builds the executable using `pyinstaller`.
	- **Archive binary**: Archives the built binary for later steps.

3. **Release Job**:
	- **Checkout repository**: Clones the repository to the runner.
	- **Extract tag name**: Extracts the tag name from the GitHub reference.
	- **Create GitHub Release**: Creates a new release on GitHub with the extracted tag name.
	- **Save upload URL**: Saves the upload URL for the release asset.
	- **Upload upload_url artifact**: Uploads the URL to an artifact to be used in the next job.

4. **Upload Assets Job**:
	- **Checkout repository**: Clones the repository to the runner.
	- **Download binary**: Downloads the archived binary from the build job.
	- **Download upload_url artifact**: Downloads the artifact containing the upload URL.
	- **Read upload_url**: Reads the upload URL from the artifact and sets it as an environment variable.
	- **Upload Release Asset**: Uploads the built binary to the GitHub release as an asset.

This workflow ensures that each step in the process of building, testing, and releasing a new version of the software is automated and consistently executed.

### Creating a Release

To create a new release, push a new tag that matches the pattern `v*.*.*`. For example:

```sh
git tag v1.0.0
git push origin v1.0.0
```

This will trigger the GitHub Actions workflow, build the binary, and create a new release on GitHub with the binary attached.

## Git Commit Hook for Code Formatting

This project uses `pre-commit` to manage git commit hooks. We use [`black`](https://github.com/psf/black) for code formatting python files.

### Setup

Install pre-commit:

```sh
pip install pre-commit
```

Install the pre-commit hooks:

```sh
pre-commit install
```

### Usage

The `pre-commit` hook will automatically format your code using `black` before each commit. If any files are reformatted, the commit will be aborted, and you will need to stage the changes and commit again.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgements

- The official [GitHub CLI](https://github.com/cli/cli) for providing the base functionality.

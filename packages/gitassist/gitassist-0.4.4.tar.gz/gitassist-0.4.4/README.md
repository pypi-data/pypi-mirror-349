# GitAssist
GitAssist is a command-line tool that uses OpenAI to generate commit messages and pull
request descriptions based on your Git history and staged changes. It streamlines your Git
workflow by suggesting clear, concise, and contextually appropriate messages.

## Features
- Automatically generate commit messages from staged changes
- Automatically generate PR titles and descriptions from commit history
- Push the current branch and open the PR creation page on GitHub or GitLab

## Installation

### Using pipx (Recommended)

`pipx` allows you to install and run Python applications in isolated environments, ensuring that your system Python packages remain untouched.

- **On macOS (using Homebrew):**

  ```bash
  brew install pipx
  pipx ensurepath
  ```

  After running `pipx ensurepath`, restart your terminal to apply the changes.

- **On Linux (Debian/Ubuntu):**

  ```bash
  sudo apt update
  sudo apt install pipx
  pipx ensurepath
  ```

  After running `pipx ensurepath`, restart your terminal to apply the changes.

- **On Windows:**

  ```powershell
  python -m pip install --user pipx
  python -m pipx ensurepath
  ```

  After running `pipx ensurepath`, restart your terminal to apply the changes.

For more detailed instructions, refer to the official pipx installation guide: [pipx.pypa.io](https://pipx.pypa.io/stable/installation/)

- **Install Command**
  ```bash
  pipx install gitassist
  ```

## Usage

### Initialize the tool with your OpenAI API key
```bash
gitassist init
```

![init example](https://github.com/user-attachments/assets/d97f717b-3556-4ee6-bb65-419902fd27b2)

### Generate and commit with an AI-suggested message
```bash
gitassist commit
```

Opens your default system editor with a pre-filled commit message. Edit as needed, save, and close the editor to proceed with the commit.

![commit example](https://github.com/user-attachments/assets/34952188-3295-41e3-bac6-684cbef6abab)

### Generate a PR title and description, push your branch, and open the PR page
```bash
gitassist new-pr --base main
```

Pushes your local branch and opens the GitHub or GitLab new pull request page with a generated title and description. You can review, edit, and publish your PR!

![new pr example](https://github.com/user-attachments/assets/8fac952c-f6fb-403f-9e19-cbd55a4e8564)

## Requirements
- Python 3.7+
- `git` must be installed and available on your system path
- A valid OpenAI API key

## Assumptions
GitAssist assumes a few things about your development workflow:

1. **Branching Model**: You are working on a feature branch that diverged from a long-lived base branch like `main`.
2. **Staging Area**: When running `gitassist commit`, you have already staged your changes.
3. **Remote Setup**: You have a remote named `origin` pointing to a GitHub or GitLab repository.
4. **Authentication**: You are authenticated with the remote (e.g., via SSH or HTTPS credentials) and have permission to push.
5. **Push Before PR**: Your local branch does not need to be pushed manually before PR creation — GitAssist pushes it for you.
6. **Platform Detection**: GitAssist can detect whether you're using GitHub or GitLab based on your `origin` URL.

## License
MIT License

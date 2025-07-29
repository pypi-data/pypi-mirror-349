import os
import click
import subprocess
import urllib.parse
import json
import webbrowser
from git import Repo, GitCommandError
from openai import OpenAI

CONFIG_FILE = os.path.expanduser("~/.git_ai_helper_config")
MAX_DIFF_CHARS = 2000

def load_api_key():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return f.read().strip()

def save_api_key(api_key):
    with open(CONFIG_FILE, 'w') as f:
        f.write(api_key)

def get_staged_files():
    result = subprocess.run(['git', 'diff', '--cached', '--name-only'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().split('\n')

def get_file_diff(file_path):
    result = subprocess.run(['git', 'diff', '--cached', '--', file_path], stdout=subprocess.PIPE, text=True)
    return result.stdout

def summarize_diff(api_key, file_path, diff_text):
    prompt = (
        f"Summarize the changes in the following git diff for the file `{file_path}`. "
        "Respond with a one-line summary of what was changed.\n\n"
        f"{diff_text}"
    )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def suggest_commit_message(api_key, summaries):
    summary_text = "\n".join(f"- {s}" for s in summaries)
    prompt = (
        "Given these file change summaries, generate a one-line commit message using the imperative mood (e.g. ‘Add support for X’, ‘Fix crash when Y’). Focus on the purpose of the change, not how it was implemented. Do not include any punctuation at the end. \n"
        """Examples:
            - Fix login redirect logic
            - Add retry handling to API calls
            - Refactor job scheduler pipeline

            Commit messages:
            ...\n"""
        f"{summary_text}"
    )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def get_current_branch(repo):
    return repo.active_branch.name

def get_commits_since_branch_point(repo, base_branch='main'):
    current_branch = get_current_branch(repo)
    try:
        merge_base = repo.git.merge_base(base_branch, current_branch)
    except GitCommandError:
        raise ValueError(f"Base branch '{base_branch}' not found or no common ancestor with '{current_branch}'.")
    commits = list(repo.iter_commits(f'{merge_base}..{current_branch}'))
    return commits

@click.group()
def cli():
    pass

@cli.command(name='init')
def init_command():
    """Initialize and store OpenAI API token."""
    api_key = click.prompt("Enter your OpenAI API key", hide_input=True)
    save_api_key(api_key)
    click.echo("API key saved successfully.")

@cli.command(name='commit')
def commit_command():
    """Generate a recommended commit message, allow edits, and commit."""
    api_key = load_api_key()
    if not api_key:
        click.echo("API key not found. Please run 'gitprompt init' first.")
        return

    try:
        repo = Repo(os.getcwd(), search_parent_directories=True)
        repo_path = repo.git.rev_parse("--show-toplevel")
        os.chdir(repo_path)
    except Exception as e:
        click.echo(f"Error accessing Git repository: {e}")
        return

    staged_files = get_staged_files()
    if not staged_files or staged_files == ['']:
        click.echo("No staged files to process.")
        return

    summaries = []
    for file in staged_files:
        diff = get_file_diff(file)
        if len(diff) > MAX_DIFF_CHARS:
            summary = f"Modified `{file}` (diff too large to analyze, falling back to filename-level summary)"
            summaries.append(summary)
        else:
            if diff.strip():
                click.echo(f"Summarizing changes in {file}...")
                summary = summarize_diff(api_key, file, diff)
                summaries.append(summary)

    if not summaries:
        click.echo("No summaries generated. Aborting commit.")
        return

    commit_message = suggest_commit_message(api_key, summaries)

    edited_message = click.edit(text=commit_message)
    if edited_message is None:
        click.echo("Commit message edit canceled.")
        return

    try:
        subprocess.run(['git', 'commit', '-m', edited_message], check=True)
        click.echo("Changes committed successfully.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error during git commit: {e}")

@cli.command(name='new-pr')
@click.option('--base', required=True, help='Base branch to compare against.')
def new_pr_command(base):
    """Generate a recommended PR title and description based on new commits."""
    api_key = load_api_key()
    if not api_key:
        click.echo("API key not found. Please run 'gitprompt init' first.")
        return

    try:
        repo = Repo(os.getcwd(), search_parent_directories=True)
    except Exception as e:
        click.echo(f"Error accessing Git repository: {e}")
        return

    current_branch = get_current_branch(repo)
    if current_branch == base:
        click.echo(f"Current branch is the same as base branch '{base}'. Please switch to a feature branch.")
        return

    if 'origin' not in [remote.name for remote in repo.remotes]:
        click.echo("No remote named 'origin' found in this repository.")
        return

    try:
        subprocess.run(['git', 'push', '--set-upstream', 'origin', current_branch], check=True)
        click.echo(f"Branch '{current_branch}' pushed to remote 'origin'.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error pushing branch '{current_branch}' to remote 'origin': {e}")
        return

    try:
        commits = get_commits_since_branch_point(repo, base_branch=base)
    except ValueError as e:
        click.echo(str(e))
        return

    if not commits:
        click.echo("No new commits found compared to the base branch.")
        return

    commit_messages = "\n".join(f"- {commit.message.strip()}" for commit in reversed(commits))
    title_prompt = (
        """
        Generate a concise pull request title based on the following commit messages.

        Requirements:
        - Use active voice and imperative mood (e.g. "Add", "Fix", "Update")
        - Do not include punctuation or markdown
        - Do not prefix with "PR" or "This change..."
        - Keep under 60 characters

        Examples:
        - Add environment validation to deployment script
        - Fix redirect issue in auth callback
        - Refactor logging and error handling
        - Remove unused config fields
        - Support GitLab remote detection

        Commit messages:
        <...>
        """
        f"{commit_messages}"
    )

    description_prompt = ("""
        Generate a pull request description for engineers.

        Requirements:
        - Start with `# Description`
        - Use bullet points
        - Focus on what changed and why it matters
        - Avoid implementation details, intros, or marketing language
        - Do not restate the commit messages
        - Use plain markdown with no headers or boilerplate

        Examples:
        - Add input validation to CLI arguments to prevent crashes
        - Remove support for CNAB worker deployment (deprecated)
        - Improve developer experience by simplifying flag parsing

        Commit messages:
        """
        f"{commit_messages}"
    )

    client = OpenAI(api_key=api_key)
    try:
        title_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": title_prompt}],
            max_tokens=300,
            temperature=0.5
        )
        title_content = title_response.choices[0].message.content.strip()

        description_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": description_prompt}],
            max_tokens=300,
            temperature=0.5
        )
        description_content = description_response.choices[0].message.content.strip()

        description = f"{description_content}"

        origin_url = repo.remotes.origin.url
        if 'github.com' in origin_url:
            platform = 'github'
        elif 'gitlab.com' in origin_url:
            platform = 'gitlab'
        else:
            click.echo("Unsupported remote hosting platform.")
            return

        if origin_url.startswith("git@"):
            path = origin_url.split(":", 1)[1]
        elif origin_url.startswith("https://"):
            path = origin_url.split("github.com/")[1]
        else:
            click.echo("Unsupported remote URL format.")
            return
        owner_repo = path.replace(".git", "")

        if platform == 'github':
            owner, repo_name = owner_repo.split("/")
            pr_url = (
                f"https://github.com/{owner}/{repo_name}/compare/{base}...{current_branch}"
                f"?quick_pull=1&title={urllib.parse.quote(title_content)}&body={urllib.parse.quote(description)}"
            )
        elif platform == 'gitlab':
            pr_url = (
                f"https://gitlab.com/{owner_repo}/-/merge_requests/new"
                f"?merge_request[source_branch]={urllib.parse.quote(current_branch)}"
                f"&merge_request[target_branch]={urllib.parse.quote(base)}"
                f"&merge_request[title]={urllib.parse.quote(title_content)}"
                f"&merge_request[description]={urllib.parse.quote(description)}"
            )

        click.echo(f"Recommended PR Title:\n{title_content}\n")
        click.echo(f"Recommended PR Description:\n{description}\n")
        click.echo(f"Opening the following URL to create the pull request:\n{pr_url}")
        webbrowser.open(pr_url)
    except Exception as e:
        click.echo(f"Error generating pull request suggestion: {e}")

if __name__ == '__main__':
    cli()

from typing import Optional

import inquirer
import subprocess

import typer
from jira import Issue

from ttool.jira_utils.utils import get_my_issues


def generate_github_branch_from_issue(issue: Issue) -> str:
    s = ''.join(ch for ch in issue.get_field('summary') if ch.isalnum() or ch.isalpha() or ch == ' ')
    return f"{issue.key}/{'-'.join(s.split())}"


def get_issue_to_github_selector() -> Optional[str]:
    issues = get_my_issues()

    if not issues:
        typer.echo("You have no issues assigned to you")
        raise typer.Exit()

    choices = {issue: f"{issue.key} - {issue.get_field('status')} - {issue.get_field('summary')}" for issue in issues}
    questions = [
        inquirer.List(
            'issue',
            message="Pick your jira issue",
            choices=choices.values(),
        ),
    ]
    answers = inquirer.prompt(questions)

    if not answers:
        return

    for issue, choice in choices.items():
        if choice == answers['issue']:
            return generate_github_branch_from_issue(issue)


def run_jira_issue_to_github_branch(should_print: bool):
    branch_name = get_issue_to_github_selector()
    if not branch_name:
        return

    if should_print:
        print(branch_name)

    else:
        subprocess.Popen(["git", "checkout", "-b", branch_name])


def checkout(print: bool = False):
    """Checkout/Print your chosen jira issue with 'ISSUE-ID/the-issue-summery' format.
    use --print to print the branch name without checkout"""
    run_jira_issue_to_github_branch(should_print=print)


if __name__ == '__main__':
    typer.run(checkout)

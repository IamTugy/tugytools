""" Checkout/Print your chosen jira issue with 'ISSUE-ID/the-issue-summery' format.

    Usage:
        jira_issue_to_github_branch.py [--checkout | --print]
        jira_issue_to_github_branch.py (-h | --help)

    Options:
        -h --help   Show this screen.
        --checkout  Git Checkout -b to the desired branch
        --print     Print how would the desired branch called
"""

import inquirer
import subprocess
from docopt import docopt
from jira import Issue

from jira_utils.scripts.utils import get_my_issues


def generate_github_branch_from_issue(issue: Issue) -> str:
    s = ''.join(ch for ch in issue.get_field('summary') if ch.isalnum() or ch.isalpha() or ch == ' ')
    return f"{issue.key}/{'-'.join(s.split())}"


def get_issue_to_github_selector() -> str:
    issues = get_my_issues()

    if not issues:
        print("You have no issues assigned to you")
        raise

    choices = {issue: f"{issue.key} - {issue.get_field('status')} - {issue.get_field('summary')}" for issue in issues}
    questions = [
        inquirer.List(
            'issue',
            message="Pick your jira issue",
            choices=choices.values(),
        ),
    ]
    answers = inquirer.prompt(questions)
    for issue, choice in choices.items():
        if choice == answers['issue']:
            return generate_github_branch_from_issue(issue)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    should_print = arguments.get('--print')
    should_checkout = arguments.get('--checkout')

    if should_checkout or should_print:
        branch_name = get_issue_to_github_selector()

        if should_print:
            print(branch_name)

        if should_checkout:
            subprocess.Popen(["git", "checkout", "-b", branch_name])

    else:
        print("You must use --print or --checkout")

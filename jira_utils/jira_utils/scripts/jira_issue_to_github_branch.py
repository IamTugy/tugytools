import inquirer
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
    print(get_issue_to_github_selector())

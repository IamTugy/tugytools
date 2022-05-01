import typer

from jira_utils.scripts.jira_issue_to_github_branch import checkout
from jira_utils.scripts.set_up import setup

jira = typer.Typer()
jira.command()(setup)
jira.command()(checkout)


if __name__ == '__main__':
    jira()

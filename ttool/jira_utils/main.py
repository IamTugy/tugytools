import typer

from ttool.jira_utils.jira_issue_to_github_branch import checkout
from ttool.jira_utils.set_up import setup

jira_app = typer.Typer()
jira_app.command()(setup)
jira_app.command()(checkout)


if __name__ == '__main__':
    jira_app()

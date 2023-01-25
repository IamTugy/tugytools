import inquirer

import typer
from jira import JIRAError

from ttool.jira_utils.utils import CONFIG_FILE, get_config, Config, get_jira_projects, JiraHostType

YES = 'yes'
NO = 'no'


def set_up_jira():
    if CONFIG_FILE.exists():
        questions = [
            inquirer.Confirm(
                'continue',
                message="You are already configured, do you want to configure jira again?",
                default=False
            ),
        ]
        should_continue = inquirer.prompt(questions)['continue']
        if not should_continue:
            return

    default_values = get_config()
    questions = [
        inquirer.Text(
            'server',
            message="Enter your atlassian server (https://some_server.atlassian.net/)",
            default=default_values.server
        ),
        inquirer.List(
            'host_type',
            message="Enter your atlassian host type",
            choices=list(JiraHostType.__members__.keys()),
            default=None
        ),
    ]

    answers = inquirer.prompt(questions)
    server = answers['server']
    if not server:
        typer.secho("Atlassian server was not entered! run set_up again", fg=typer.colors.RED, err=True)
        raise typer.Exit()

    host_type = answers['host_type']
    if not server:
        typer.secho("Atlassian host type was not entered! run set_up again", fg=typer.colors.RED, err=True)
        raise typer.Exit()

    try:
        projects = get_jira_projects(server=server, jira_host_type=host_type)
    except JIRAError:
        typer.secho("The given atlassian server is invalid", fg=typer.colors.RED, err=True)
        raise typer.Exit()

    choices = {project.key: f"{project.key}: {project.name}" for project in projects}
    questions = [
        inquirer.List(
            'project_name',
            message="Pick your team's project key",
            choices=choices.values(),
            default=choices.get(default_values.project_name)
        ),
    ]
    project_name = None
    answer = inquirer.prompt(questions)['project_name']
    for key, choice in choices.items():
        if choice == answer:
            project_name = key

    config = Config(server=server, project_name=project_name, jira_host_type=host_type)
    config.save()


def setup():
    """Set up your jira configurations.
    Before that make sure youve configured this 2 local env variables:
    JIRA_API_TOKEN: create one here - https://id.atlassian.com/manage-profile/security/api-tokens
    JIRA_MAIL: your jira email
    """
    set_up_jira()


if __name__ == '__main__':
    typer.run(setup)

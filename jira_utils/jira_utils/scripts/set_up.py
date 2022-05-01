from dataclasses import asdict

import inquirer

from pathlib import Path

import yaml
from jira import JIRAError

from utils import CONFIG_FILE, get_config, Config, get_jira_projects

YES = 'yes'
NO = 'no'


def set_up_jira():
    config_file = Path(CONFIG_FILE)

    if config_file.exists():
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
    ]

    server = inquirer.prompt(questions)['server']
    if not server:
        print("Atlassian server was not entered! run set_up again")
        return

    try:
        projects = get_jira_projects(server)
    except JIRAError:
        print("The given atlassian server is invalid")
        return

    choices = {project.key: f"{project.key}: {project.name}" for project in projects}
    questions = [
        inquirer.List(
            'project_name',
            message="Pick your team's project key:",
            choices=choices.values(),
            default=choices.get(default_values.project_name)
        ),
    ]
    project_name = None
    answer = inquirer.prompt(questions)['project_name']
    for key, choice in choices.items():
        if choice == answer:
            project_name = key

    config = Config(server=server, project_name=project_name)

    with config_file.open('w') as fp:
        yaml.safe_dump(asdict(config), fp, default_flow_style=False)


if __name__ == '__main__':
    set_up_jira()

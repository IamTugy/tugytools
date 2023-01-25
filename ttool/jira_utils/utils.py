import os

from dataclasses import dataclass, field, asdict
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple, Optional, Union

import typer
from dacite import from_dict
from jira import JIRA, Issue, Project, JIRAError
import yaml


CONFIG_RELATIVE_PATH = Path('.ttool/jira/.config.yaml')
CONFIG_FILE = Path(os.environ['HOME']) / CONFIG_RELATIVE_PATH
JIRA_API_TOKEN = 'JIRA_API_TOKEN'
JIRA_MAIL = 'JIRA_MAIL'


class JiraHostType(Enum):
    Local = "Local"
    Cloud = "Cloud"

    @staticmethod
    def represent(dumper: yaml.Dumper, host_type: "JiraHostType"):
        return dumper.represent_scalar('tag:yaml.org,2002:str', host_type.name)


yaml.add_representer(JiraHostType, JiraHostType.represent)


@dataclass
class Config:
    server: Optional[str] = field(default=None)
    project_name: Optional[str] = field(default=None)
    jira_host_type: Optional[Union[JiraHostType, str]] = field(default=None)

    def save(self):
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with CONFIG_FILE.open('w') as fp:
            yaml.safe_dump(asdict(self), fp, default_flow_style=False)
            typer.secho(f"Config file saved in {CONFIG_FILE}", fg=typer.colors.GREEN)


def get_config() -> Config:
    if not CONFIG_FILE.exists():
        return Config()

    with CONFIG_FILE.open() as fp:
        return from_dict(Config, yaml.safe_load(fp))


def get_auth() -> Tuple[str, str]:
    token_auth = os.environ.get(JIRA_API_TOKEN)
    mail_auth = os.environ.get(JIRA_MAIL)

    if not (token_auth and mail_auth):
        raise f"{JIRA_API_TOKEN} and {JIRA_MAIL} env variables must be configured"

    return token_auth, mail_auth


@lru_cache
def get_jira_client(jira_server_url: str, jira_email: str, jira_api_token: str, jira_host_type: JiraHostType) -> JIRA:
    kwargs = {
        JiraHostType.Local: dict(token_auth=jira_api_token),
        JiraHostType.Cloud: dict(basic_auth=(jira_email, jira_api_token))
    }.get(jira_host_type)
    return JIRA(jira_server_url, **kwargs)


@lru_cache
def get_jira(server: str = None, jira_host_type: str = None) -> JIRA:
    if not server or not jira_host_type:
        config = get_config()
        server = server or config.server
        jira_host_type = jira_host_type or config.jira_host_type
    token_auth, mail_auth = get_auth()

    try:
        jira_host_type = JiraHostType[jira_host_type] if isinstance(jira_host_type, str) else jira_host_type
    except KeyError:
        raise "Host type is not valid"

    jira_client = get_jira_client(
        jira_server_url=server,
        jira_email=mail_auth,
        jira_api_token=token_auth,
        jira_host_type=jira_host_type
    )

    # validate user authentication:
    try:
        jira_client.current_user()
    except JIRAError:
        raise "Client must be authenticated to access this resource"

    return jira_client


def get_my_issues() -> List[Issue]:
    project_name = get_config().project_name
    jira_client = get_jira()
    issues: List[Issue] = []
    i = 0
    chunk_size = 100

    while True:
        chunk = jira_client.search_issues(
            f'assignee = currentUser() and project = {project_name} and status not in (Done, Closed)',
            startAt=i, maxResults=chunk_size
        )
        i += chunk_size
        issues += chunk.iterable
        if i >= chunk.total:
            break
    return issues


def get_jira_projects(server: str = None, jira_host_type: str = None) -> List[Project]:
    jira_client = get_jira(server, jira_host_type)
    return jira_client.projects()

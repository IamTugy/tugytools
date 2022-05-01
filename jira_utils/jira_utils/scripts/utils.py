import os

from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import List, Tuple, Optional

from dacite import from_dict
from jira import JIRA, Issue, Project
import yaml


CONFIG_FILE = 'jira_utils/config.yaml'
JIRA_API_TOKEN = 'JIRA_API_TOKEN'
JIRA_MAIL = 'JIRA_MAIL'


@dataclass
class Config:
    server: Optional[str] = field(default=None)
    project_name: Optional[str] = field(default=None)


def get_config() -> Config:
    config_file = Path(CONFIG_FILE)
    if not config_file.exists():
        return Config()

    with Path(CONFIG_FILE).open() as fp:
        return from_dict(Config, yaml.safe_load(fp))


def get_auth() -> Tuple[str, str]:
    token_auth = os.environ.get(JIRA_API_TOKEN)
    mail_auth = os.environ.get(JIRA_MAIL)

    if not (token_auth and mail_auth):
        raise f"{JIRA_API_TOKEN} and {JIRA_MAIL} env virables must be configured"

    return token_auth, mail_auth


@cache
def get_jira(server: str = None) -> JIRA:
    if not server:
        config = get_config()
        server = config.server
    token_auth, mail_auth = get_auth()
    return JIRA(server, basic_auth=(mail_auth, token_auth))


def get_my_issues() -> List[Issue]:
    project_name = get_config().project_name
    jira_client = get_jira()
    issues: List[Issue] = []
    i = 0
    chunk_size = 100
    while True:
        chunk = jira_client.search_issues(f'assignee = currentUser() and project = {project_name}',
                                          startAt=i, maxResults=chunk_size)
        i += chunk_size
        issues += chunk.iterable
        if i >= chunk.total:
            break
    return issues


def get_jira_projects(server: str = None) -> List[Project]:
    jira_client = get_jira(server)
    return jira_client.projects()

import typer

from ttool.jira_utils.main import jira_app


app = typer.Typer()
app.add_typer(jira_app, name="jira")


if __name__ == '__main__':
    app()

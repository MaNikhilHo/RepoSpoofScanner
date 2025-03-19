import typer
from rich.progress import Progress
from typing import Optional
from ..utils.github_client import AsyncGitHubClient

app = typer.Typer(help="Detect spoofed packages in GitHub repositories")


@app.command()
def scan(
        repo_url: str,
        token: Optional[str] = typer.Option(None, help="GitHub Personal Access Token"),
        output: str = typer.Option("text", help="Output format (text/json)")
):
    """Scan a GitHub repository for suspicious dependencies"""
    with Progress() as progress:
        task = progress.add_task(f"Scanning {repo_url}", total=5)

        # Task for future myself.
    typer.secho("Scan complete!", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
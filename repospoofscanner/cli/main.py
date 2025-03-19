import typer
from rich.console import Console
from typing import Optional
from repospoofscanner.core.scanner import RepoSpoofScanner

app = typer.Typer()
console = Console()


@app.command()
def scan(
        repo_url: str,
        token: Optional[str] = typer.Option(None, help="GitHub Personal Access Token"),
        output: str = typer.Option("text", help="Output format (text/json)")
):
    """Scan a GitHub repository for suspicious packages"""
    scanner = RepoSpoofScanner()
    results = scanner.scan(repo_url, token)

    if output == "json":
        console.print_json(data=results)
    else:
        console.print("\n[bold red]Suspicious Packages Found[/bold red]")
        for pkg in results["invalid"]:
            console.print(f"- {pkg} (not found in registry)")
        for pkg, dist in results["typosquatted"]:
            console.print(f"- {pkg} (similar to known package, distance={dist})")
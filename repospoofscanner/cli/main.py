import typer
from rich.console import Console
from typing import Optional
import asyncio
from repospoofscanner.core.scanner import RepoSpoofScanner

app = typer.Typer(
    help="🛡️ Detect malicious dependencies in GitHub repositories",
    no_args_is_help=True,
    add_completion=False
)
console = Console()


@app.command()
def scan(
        repo_url: str = typer.Argument(..., help="GitHub repository URL"),
        token: Optional[str] = typer.Option(None, "--token", "-t"),
        output: str = typer.Option("text", "--output", "-o")
):
    """Scan a repository for suspicious packages"""
    scanner = RepoSpoofScanner()

    try:
        results = asyncio.run(scanner.scan(repo_url, token))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

    if output.lower() == "json":
        console.print_json(data=results)
    else:
        console.print(f"\n[bold]Scan Results for [link={repo_url}]{repo_url}[/link]:[/bold]")
        if not any(results.values()):
            console.print("[green]✅ No suspicious packages found[/green]")
            return

        if results["invalid"]:
            console.print("[yellow]⚠️ Unregistered Packages:[/yellow]")
            for pkg in results["invalid"]:
                console.print(f"- {pkg}")

        if results["typosquatted"]:
            console.print("\n[red]🚨 Potential Typosquats:[/red]")
            for pkg, score in results["typosquatted"]:
                console.print(f"- {pkg} ({score:.0%} similarity)")


if __name__ == "__main__":
    app()
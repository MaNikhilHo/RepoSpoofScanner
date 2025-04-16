import typer
from rich.console import Console
from typing import Optional
import asyncio
from repospoofscanner.core.scanner import RepoSpoofScanner

# Initialize root command group
app = typer.Typer(
    name="RepoSpoofScanner",
    help="🔍 Security Scanner for GitHub Repositories",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich"
)
console = Console()


@app.command()
def scan(
        repo_url: str = typer.Argument(..., help="[bold green]GitHub repository URL[/bold green]"),
        token: Optional[str] = typer.Option(
            None, "--token", "-t",
            help="GitHub Personal Access Token"
        ),
        output: str = typer.Option(
            "text", "--output", "-o",
            help="Output format: [yellow]text[/yellow] or [yellow]json[/yellow]"
        )
):
    """Scan a repository for suspicious dependencies"""
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
            console.print("[red]🚨 Missing from registries:[/red]")
            for pkg in results["invalid"]:
                console.print(f"- {pkg}")

        if results["typosquatted"]:
            console.print("\n[yellow]⚠️ Similar packages:[/yellow]")
            for pkg, score in results["typosquatted"]:
                console.print(f"- {pkg} ({score:.0%} similarity)")


if __name__ == "__main__":
    app()
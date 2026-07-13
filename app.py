import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from scanner import KubernetesScanner
from rules import RuleEngine
from ai import AIAnalyzer
from delete import ResourceDeleter
from config import config

app = typer.Typer(help="AI Kubernetes Orphan Resource Cleaner")

console = Console()


@app.command()
def scan(delete: bool = typer.Option(False, "--delete", help="Delete approved orphan resources")):
    """
    Scan Kubernetes cluster for orphan PVCs.
    """

    console.rule("[bold cyan]AI Orphan Cleaner")

    console.print("[yellow]Scanning Kubernetes cluster...[/yellow]")

    scanner = KubernetesScanner()
    rule_engine = RuleEngine(
        min_age_days=config.min_resource_age_days
    )
    ai = AIAnalyzer()
    deleter = ResourceDeleter()

    resources = scanner.scan_orphan_pvcs()

    console.print(f"Found {len(resources)} candidate PVCs")

    resources = rule_engine.evaluate(resources)

    if not resources:
        console.print("[green]No orphan resources found.[/green]")
        raise typer.Exit()

    table = Table(title="Orphan Resources")

    table.add_column("Namespace")
    table.add_column("Name")
    table.add_column("Risk")
    table.add_column("Recommendation")

    for resource in resources:

        console.print(
            f"\nAnalyzing {resource.namespace}/{resource.name}..."
        )

        resource = ai.analyze(resource)

        table.add_row(
            resource.namespace,
            resource.name,
            resource.risk.value,
            resource.recommendation or "",
        )

    console.print(table)

    if not delete:
        console.print(
            "\n[yellow]Dry run complete. "
            "Use --delete to remove resources.[/yellow]"
        )
        return

    confirm = typer.confirm(
        "Delete all LOW risk resources?"
    )

    if not confirm:
        console.print("[red]Operation cancelled.[/red]")
        return

    for resource in resources:

        if resource.risk.value != "LOW":
            continue

        deleter.delete(resource)

    console.print(
        Panel.fit(
            "[green]Cleanup complete![/green]"
        )
    )


if __name__ == "__main__":
    app()
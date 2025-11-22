"""Command-line interface for hfsearch."""

import argparse
import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from hfsearch.search import search_models, search_datasets
from hfsearch.export import export_to_csv, export_to_txt

console = Console()


def format_number(num: int) -> str:
    return f"{num:,}"


def create_results_table(results: list, result_type: str) -> Table:
    """Create a formatted table for search results."""
    table = Table(
        title=f" {result_type.capitalize()} Search Results",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        title_style="bold magenta",
    )

    result_type_lower = result_type.lower()
    if result_type_lower == "model" or result_type_lower == "models":
        table.add_column("Model ID", style="cyan", no_wrap=True)
        table.add_column("Author", style="yellow")
        table.add_column("Downloads", style="green", justify="right")
        table.add_column("Likes", style="red", justify="right")
        table.add_column("Tags", style="blue")

        for item in results:
            model_id = item.get("id", "N/A")
            author = item.get("author", "N/A")
            downloads = format_number(item.get("downloads", 0))
            likes = format_number(item.get("likes", 0))
            tags = ", ".join(item.get("tags", [])[:3])
            if len(item.get("tags", [])) > 3:
                tags += "..."

            table.add_row(model_id, author, downloads, likes, tags)
    else:
        table.add_column("Dataset ID", style="cyan", no_wrap=True)
        table.add_column("Author", style="yellow")
        table.add_column("Downloads", style="green", justify="right")
        table.add_column("Likes", style="red", justify="right")
        table.add_column("Tags", style="blue")

        for item in results:
            dataset_id = item.get("id", "N/A")
            author = item.get("author", "N/A")
            downloads = format_number(item.get("downloads", 0))
            likes = format_number(item.get("likes", 0))
            tags = ", ".join(item.get("tags", [])[:3])
            if len(item.get("tags", [])) > 3:
                tags += "..."

            table.add_row(dataset_id, author, downloads, likes, tags)

    return table


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Search for models and datasets on Hugging Face Hub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s models --query "bert"
  %(prog)s models --query "translation" --limit 20
  %(prog)s models --author "google" --limit 5
  %(prog)s datasets --query "sentiment"
  %(prog)s datasets --tags "text-classification" --limit 15
  %(prog)s models --query "bert" --export
  %(prog)s models --query "bert" --export --export-format txt
        """,
    )

    subparsers = parser.add_subparsers(dest="type", help="Type of resource to search")

    models_parser = subparsers.add_parser("models", help="Search for models")
    models_parser.add_argument("--query", "-q", type=str, help="Search query/keywords")
    models_parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=10,
        help="Maximum number of results to return (default: 10)",
    )
    models_parser.add_argument(
        "--author", "-a", type=str, help="Filter by author/organization"
    )
    models_parser.add_argument(
        "--tags", type=str, nargs="+", help="Filter by tags (space-separated)"
    )
    models_parser.add_argument(
        "--task",
        type=str,
        help="Filter by task (e.g., text-classification, translation, etc.)",
    )
    models_parser.add_argument(
        "--export",
        "-e",
        action="store_true",
        help="Export results to CSV file (auto-generates filename)",
    )
    models_parser.add_argument(
        "--export-format",
        choices=["csv", "txt"],
        default="csv",
        help="Export format: csv or txt (default: csv)",
    )

    datasets_parser = subparsers.add_parser("datasets", help="Search for datasets")
    datasets_parser.add_argument(
        "--query", "-q", type=str, help="Search query/keywords"
    )
    datasets_parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=10,
        help="Maximum number of results to return (default: 10)",
    )
    datasets_parser.add_argument(
        "--author", "-a", type=str, help="Filter by author/organization"
    )
    datasets_parser.add_argument(
        "--tags", type=str, nargs="+", help="Filter by tags (space-separated)"
    )
    datasets_parser.add_argument(
        "--export",
        "-e",
        action="store_true",
        help="Export results to CSV file (auto-generates filename)",
    )
    datasets_parser.add_argument(
        "--export-format",
        choices=["csv", "txt"],
        default="csv",
        help="Export format: csv or txt (default: csv)",
    )

    args = parser.parse_args()

    if not args.type:
        parser.print_help()
        sys.exit(1)

    with console.status("[bold green]Searching Hugging Face Hub..."):
        try:
            if args.type == "models":
                results = search_models(
                    query=args.query,
                    limit=args.limit,
                    author=args.author,
                    tags=args.tags,
                    task=args.task,
                )
                result_type = "Model"
            else:
                results = search_datasets(
                    query=args.query,
                    limit=args.limit,
                    author=args.author,
                    tags=args.tags,
                )
                result_type = "Dataset"
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)

    if not results:
        console.print(
            Panel(
                f"[yellow]No {args.type} found matching your criteria.[/yellow]",
                title="No Results",
                border_style="yellow",
            )
        )
        sys.exit(0)

    table = create_results_table(results, args.type)
    console.print("\n")
    console.print(table)
    console.print(f"\n[dim]Found {len(results)} {args.type}[/dim]\n")

    # Export if requested
    if hasattr(args, "export") and args.export:
        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_type_lower = result_type.lower()
        export_format = getattr(args, "export_format", "csv")

        try:
            if export_format == "csv":
                export_file = f"{result_type_lower}s_search_{timestamp}.csv"
                export_to_csv(results, result_type, export_file)
                console.print(f"[green]Results exported to {export_file}[/green]")
            else:
                export_file = f"{result_type_lower}s_search_{timestamp}.txt"
                export_to_txt(results, result_type, export_file)
                console.print(f"[green]Results exported to {export_file}[/green]")
        except Exception as e:
            console.print(f"[red]Error exporting: {e}[/red]")
            sys.exit(1)

    if args.query:
        console.print(
            Panel(
                f"[dim] Tip: Use 'huggingface-cli download <model_id>' to download a model[/dim]",
                border_style="dim",
            )
        )


if __name__ == "__main__":
    main()

"""Export functionality for search results."""

import csv
from typing import List


def format_number(num: int) -> str:
    """Format large numbers with commas."""
    return f"{num:,}"


def export_to_txt(results: List[dict], result_type: str, filename: str) -> None:
    """
    Export results to a text file.
    
    Args:
        results: List of result dictionaries
        result_type: Type of results ("Model" or "Dataset")
        filename: Output filename
    
    Example:
        >>> from hfsearch import search_models, export_to_txt
        >>> results = search_models(query="bert", limit=5)
        >>> export_to_txt(results, "Model", "results.txt")
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"{result_type.capitalize()} Search Results\n")
            f.write("=" * 80 + "\n\n")
            
            for i, item in enumerate(results, 1):
                f.write(f"{i}. {item.get('id', 'N/A')}\n")
                f.write(f"   Author: {item.get('author', 'N/A')}\n")
                f.write(f"   Downloads: {format_number(item.get('downloads', 0))}\n")
                f.write(f"   Likes: {format_number(item.get('likes', 0))}\n")
                tags = item.get("tags", [])
                if tags:
                    f.write(f"   Tags: {', '.join(tags)}\n")
                f.write("\n")
            
            f.write(f"\nTotal: {len(results)} {result_type}\n")
    except Exception as e:
        raise IOError(f"Error exporting to TXT: {e}") from e


def export_to_csv(results: List[dict], result_type: str, filename: str) -> None:
    """
    Export results to a CSV file.
    
    Args:
        results: List of result dictionaries
        result_type: Type of results ("Model" or "Dataset")
        filename: Output filename
    
    Example:
        >>> from hfsearch import search_models, export_to_csv
        >>> results = search_models(query="bert", limit=5)
        >>> export_to_csv(results, "Model", "results.csv")
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if result_type.lower() in ["model", "models"]:
                fieldnames = ['Model ID', 'Author', 'Downloads', 'Likes', 'Tags']
            else:
                fieldnames = ['Dataset ID', 'Author', 'Downloads', 'Likes', 'Tags']
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in results:
                row = {
                    fieldnames[0]: item.get('id', 'N/A'),
                    'Author': item.get('author', 'N/A'),
                    'Downloads': format_number(item.get('downloads', 0)),
                    'Likes': format_number(item.get('likes', 0)),
                    'Tags': ', '.join(item.get('tags', []))
                }
                writer.writerow(row)
    except Exception as e:
        raise IOError(f"Error exporting to CSV: {e}") from e


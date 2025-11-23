# hfsearch

[![PyPI version](https://badge.fury.io/py/hfsearch.svg)](https://badge.fury.io/py/hfsearch)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/hfsearch?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=RED&left_text=downloads)](https://pepy.tech/projects/hfsearch)
[![GitHub stars](https://img.shields.io/github/stars/HenokB/hfsearch?style=social)](https://github.com/HenokB/hfsearch)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Python library and CLI tool to search for models and datasets on the [Hugging Face Hub](https://huggingface.co/).

## Installation

Install from PyPI:

```bash
pip install hfsearch
```

Or install from source:

```bash
git clone https://github.com/yourusername/hfsearch.git
cd hfsearch
pip install -e .
```

## Usage

### As a Library

```python
from hfsearch import search_models, search_datasets, export_to_csv

# Search for models
results = search_models(query="bert", limit=10)
print(f"Found {len(results)} models")
for model in results:
    print(f"{model['id']} - {model['author']}")

# Search for datasets
datasets = search_datasets(query="sentiment", limit=5)
for dataset in datasets:
    print(f"{dataset['id']} - Downloads: {dataset['downloads']}")

# Export results
export_to_csv(results, "Model", "results.csv")
```

### As a CLI Tool

After installation, use the `hfsearch` command:

```bash
# Search for models
hfsearch models --query "bert"

# Search with filters
hfsearch models --query "translation" --limit 20 --author "google"

# Search datasets
hfsearch datasets --query "sentiment" --limit 15

# Export results
hfsearch models --query "bert" --export
hfsearch models --query "bert" --export --export-format txt
```

## Features

- **Search Models**: Find models by keywords, author, tags, or task
- **Search Datasets**: Find datasets by keywords, author, or tags
- **Export Results**: Export search results to CSV or TXT files
- **Beautiful Output**: Formatted terminal output with Rich
- **Python API**: Use as a library in your Python projects

## CLI Examples

### Search Models

```bash
# Search by keyword
hfsearch models --query "bert"

# Search with limit
hfsearch models --query "translation" --limit 20

# Filter by author
hfsearch models --author "google" --limit 5

# Filter by tags
hfsearch models --tags "text-classification" "pytorch"

# Filter by task
hfsearch models --task "text-classification"

# Combine filters
hfsearch models --query "bert" --author "google" --limit 10
```

### Search Datasets

```bash
# Search by keyword
hfsearch datasets --query "sentiment"

# Filter by tags
hfsearch datasets --tags "text-classification" --limit 15

# Filter by author
hfsearch datasets --author "huggingface"
```

### Export Results

```bash
# Export to CSV (default)
hfsearch models --query "bert" --export

# Export to TXT
hfsearch models --query "bert" --export --export-format txt
```

## API Reference

### `search_models(query=None, limit=10, author=None, tags=None, task=None)`

Search for models on Hugging Face Hub.

**Parameters:**
- `query` (str, optional): Search query/keywords
- `limit` (int): Maximum number of results (default: 10)
- `author` (str, optional): Filter by author/organization
- `tags` (list, optional): Filter by tags
- `task` (str, optional): Filter by task (e.g., "text-classification")

**Returns:**
- List of dictionaries with keys: `id`, `author`, `downloads`, `likes`, `tags`

### `search_datasets(query=None, limit=10, author=None, tags=None)`

Search for datasets on Hugging Face Hub.

**Parameters:**
- `query` (str, optional): Search query/keywords
- `limit` (int): Maximum number of results (default: 10)
- `author` (str, optional): Filter by author/organization
- `tags` (list, optional): Filter by tags

**Returns:**
- List of dictionaries with keys: `id`, `author`, `downloads`, `likes`, `tags`

### `export_to_csv(results, result_type, filename)`

Export results to a CSV file.

**Parameters:**
- `results` (list): List of result dictionaries
- `result_type` (str): "Model" or "Dataset"
- `filename` (str): Output filename

### `export_to_txt(results, result_type, filename)`

Export results to a text file.

**Parameters:**
- `results` (list): List of result dictionaries
- `result_type` (str): "Model" or "Dataset"
- `filename` (str): Output filename

## Requirements

- Python 3.7+
- `huggingface_hub>=0.20.0` - For accessing Hugging Face Hub API
- `rich>=13.0.0` - For beautiful terminal output

## Notes

- The tool uses the Hugging Face Hub API, so you need an internet connection
- For downloading models, use the official `huggingface-cli download` command
- Authentication is optional but recommended for private models/datasets

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- GitHub: https://github.com/HenokB/hfsearch
- PyPI: https://pypi.org/project/hfsearch/

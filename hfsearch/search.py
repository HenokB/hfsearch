"""Search functionality for Hugging Face Hub models and datasets."""

from typing import Optional, List
from huggingface_hub import HfApi


def search_models(
    query: Optional[str] = None,
    limit: int = 10,
    author: Optional[str] = None,
    tags: Optional[List[str]] = None,
    task: Optional[str] = None
) -> List[dict]:
    """
    Search for models on Hugging Face Hub.
    
    Args:
        query: Search query/keywords
        limit: Maximum number of results to return (default: 10)
        author: Filter by author/organization
        tags: Filter by tags (list of strings)
        task: Filter by task (e.g., text-classification, translation, etc.)
    
    Returns:
        List of dictionaries containing model information with keys:
        - id: Model ID
        - author: Author/organization
        - downloads: Number of downloads
        - likes: Number of likes
        - tags: List of tags
    
    Example:
        >>> from hfsearch import search_models
        >>> results = search_models(query="bert", limit=5)
        >>> print(results[0]['id'])
        'bert-base-uncased'
    """
    api = HfApi()
    
    try:
        kwargs = {"limit": limit}
        if query:
            kwargs["search"] = query
        if author:
            kwargs["author"] = author
        if tags:
            kwargs["tags"] = tags
        if task:
            kwargs["pipeline_tag"] = task  
        
        results = api.list_models(**kwargs)
        
        model_list = []
        for model in results:
            model_dict = {
                "id": getattr(model, "id", "N/A"),
                "author": getattr(model, "author", "N/A"),
                "downloads": getattr(model, "downloads", 0),
                "likes": getattr(model, "likes", 0),
                "tags": getattr(model, "tags", []),
            }
            model_list.append(model_dict)
        
        return model_list
    except Exception as e:
        raise RuntimeError(f"Error searching models: {e}") from e


def search_datasets(
    query: Optional[str] = None,
    limit: int = 10,
    author: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> List[dict]:
    """
    Search for datasets on Hugging Face Hub.
    
    Args:
        query: Search query/keywords
        limit: Maximum number of results to return (default: 10)
        author: Filter by author/organization
        tags: Filter by tags (list of strings)
    
    Returns:
        List of dictionaries containing dataset information with keys:
        - id: Dataset ID
        - author: Author/organization
        - downloads: Number of downloads
        - likes: Number of likes
        - tags: List of tags
    
    Example:
        >>> from hfsearch import search_datasets
        >>> results = search_datasets(query="sentiment", limit=5)
        >>> print(results[0]['id'])
        'sentiment140'
    """
    api = HfApi()
    
    try:
        kwargs = {"limit": limit}
        if query:
            kwargs["search"] = query
        if author:
            kwargs["author"] = author
        if tags:
            kwargs["tags"] = tags
        
        results = api.list_datasets(**kwargs)
        
        dataset_list = []
        for dataset in results:
            dataset_dict = {
                "id": getattr(dataset, "id", "N/A"),
                "author": getattr(dataset, "author", "N/A"),
                "downloads": getattr(dataset, "downloads", 0),
                "likes": getattr(dataset, "likes", 0),
                "tags": getattr(dataset, "tags", []),
            }
            dataset_list.append(dataset_dict)
        
        return dataset_list
    except Exception as e:
        raise RuntimeError(f"Error searching datasets: {e}") from e


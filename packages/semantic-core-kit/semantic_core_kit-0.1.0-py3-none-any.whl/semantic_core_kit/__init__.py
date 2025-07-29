"""
semantic_core_kit

An AI-Assisted Semantic Core & Article Idea Generator library.

This library provides tools to:
1. Load and clean keywords from a CSV file.
2. Use OpenAI to group keywords into semantic clusters.
3. Generate article ideas (title, type, primary/supporting keywords) for these clusters.
4. Save the generated article ideas to a Markdown file.

Primary entry point: `process_keywords()`

See the individual modules and functions for more detailed documentation.
"""

from .ai_processor import (
    AIClientInterface,
    OpenAIClient,
    generate_article_ideas_from_clusters_with_ai,
    generate_keyword_clusters_with_ai,
)
from .loader import load_and_clean_keywords
from .main import process_keywords
from .utils import save_article_ideas_to_markdown

__all__ = [
    "process_keywords",
    "load_and_clean_keywords",
    "generate_keyword_clusters_with_ai",
    "generate_article_ideas_from_clusters_with_ai",
    "save_article_ideas_to_markdown",
    "OpenAIClient",
    "AIClientInterface"
]

__version__ = "0.2.0"

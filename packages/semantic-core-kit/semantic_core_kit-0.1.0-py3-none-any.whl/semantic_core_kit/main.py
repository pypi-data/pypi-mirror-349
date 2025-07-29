import logging
import os
from typing import Any, Dict, List, Optional

from .ai_processor import (
    OpenAIClient,  # Import the new OpenAIClient
    generate_article_ideas_from_clusters_with_ai,
    generate_keyword_clusters_with_ai,
    consolidate_clusters_with_ai # Added import
)
from .loader import load_and_clean_keywords

logger = logging.getLogger(__name__)


def process_keywords(
    csv_filepath: str,
    openai_model_name: Optional[str] = None,
    batch_size: int = 50,
    # Add a parameter to control consolidation, defaulting to True
    consolidate: bool = True 
) -> List[Dict[str, Any]]:
    """
    Processes a keyword CSV to generate article ideas using OpenAI.

    This function orchestrates the loading, cleaning, clustering, and idea generation steps.
    OpenAI API key is read from the OPENAI_API_KEY environment variable.
    OpenAI model name is configurable via a parameter or the OPENAI_MODEL_NAME environment variable.

    Args:
        csv_filepath: Path to the input CSV file.
        openai_model_name: OpenAI model to use (e.g., "gpt-3.5-turbo"). 
                           If None, uses OPENAI_MODEL_NAME env var, then defaults to "gpt-3.5-turbo".
        batch_size: Number of keywords to process in each batch for clustering.
        consolidate: Boolean to control whether clusters should be consolidated.

    Returns:
        A list of article idea dictionaries.
        Returns an empty list if any critical step fails (e.g., file not found, API key missing).

    Raises:
        ValueError: If OpenAI API key is not found.
        # Other exceptions from OpenAI API calls might also be raised.
    """
    logger.info(f"Starting keyword processing for: {csv_filepath}")

    # 1. Load and clean keywords
    logger.info("Step 1: Loading and cleaning keywords...")
    cleaned_keywords = load_and_clean_keywords(csv_filepath)
    if not cleaned_keywords:
        logger.warning("No keywords loaded or an error occurred during loading. Exiting.")
        return []
    logger.info(f"Loaded {len(cleaned_keywords)} cleaned keywords.")

    # 2. Initialize AI Client
    logger.info("Step 2: Initializing OpenAI client...")
    try:
        # OpenAIClient now internally handles API key from env var
        ai_client = OpenAIClient(model_name=openai_model_name)
        logger.info(f"OpenAI client initialized with model: {ai_client.model_name}")
    except ValueError as e:
        logger.error(f"Error initializing OpenAI client: {e}")
        return []
    except Exception as e: # Catch any other unexpected error during client init
        logger.error(f"An unexpected error occurred during OpenAI client initialization: {e}")
        return []

    # 3. Generate keyword clusters
    logger.info("Step 3: Generating keyword clusters...")
    try:
        initial_clusters = generate_keyword_clusters_with_ai(cleaned_keywords, ai_client, batch_size=batch_size)
        if not initial_clusters:
            logger.warning("No initial keyword clusters were generated. Exiting.")
            # Depending on desired strictness, you might return [] or proceed with no clusters
        else:
            logger.info(f"Generated {len(initial_clusters)} initial keyword clusters.")
    except Exception as e:
        logger.error(f"Error during keyword clustering: {e}")
        return [] # Critical step failed

    # 4. Consolidate keyword clusters
    final_clusters = initial_clusters
    if consolidate and len(initial_clusters) >= 2: # Only consolidate if flag is true and there's something to consolidate
        logger.info("Step 4: Consolidating keyword clusters...")
        final_clusters = consolidate_clusters_with_ai(
            initial_clusters=initial_clusters, ai_client=ai_client
        )
        if not final_clusters:
            logger.warning("Cluster consolidation resulted in no clusters. Using initial clusters as fallback, though this is unexpected.")
            # Fallback or decide error handling. For now, let's assume this shouldn't happen if initial_clusters was populated.
            # If consolidation truly can result in zero clusters from a non-zero input, this might need specific handling.
            final_clusters = initial_clusters # Fallback to initial if consolidation somehow empties the list and that's not desired.
        logger.info(f"Consolidated to {len(final_clusters)} final keyword clusters.")
    elif not consolidate:
        logger.info("Step 4: Skipping cluster consolidation as per configuration.")
    else: # len(initial_clusters) < 2
        logger.info("Step 4: Skipping cluster consolidation as there are fewer than 2 initial clusters.")
        
    # 5. Generate article ideas from clusters
    logger.info("Step 5: Generating article ideas from clusters...")
    if not final_clusters: # If no clusters, no ideas can be generated
        logger.warning("Skipping article idea generation as no clusters are available.")
        return []

    try:
        article_ideas = generate_article_ideas_from_clusters_with_ai(final_clusters, ai_client)
        if not article_ideas:
            logger.warning("No article ideas were generated by the AI or an error occurred.")
        else:
            logger.info(f"Generated {len(article_ideas)} article ideas.")
    except Exception as e:
        logger.error(f"Error during article idea generation: {e}")
        return [] # Critical step failed

    logger.info("Keyword processing completed.")
    return article_ideas

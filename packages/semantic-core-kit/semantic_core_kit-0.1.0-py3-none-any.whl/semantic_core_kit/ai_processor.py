import json
import os
import logging
import re # Added import
from typing import Any, Dict, List, Optional, Protocol

from openai import OpenAI  # Import OpenAI library

logger = logging.getLogger(__name__)

# --- Prompt Examples ---
CLUSTER_PROMPT_TEMPLATE = """
You are an AI assistant that groups keywords into semantic clusters.
Given the following list of keywords, please group them into relevant clusters.
For each cluster, provide a concise `cluster_name` and a list of the `keywords` that belong to it.
Keywords to cluster:
{batched_keywords_list}

Respond ONLY with a valid JSON list of objects, where each object has "cluster_name" (string) and "keywords" (list of strings).
Example JSON output:
[{{"cluster_name": "Sustainable Gardening", "keywords": ["organic fertilizer", "heirloom seeds"]}}]
"""

ARTICLE_IDEA_PROMPT_TEMPLATE = """
You are an AI assistant that generates article ideas based on keyword clusters.
For the given keyword cluster named '{cluster_name}' with the keywords [{keywords_list_str}],
please suggest an engaging 'article_title' and an 'article_type'.
The 'article_type' should be one of: 'review', 'guide', 'feature', 'news', 'generic'.

Respond ONLY with a valid JSON object with keys "article_title" (string) and "article_type" (string).
Example JSON output:
{{"article_title": "The Ultimate Guide to Starting Your Own Sustainable Garden", "article_type": "guide"}}
"""
# Note: The primary_keyword identification from the original plan is better handled in Python code
# after AI generation, as LLMs might struggle with consistently picking based on specific metrics from a list.
# --- End Prompt Examples ---


class AIClientInterface(Protocol):
    def generate(self, prompt: str) -> str:
        ...


# New OpenAIClient implementation
class OpenAIClient(AIClientInterface):
    """Handles communication with the OpenAI API."""
    def __init__(self, model_name: str | None = None):
        """
        Initializes the OpenAI client.

        API key is read from the OPENAI_API_KEY environment variable.
        Model name can be provided or read from OPENAI_MODEL_NAME env var.

        Args:
            model_name: OpenAI model name (e.g., "gpt-3.5-turbo"). If None, tries to read 
                        from OPENAI_MODEL_NAME env var, then defaults to "gpt-3.5-turbo".
        
        Raises:
            ValueError: If the OPENAI_API_KEY environment variable is not set.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set. Please set it before proceeding.")

        self.model_name = model_name or os.getenv("OPENAI_MODEL_NAME") or "gpt-3.5-turbo"

        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            # Catch potential errors during OpenAI client initialization (e.g. invalid API key format before first call)
            raise ValueError(f"Failed to initialize OpenAI client: {e}")

    def generate(self, prompt: str) -> str:
        """
        Generates text using the configured OpenAI model.

        Args:
            prompt: The prompt to send to the OpenAI API.

        Returns:
            The AI-generated text response.
        
        Raises:
            Exception: If the API call fails.
        """
        try:
            # Using ChatCompletion for newer models like gpt-3.5-turbo and gpt-4
            # The prompts are designed for a user/assistant style interaction implicitly.
            # For more complex scenarios, you might want to structure messages with roles explicitly.
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7, # Adjust for creativity vs. determinism
                # max_tokens can be set if needed, but prompts ask for JSON, so length should be manageable
            )
            # Assuming the response format is as expected for chat completions
            content = response.choices[0].message.content
            if content is None:
                 raise ValueError("OpenAI API returned an empty message content.")
            return content.strip()
        except Exception as e:
            # Log the error or handle it more gracefully
            print(f"OpenAI API call failed: {e}")
            # Depending on the desired behavior, you might re-raise, return a default, or handle specific API errors.
            raise # Re-raise the exception for now


# Helper function to extract JSON from markdown code blocks
def _extract_json_from_markdown(raw_response: str) -> str:
    """Extracts a JSON string from a markdown code block if present."""
    # Pattern to find ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_response)
    if match:
        return match.group(1).strip()
    return raw_response.strip() # Fallback to stripping the raw response


def generate_keyword_clusters_with_ai(
    cleaned_keywords: List[Dict[str, Any]],
    ai_client: AIClientInterface, # This will now typically be an OpenAIClient instance
    batch_size: int = 50
) -> List[Dict[str, Any]]:
    """
    Generates semantic keyword clusters using an AI model.

    Args:
        cleaned_keywords: A list of keyword dictionaries from load_and_clean_keywords.
        ai_client: An instance of the user's AI client with a .generate() method.
        batch_size: The number of keywords to send to the AI in each batch.

    Returns:
        A list of cluster dictionaries, where each cluster contains a
        'cluster_name' and a list of 'keywords' (original keyword dicts).
    """
    all_clusters: List[Dict[str, Any]] = []
    keyword_map = {kw["keyword"]: kw for kw in cleaned_keywords}

    for i in range(0, len(cleaned_keywords), batch_size):
        batch = cleaned_keywords[i : i + batch_size]
        if not batch:
            continue

        batch_keyword_strings = [kw["keyword"] for kw in batch]
        prompt = CLUSTER_PROMPT_TEMPLATE.format(
            batched_keywords_list="\n".join([f"- {kw}" for kw in batch_keyword_strings])
        )

        try:
            ai_response_str = ai_client.generate(prompt)
            # Clean the response before parsing
            cleaned_ai_response_str = _extract_json_from_markdown(ai_response_str)
            
            if not cleaned_ai_response_str:
                logger.warning(f"AI returned an empty response for batch {i // batch_size + 1}. Original: {ai_response_str}")
                continue

            ai_clusters_data = json.loads(cleaned_ai_response_str)

            ai_clusters_list = ai_clusters_data # In this function, ai_clusters_data is expected to be a list or a single cluster dict

            if not isinstance(ai_clusters_list, list):
                # If the AI returned a single dictionary, check if it's a valid cluster structure
                if isinstance(ai_clusters_list, dict) and \
                   "cluster_name" in ai_clusters_list and \
                   "keywords" in ai_clusters_list and \
                   isinstance(ai_clusters_list.get("keywords"), list):
                    ai_clusters_list = [ai_clusters_list] # Wrap it in a list
                else:
                    print(f"Warning: AI response for batch {i//batch_size + 1} was not a list or a valid single cluster dictionary. Response: {ai_response_str}")
                    continue # Skip this batch

            for ai_cluster in ai_clusters_list:
                if not (
                    isinstance(ai_cluster, dict)
                    and isinstance(ai_cluster.get("cluster_name"), str)
                    and isinstance(ai_cluster.get("keywords"), list)
                ):
                    print(f"Warning: Skipping malformed cluster from AI: {ai_cluster}")
                    continue

                cluster_name = ai_cluster["cluster_name"].strip()
                if not cluster_name:
                    print(f"Warning: Skipping cluster with empty name from AI: {ai_cluster}")
                    continue

                clustered_keyword_objects = []
                for kw_str in ai_cluster["keywords"]:
                    if isinstance(kw_str, str) and kw_str.lower() in keyword_map:
                        clustered_keyword_objects.append(keyword_map[kw_str.lower()])
                    else:
                        print(
                            f"Warning: Keyword '{kw_str}' from AI cluster '{cluster_name}' not found in original keyword map or not a string. It might be a new variation or a formatting issue."
                        )

                if clustered_keyword_objects:
                    all_clusters.append({"cluster_name": cluster_name, "keywords": clustered_keyword_objects})

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from AI for batch {i // batch_size + 1}: {e}. Response: {ai_response_str}")
        except Exception as e:
            logger.error(f"An unexpected error occurred with AI processing for batch {i // batch_size + 1}: {e}. Response: {ai_response_str}")

    return all_clusters


def generate_article_ideas_from_clusters_with_ai(
    clusters: List[Dict[str, Any]],
    ai_client: AIClientInterface # This will now typically be an OpenAIClient instance
) -> List[Dict[str, Any]]:
    """
    Generates article ideas for each keyword cluster using an AI model.

    Args:
        clusters: A list of keyword cluster dictionaries from generate_keyword_clusters_with_ai.
        ai_client: An instance of the user's AI client with a .generate() method.

    Returns:
        A list of article idea dictionaries, including 'theme' (cluster_name),
        'article_title', 'primary_keyword' (dict), 'supporting_keywords' (list of dicts),
        and 'article_type'.
    """
    article_ideas: List[Dict[str, Any]] = []
    valid_article_types = {"review", "guide", "feature", "news", "generic"}

    for cluster in clusters:
        cluster_name = cluster.get("cluster_name", "Unknown Cluster")
        cluster_keywords = cluster.get("keywords", [])

        if not cluster_keywords:
            print(f"Skipping cluster '{cluster_name}' as it has no keywords.")
            continue

        # Determine primary keyword (highest search volume)
        primary_keyword_obj = None
        if cluster_keywords:
            primary_keyword_obj = max(cluster_keywords, key=lambda kw: kw.get("avg_monthly_searches", 0))

        supporting_keywords = [kw for kw in cluster_keywords if kw != primary_keyword_obj]

        keyword_strings_for_prompt = [kw["keyword"] for kw in cluster_keywords]
        keywords_list_str = ", ".join(f"'{kw}'" for kw in keyword_strings_for_prompt)

        prompt = ARTICLE_IDEA_PROMPT_TEMPLATE.format(
            cluster_name=cluster_name,
            keywords_list_str=keywords_list_str
        )

        try:
            ai_response_str = ai_client.generate(prompt)
            # Clean the response before parsing
            cleaned_ai_response_str = _extract_json_from_markdown(ai_response_str)

            if not cleaned_ai_response_str:
                logger.warning(f"AI returned an empty response for cluster '{cluster_name}'. Original: {ai_response_str}")
                article_data = default_article_data
            else:
                article_data = json.loads(cleaned_ai_response_str)

            if not isinstance(article_data, dict) or \
               not isinstance(article_data.get("article_title"), str) or \
               not isinstance(article_data.get("article_type"), str):
                print(f"Warning: Skipping malformed article idea from AI for cluster '{cluster_name}': {article_data}")
                continue

            article_title = article_data["article_title"].strip()
            article_type = article_data["article_type"].strip().lower()

            if not article_title:
                print(f"Warning: Skipping article idea with empty title for cluster '{cluster_name}': {article_data}")
                continue

            if article_type not in valid_article_types:
                print(
                    f"Warning: AI returned an invalid article_type '{article_type}' for cluster '{cluster_name}'. Defaulting to 'generic'. Original response: {article_data}"
                )
                article_type = "generic"

            article_ideas.append(
                {
                    "theme": cluster_name,
                    "article_title": article_title,
                    "primary_keyword": primary_keyword_obj,  # This is the full dict
                    "supporting_keywords": supporting_keywords,  # List of full dicts
                    "article_type": article_type,
                }
            )

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from AI for cluster '{cluster_name}': {e}. Response: {ai_response_str}")
        except Exception as e:
            logger.error(f"An unexpected error occurred with AI processing for cluster '{cluster_name}': {e}. Response: {ai_response_str}")

    return article_ideas

MERGE_CLUSTERS_PROMPT_TEMPLATE = """You are an expert in semantic keyword analysis and topic clustering.
Your task is to determine if two keyword clusters should be merged into a single, more comprehensive cluster.

Cluster A:
Name: "{cluster_A_name}"
Keywords: {cluster_A_keywords_list}

Cluster B:
Name: "{cluster_B_name}"
Keywords: {cluster_B_keywords_list}

Based on the semantic similarity and topical relevance of these two clusters, should they be merged?
- If yes, provide a new, concise, and descriptive name for the merged cluster. The new name should ideally synthesize the core themes of both clusters.
- If no, the clusters should remain separate.

Respond ONLY with a JSON object in the following format:
{json_format}

Example for merging:
{{
  "should_merge": true,
  "merged_cluster_name": "Sustainable Urban Gardening Techniques"
}}

Example for not merging:
{{
  "should_merge": false,
  "merged_cluster_name": null
}}
"""

def consolidate_clusters_with_ai(
    initial_clusters: List[Dict[str, Any]], 
    ai_client: AIClientInterface,
    min_keywords_for_merge_check: int = 3 # Don't bother checking tiny clusters against each other often
) -> List[Dict[str, Any]]:
    """Consolidates a list of keyword clusters by asking an AI to merge similar ones."""
    logger.info(f"Starting cluster consolidation. Initial clusters: {len(initial_clusters)}")
    if not initial_clusters or len(initial_clusters) < 2:
        logger.info("Not enough clusters to consolidate.")
        return initial_clusters

    consolidated_clusters = [dict(c) for c in initial_clusters] # Work with a copy
    # Keep track of clusters that have been merged into others and should be removed
    merged_indices = set()

    # Define the expected JSON format for the prompt
    merge_json_format = '{\n  "should_merge": true_or_false,\n  "merged_cluster_name": "string_if_true_else_null"\n}'

    # Single pass consolidation: compare each cluster with subsequent ones
    for i in range(len(consolidated_clusters)):
        if i in merged_indices:
            continue # Skip if this cluster has already been merged

        cluster_A = consolidated_clusters[i]
        # Avoid merging very small clusters frequently unless necessary by specific use case
        if len(cluster_A.get("keywords", [])) < min_keywords_for_merge_check and min_keywords_for_merge_check > 0:
            continue

        for j in range(i + 1, len(consolidated_clusters)):
            if j in merged_indices:
                continue # Skip if this cluster has already been merged

            cluster_B = consolidated_clusters[j]
            if len(cluster_B.get("keywords", [])) < min_keywords_for_merge_check and min_keywords_for_merge_check > 0:
                continue

            logger.debug(f"Checking for merge: '{cluster_A['cluster_name']}' and '{cluster_B['cluster_name']}'")
            
            cluster_A_keywords_str = ", ".join([kw['keyword'] for kw in cluster_A.get("keywords", [])])
            cluster_B_keywords_str = ", ".join([kw['keyword'] for kw in cluster_B.get("keywords", [])])

            prompt = MERGE_CLUSTERS_PROMPT_TEMPLATE.format(
                cluster_A_name=cluster_A["cluster_name"],
                cluster_A_keywords_list=cluster_A_keywords_str,
                cluster_B_name=cluster_B["cluster_name"],
                cluster_B_keywords_list=cluster_B_keywords_str,
                json_format=merge_json_format
            )

            try:
                ai_response_str = ai_client.generate(prompt)
                cleaned_response = _extract_json_from_markdown(ai_response_str)
                if not cleaned_response:
                    logger.warning(f"AI returned empty response for merge check between '{cluster_A['cluster_name']}' and '{cluster_B['cluster_name']}'. Skipping merge.")
                    continue
                
                merge_decision = json.loads(cleaned_response)

                if merge_decision.get("should_merge") is True:
                    new_name = merge_decision.get("merged_cluster_name")
                    if not new_name or not isinstance(new_name, str):
                        logger.warning(f"AI suggested merge but provided no valid new name for '{cluster_A['cluster_name']}' & '{cluster_B['cluster_name']}'. Using A's name.")
                        new_name = cluster_A["cluster_name"]
                    
                    logger.info(f"Merging '{cluster_A['cluster_name']}' and '{cluster_B['cluster_name']}' into '{new_name}'")
                    
                    # Combine keywords (ensure no duplicates if a keyword somehow ended up in both)
                    # This assumes keyword dicts are unique or can be identified if not.
                    # For simplicity, just extend and then rely on primary keyword logic later if needed.
                    # A more robust way would be to create a set of keyword strings first.
                    cluster_A["keywords"].extend(cluster_B["keywords"])
                    # Deduplicate keywords based on the 'keyword' string within the dict
                    seen_keywords = set()
                    unique_keywords_list = []
                    for kw_dict in cluster_A["keywords"]:
                        if kw_dict['keyword'] not in seen_keywords:
                            unique_keywords_list.append(kw_dict)
                            seen_keywords.add(kw_dict['keyword'])
                    cluster_A["keywords"] = unique_keywords_list

                    cluster_A["cluster_name"] = new_name
                    merged_indices.add(j) # Mark cluster B as merged
                    
                    # Since cluster_A has changed, it might be good to re-evaluate it against others,
                    # but for a single pass, we just continue with the modified cluster_A.
                    # For a more thorough merge, one might break and restart the inner loop or the whole process.

            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from AI for merge check ('{cluster_A['cluster_name']}' vs '{cluster_B['cluster_name']}'): {e}. Response: {ai_response_str}")
            except Exception as e:
                logger.error(f"Unexpected error during AI merge check ('{cluster_A['cluster_name']}' vs '{cluster_B['cluster_name']}'): {e}")

    # Filter out the clusters that were marked as merged
    final_clusters = [consolidated_clusters[i] for i in range(len(consolidated_clusters)) if i not in merged_indices]
    logger.info(f"Cluster consolidation complete. Final clusters: {len(final_clusters)}")
    return final_clusters

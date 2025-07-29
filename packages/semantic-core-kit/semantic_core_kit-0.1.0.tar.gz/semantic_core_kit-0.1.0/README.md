# Semantic Core Kit: AI-Assisted Semantic Core & Article Idea Generator

`semantic-core-kit` is a Python library designed to help content creators, SEO specialists, and marketers process keyword lists, discover semantic relationships between keywords using OpenAI, and generate actionable article ideas.

## Features

- **Load & Clean Keywords**: Import keywords from a CSV file, automatically clean them (lowercase, normalize search volumes), and handle duplicates intelligently.
- **OpenAI-Powered Keyword Clustering**: Leverages OpenAI (configurable model) to group keywords into semantically relevant clusters. The library handles batching and API interaction.
- **OpenAI-Powered Article Idea Generation**: For each keyword cluster, use OpenAI to brainstorm article titles and types (e.g., review, guide, feature), automatically identifying a primary keyword for focus.
- **Markdown Export**: Save the generated article ideas, complete with themes, titles, primary and supporting keywords, and article types, into a structured Markdown file using a separate utility function.
- **Simplified Workflow**: A primary function `process_keywords()` handles the end-to-end process.
- **Environment Variable Configuration**: Securely configure your OpenAI API key (`OPENAI_API_KEY`) and model (`OPENAI_MODEL_NAME`) via environment variables.

## Installation

1.  **Copy the `semantic_core_kit` directory** into your project, or install it if packaged (see `pyproject.toml`).
2.  **Ensure you have Python 3.8+** installed.
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt 
    # or if you manage dependencies with your project, ensure 'openai' is included.
    ```
4.  **Set Environment Variables**:
    For the library to access OpenAI, you **must** set the following environment variables:
    -   `OPENAI_API_KEY`: Your OpenAI API key.
    -   `OPENAI_MODEL_NAME` (Optional): The OpenAI model you wish to use (e.g., `gpt-4-turbo-preview`, `gpt-3.5-turbo`). Defaults to `gpt-3.5-turbo` if not set.

## Usage Example

Here's a typical workflow using `semantic-core-kit`:

```python
import os
from semantic_core_kit import process_keywords, save_article_ideas_to_markdown

# Ensure your OPENAI_API_KEY is set as an environment variable
# For example, you might load it from a .env file using python-dotenv in your main script
# from dotenv import load_dotenv
# load_dotenv()

# Check if API key is available (optional, process_keywords will also check)
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it before running the script.")
    exit()

# 1. Prepare your CSV file (e.g., 'keywords.csv')
#    The CSV should skip the first 2 lines and use the 3rd as headers.
#    Required columns: "Keyword", "Avg. monthly searches"
#    Optional columns: "Competition (indexed value)", "Competition"
#    Example 'keywords.csv' content:
#    Line 1: Some descriptive text (will be skipped)
#    Line 2: Another descriptive line (will be skipped)
#    Line 3: Keyword,Avg. monthly searches,Competition (indexed value),Competition
#    Data: organic fertilizer,1000,50,Medium
#    Data: heirloom seeds,500,30,Low
#    Data: indoor gardening lights,800,60,High
#    Data: low light houseplants,1200,40,Medium

csv_filepath = "my_keywords.csv" # Replace with your CSV file path

# Create a dummy keywords.csv for the example to run
# In a real scenario, you would have your own CSV file.
if not os.path.exists(csv_filepath):
    print(f"Creating dummy CSV: {csv_filepath}")
    with open(csv_filepath, 'w', encoding='utf-8') as f:
        f.write("Source: My Keyword Research Tool\n")
        f.write("Date: 2023-01-01\n")
        f.write("Keyword,Avg. monthly searches,Competition (indexed value),Competition\n")
        f.write("organic fertilizer,1000,50,Medium\n")
        f.write("heirloom seeds,500,30,Low\n")
        f.write("indoor gardening lights,800,60,High\n")
        f.write("low light houseplants,1200,40,Medium\n")
        f.write("sustainable farming,1500,55,Medium\n")
        f.write("vertical gardens,700,65,High\n")

# 2. Process the keywords to get article ideas
print(f"Processing {csv_filepath}...")
# You can optionally override the OpenAI model here, or rely on OPENAI_MODEL_NAME env var
# article_ideas = process_keywords(csv_filepath, openai_model_name="gpt-4-turbo-preview") 
article_ideas = process_keywords(csv_filepath)

# 3. Use the generated article ideas
if article_ideas:
    print(f"\nSuccessfully generated {len(article_ideas)} article ideas.")
    for i, idea in enumerate(article_ideas):
        print(f"  Idea {i+1}: {idea['article_title']} (Theme: {idea['theme']}, Type: {idea['article_type']})")
        # print(f"    Primary Keyword: {idea['primary_keyword']['keyword']}")

    # 4. Optionally, save them to a Markdown file
    output_md_file = "generated_article_ideas.md"
    print(f"\nSaving article ideas to {output_md_file}...")
    save_article_ideas_to_markdown(article_ideas, output_md_file)
    print(f"Done. Check '{output_md_file}'.")
else:
    print("No article ideas were generated. Check logs for errors.")

```

## API Overview

The library primarily exposes:

-   `process_keywords(csv_filepath: str, openai_model_name: Optional[str] = None, batch_size: int = 50) -> List[Dict[str, Any]]`
    -   **Main function.** Orchestrates loading keywords, clustering with OpenAI, and generating article ideas with OpenAI.
    -   Requires `OPENAI_API_KEY` environment variable to be set.
    -   `openai_model_name`: Optionally override the OpenAI model. If `None`, `OPENAI_MODEL_NAME` env var is used, then defaults to "gpt-3.5-turbo".
    -   Returns a list of article idea dictionaries.

And the following utility/component functions:

-   `save_article_ideas_to_markdown(article_ideas: list[dict], output_filepath: str = "article_ideas.md") -> None`
    -   Saves the generated article ideas into a structured Markdown file.
-   `load_and_clean_keywords(csv_filepath: str) -> list[dict]`
    -   Loads and processes keywords from the specified CSV file. (Used internally by `process_keywords`)
-   `OpenAIClient(model_name: Optional[str] = None)`
    -   The client class for interacting with OpenAI. Requires `OPENAI_API_KEY` env var. (Used internally by `process_keywords`)

Refer to the docstrings within each module (`loader.py`, `ai_processor.py`, `utils.py`, `main.py`) for more detailed information.

## Advanced Usage & AI Client

While `process_keywords` provides a simplified interface, the underlying functions (`generate_keyword_clusters_with_ai`, `generate_article_ideas_from_clusters_with_ai`) and the `OpenAIClient` are still accessible if you need more granular control or wish to integrate them differently.

The prompts used for interacting with OpenAI are defined as constants (`CLUSTER_PROMPT_TEMPLATE` and `ARTICLE_IDEA_PROMPT_TEMPLATE`) in `semantic_core_kit/ai_processor.py`.

## Error Handling

The library includes error handling for:
-   File I/O operations.
-   Missing OpenAI API Key.
-   JSON parsing from AI responses.
-   Unexpected AI response structures and API errors.

Errors or warnings are typically printed to the console. For production use, consider integrating a more robust logging mechanism.

## To-Do / Potential Enhancements

-   More sophisticated error logging (e.g., using the `logging` module).
-   Support for other AI providers (e.g., Google Gemini, Anthropic Claude).
-   More flexible configuration for AI parameters (temperature, max_tokens, etc.).
-   Support for other input/output formats.

## Contributing

Contributions are welcome! Please feel free to submit issues or merge requests.

(This is a basic README. You can expand it with more details, badges, license information, etc., as needed.)

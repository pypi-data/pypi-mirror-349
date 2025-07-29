from typing import Any, Dict, List


def save_article_ideas_to_markdown(
    article_ideas: List[Dict[str, Any]], output_filepath: str = "article_ideas.md"
) -> None:
    """
    Saves a list of article ideas to a structured Markdown file.

    Each article idea is formatted with its theme (cluster name), title,
    primary keyword, supporting keywords, and article type.

    Args:
        article_ideas: A list of article idea dictionaries.
        output_filepath: The path to save the Markdown file.
                         Defaults to "article_ideas.md".
    """
    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("# Generated Article Ideas\n\n")
            if not article_ideas:
                f.write("No article ideas were generated.\n")
                return

            for i, idea in enumerate(article_ideas):
                theme = idea.get("theme", "N/A")
                title = idea.get("article_title", "N/A")
                article_type = idea.get("article_type", "N/A")
                primary_kw_obj = idea.get("primary_keyword")

                primary_kw_str = "N/A"
                primary_kw_searches = "N/A"
                if primary_kw_obj and isinstance(primary_kw_obj, dict):
                    primary_kw_str = primary_kw_obj.get("keyword", "N/A")
                    primary_kw_searches = str(primary_kw_obj.get("avg_monthly_searches", "N/A"))

                f.write(f"## Idea {i + 1}: {title}\n\n")
                f.write(f"- **Theme/Cluster:** {theme}\n")
                if article_type == 'N/A':
                    f.write("- **Article Type:** N/A\n")
                else:
                    f.write(f"- **Article Type:** {article_type.capitalize()}\n")
                f.write(f"- **Primary Keyword:** {primary_kw_str} (Avg. Searches: {primary_kw_searches})\n")

                supporting_keywords = idea.get("supporting_keywords", [])
                if supporting_keywords:
                    f.write("- **Supporting Keywords:**\n")
                    for skw_obj in supporting_keywords:
                        if isinstance(skw_obj, dict):
                            skw_str = skw_obj.get("keyword", "N/A")
                            skw_searches = str(skw_obj.get("avg_monthly_searches", "N/A"))
                            f.write(f"  - {skw_str} (Avg. Searches: {skw_searches})\n")
                        else:
                            f.write(f"  - {str(skw_obj)} (Data not in expected format)\n")
                else:
                    f.write("- **Supporting Keywords:** None\n")
                f.write("\n---\n\n")
        print(f"Successfully saved article ideas to {output_filepath}")
    except OSError as e:
        print(f"Error writing to file {output_filepath}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving to Markdown: {e}")

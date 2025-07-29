import csv
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

def load_and_clean_keywords(csv_filepath: str) -> List[Dict[str, Any]]:
    """
    Loads keywords from a CSV file, cleans them, and handles duplicates.

    The CSV file is expected to:
    - Skip the first 2 lines.
    - Use the 3rd line as headers.
    - Contain columns: "Keyword", "Avg. monthly searches",
                       "Competition (indexed value)", "Competition".

    Cleaning steps:
    - Converts keywords to lowercase.
    - Converts "Avg. monthly searches" to an integer, defaulting to 0 on error.
    - Removes duplicate keywords, keeping the entry with the highest search volume.

    Args:
        csv_filepath: Path to the input CSV file.

    Returns:
        A list of dictionaries, where each dictionary represents a keyword
        and its associated data (e.g., {"keyword": str, "avg_monthly_searches": int, ...}).
    """
    logger.info(f"Starting keyword loading and cleaning for: {csv_filepath}")
    print(f"[LOADER_DEBUG] Starting load_and_clean_keywords for: {csv_filepath}") # DEBUG PRINT
    raw_keywords: List[Dict[str, Any]] = []
    cleaned_keywords_dict: Dict[str, Dict[str, Any]] = {}

    encodings_to_try = ['utf-8-sig', 'utf-8', 'utf-16', 'latin-1'] # Added utf-8-sig
    file_content_lines = None

    print(f"[LOADER_DEBUG] Attempting encodings: {encodings_to_try}") # DEBUG PRINT
    for encoding in encodings_to_try:
        print(f"[LOADER_DEBUG] Trying encoding: {encoding}") # DEBUG PRINT
        try:
            with open(csv_filepath, mode='r', newline='', encoding=encoding) as file:
                file_content_lines = file.readlines()
            logger.info(f"Successfully read file {csv_filepath} with encoding {encoding}")
            print(f"[LOADER_DEBUG] Successfully read file with encoding {encoding}") # DEBUG PRINT
            break
        except UnicodeDecodeError:
            logger.warning(f"Failed to decode {csv_filepath} with encoding {encoding}. Trying next...")
            print(f"[LOADER_DEBUG] UnicodeDecodeError with encoding {encoding}. Trying next...") # DEBUG PRINT
        except FileNotFoundError:
            logger.error(f"Error: The file was not found at {csv_filepath}")
            print(f"[LOADER_DEBUG] FileNotFoundError for {csv_filepath}") # DEBUG PRINT
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred while reading {csv_filepath} with encoding {encoding}: {e}")
            print(f"[LOADER_DEBUG] Exception while reading with {encoding}: {e}") # DEBUG PRINT
            return []

    if file_content_lines is None:
        logger.error(f"Could not read or decode {csv_filepath} with any of the attempted encodings: {encodings_to_try}")
        print(f"[LOADER_DEBUG] file_content_lines is None after trying all encodings.") # DEBUG PRINT
        return []
    
    print(f"[LOADER_DEBUG] File read, proceeding to CSV parsing. Lines: {len(file_content_lines)}") # DEBUG PRINT
    try:
        if len(file_content_lines) < 3:
            logger.error(f"File {csv_filepath} has fewer than 3 lines. Cannot process headers.")
            print(f"[LOADER_DEBUG] File has < 3 lines.") # DEBUG PRINT
            return []
        
        reader = csv.DictReader(file_content_lines[2:], delimiter='\t')
        print(f"[LOADER_DEBUG] csv.DictReader created with tab delimiter.") # DEBUG PRINT

        for i, row in enumerate(reader):
            # print(f"[LOADER_DEBUG] Processing row {i}: {row}") # DEBUG PRINT - too verbose initially
            try:
                keyword = row.get("Keyword", "").strip().lower()
                if not keyword:
                    # print(f"[LOADER_DEBUG] Row {i} has empty keyword, skipping.") # DEBUG PRINT
                    continue

                avg_monthly_searches_str = row.get("Avg. monthly searches", "0")
                try:
                    avg_monthly_searches = int(
                        float(avg_monthly_searches_str.replace(",", ""))
                    )
                except ValueError:
                    avg_monthly_searches = 0

                competition_indexed_str = row.get("Competition (indexed value)", "0")
                try:
                    competition_indexed = int(competition_indexed_str)
                except ValueError:
                    competition_indexed = 0

                competition = row.get("Competition", "").strip()

                raw_keywords.append(
                    {
                        "keyword": keyword,
                        "avg_monthly_searches": avg_monthly_searches,
                        "competition_indexed_value": competition_indexed,
                        "competition": competition,
                        "original_avg_monthly_searches": row.get("Avg. monthly searches"),
                        "original_competition_indexed_value": row.get("Competition (indexed value)"),
                        "original_competition": row.get("Competition"),
                    }
                )
            except Exception as e:
                logger.error(f"Skipping row due to error processing row data: {row} - {e}")
                print(f"[LOADER_DEBUG] Error processing row {i} data: {e}") # DEBUG PRINT
                continue
        print(f"[LOADER_DEBUG] Finished processing rows. Raw keywords count: {len(raw_keywords)}") # DEBUG PRINT
    except Exception as e:
        logger.error(f"An unexpected error occurred while processing CSV data from {csv_filepath} after reading file: {e}")
        print(f"[LOADER_DEBUG] Exception during CSV processing stage: {e}") # DEBUG PRINT
        return []

    for kw_data in raw_keywords:
        keyword = kw_data["keyword"]
        if keyword in cleaned_keywords_dict:
            if kw_data["avg_monthly_searches"] > cleaned_keywords_dict[keyword]["avg_monthly_searches"]:
                cleaned_keywords_dict[keyword] = kw_data
        else:
            cleaned_keywords_dict[keyword] = kw_data

    logger.info(f"Successfully loaded and cleaned {len(cleaned_keywords_dict)} keywords from {csv_filepath}")
    print(f"[LOADER_DEBUG] Successfully cleaned keywords. Count: {len(cleaned_keywords_dict)}") # DEBUG PRINT
    return list(cleaned_keywords_dict.values())

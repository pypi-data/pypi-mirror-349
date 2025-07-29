import os
import unittest
from unittest.mock import patch, MagicMock, ANY

from semantic_core_kit.main import process_keywords

# Assuming OpenAIClient is in ai_processor for mocking purposes
# from semantic_core_kit.ai_processor import OpenAIClient

# Assuming these are sensible defaults or representative structures
SAMPLE_CLEANED_KEYWORDS = [
    {"keyword": "kw1", "avg_monthly_searches": 100},
    {"keyword": "kw2", "avg_monthly_searches": 200}
]
SAMPLE_INITIAL_CLUSTERS = [
    {"cluster_name": "Cluster A", "keywords": [SAMPLE_CLEANED_KEYWORDS[0]]},
    {"cluster_name": "Cluster B", "keywords": [SAMPLE_CLEANED_KEYWORDS[1]]}
]
SAMPLE_CONSOLIDATED_CLUSTERS = [
    {"cluster_name": "Cluster AB", "keywords": SAMPLE_CLEANED_KEYWORDS}
]
SAMPLE_ARTICLE_IDEAS = [
    {"theme": "Cluster AB", "article_title": "Title for AB", "primary_keyword": SAMPLE_CLEANED_KEYWORDS[1], "supporting_keywords": [SAMPLE_CLEANED_KEYWORDS[0]], "article_type": "guide"}
]

class TestMainProcessKeywords(unittest.TestCase):

    def setUp(self):
        self.test_csv_file = "test_process_keywords.csv"
        # Create a dummy CSV for testing
        with open(self.test_csv_file, 'w', encoding='utf-8') as f:
            f.write("Skipped Line 1\n")
            f.write("Skipped Line 2\n")
            f.write("Keyword,Avg. monthly searches\n")
            f.write("kw1,100\n")
            f.write("kw2,200\n")

        # Mock data
        self.mock_cleaned_keywords = [
            {"keyword": "kw1", "avg_monthly_searches": 100},
            {"keyword": "kw2", "avg_monthly_searches": 200}
        ]
        self.mock_clusters = [
            {"cluster_name": "Cluster 1", "keywords": [self.mock_cleaned_keywords[0]]}
        ]
        self.mock_article_ideas = [
            {"theme": "Cluster 1", "article_title": "Title 1", "primary_keyword": self.mock_cleaned_keywords[0], "supporting_keywords": [], "article_type": "guide"}
        ]

    def tearDown(self):
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)

    @patch('semantic_core_kit.main.load_and_clean_keywords')
    @patch('semantic_core_kit.main.OpenAIClient')
    @patch('semantic_core_kit.main.generate_keyword_clusters_with_ai')
    @patch('semantic_core_kit.main.consolidate_clusters_with_ai')
    @patch('semantic_core_kit.main.generate_article_ideas_from_clusters_with_ai')
    def test_process_keywords_e2e_success_with_consolidation(self, mock_gen_ideas, mock_consolidate, mock_gen_clusters, MockOpenAIClient, mock_load_keywords):
        # Setup mocks
        mock_load_keywords.return_value = SAMPLE_CLEANED_KEYWORDS
        mock_openai_client_instance = MockOpenAIClient.return_value
        mock_gen_clusters.return_value = SAMPLE_INITIAL_CLUSTERS
        mock_consolidate.return_value = SAMPLE_CONSOLIDATED_CLUSTERS
        mock_gen_ideas.return_value = SAMPLE_ARTICLE_IDEAS

        # Call the main function with consolidate=True (default)
        result = process_keywords("dummy.csv", openai_model_name="test_model", consolidate=True)

        # Assertions
        mock_load_keywords.assert_called_once_with("dummy.csv")
        MockOpenAIClient.assert_called_once_with(model_name="test_model")
        mock_gen_clusters.assert_called_once_with(
            ANY,
            mock_openai_client_instance,
            batch_size=50
        )
        mock_consolidate.assert_called_once_with(
            initial_clusters=SAMPLE_INITIAL_CLUSTERS, 
            ai_client=mock_openai_client_instance
        )
        mock_gen_ideas.assert_called_once_with(
            ANY,
            mock_openai_client_instance
        )
        self.assertEqual(result, SAMPLE_ARTICLE_IDEAS)

    @patch('semantic_core_kit.main.load_and_clean_keywords')
    @patch('semantic_core_kit.main.OpenAIClient')
    @patch('semantic_core_kit.main.generate_keyword_clusters_with_ai')
    @patch('semantic_core_kit.main.consolidate_clusters_with_ai')
    @patch('semantic_core_kit.main.generate_article_ideas_from_clusters_with_ai')
    def test_process_keywords_e2e_success_no_consolidation(self, mock_gen_ideas, mock_consolidate, mock_gen_clusters, MockOpenAIClient, mock_load_keywords):
        # Setup mocks
        mock_load_keywords.return_value = SAMPLE_CLEANED_KEYWORDS
        mock_openai_client_instance = MockOpenAIClient.return_value
        mock_gen_clusters.return_value = SAMPLE_INITIAL_CLUSTERS
        mock_gen_ideas.return_value = SAMPLE_ARTICLE_IDEAS

        # Call the main function with consolidate=False
        result = process_keywords("dummy.csv", openai_model_name="test_model", consolidate=False)

        # Assertions
        mock_load_keywords.assert_called_once_with("dummy.csv")
        MockOpenAIClient.assert_called_once_with(model_name="test_model")
        mock_gen_clusters.assert_called_once_with(
            ANY,
            mock_openai_client_instance,
            batch_size=50
        )
        mock_consolidate.assert_not_called()
        mock_gen_ideas.assert_called_once_with(
            ANY,
            mock_openai_client_instance
        )
        self.assertEqual(result, SAMPLE_ARTICLE_IDEAS)

    @patch('semantic_core_kit.main.load_and_clean_keywords')
    @patch('semantic_core_kit.main.OpenAIClient')
    @patch('semantic_core_kit.main.generate_keyword_clusters_with_ai')
    @patch('semantic_core_kit.main.consolidate_clusters_with_ai')
    @patch('semantic_core_kit.main.generate_article_ideas_from_clusters_with_ai')
    def test_process_keywords_consolidation_skipped_if_less_than_two_clusters(self, mock_gen_ideas, mock_consolidate, mock_gen_clusters, MockOpenAIClient, mock_load_keywords):
        # Setup mocks
        mock_load_keywords.return_value = SAMPLE_CLEANED_KEYWORDS
        mock_openai_client_instance = MockOpenAIClient.return_value
        one_cluster = [SAMPLE_INITIAL_CLUSTERS[0]]
        mock_gen_clusters.return_value = one_cluster 
        mock_gen_ideas.return_value = SAMPLE_ARTICLE_IDEAS

        # Call the main function with consolidate=True (but it should be skipped)
        result = process_keywords("dummy.csv", openai_model_name="test_model", consolidate=True)

        mock_consolidate.assert_not_called()
        mock_gen_ideas.assert_called_once_with(one_cluster, mock_openai_client_instance)
        self.assertEqual(result, SAMPLE_ARTICLE_IDEAS)

    @patch('semantic_core_kit.main.load_and_clean_keywords', return_value=[]) # No keywords loaded
    def test_process_keywords_no_keywords_loaded(self, mock_load_keywords):
        result = process_keywords("empty.csv")
        self.assertEqual(result, [])

    @patch('semantic_core_kit.main.load_and_clean_keywords', return_value=SAMPLE_CLEANED_KEYWORDS)
    @patch('semantic_core_kit.main.OpenAIClient', side_effect=ValueError("API Key Error"))
    def test_process_keywords_openai_client_init_fails(self, MockOpenAIClient, mock_load_keywords):
        result = process_keywords("dummy.csv")
        self.assertEqual(result, [])
        MockOpenAIClient.assert_called_once()

    @patch('semantic_core_kit.main.load_and_clean_keywords', return_value=SAMPLE_CLEANED_KEYWORDS)
    @patch('semantic_core_kit.main.OpenAIClient')
    @patch('semantic_core_kit.main.generate_keyword_clusters_with_ai', return_value=[]) # No clusters generated
    def test_process_keywords_no_initial_clusters_generated(self, mock_gen_clusters, MockOpenAIClient, mock_load_keywords):
        result = process_keywords("dummy.csv")
        self.assertEqual(result, [])

    @patch('semantic_core_kit.main.load_and_clean_keywords', return_value=SAMPLE_CLEANED_KEYWORDS)
    @patch('semantic_core_kit.main.OpenAIClient')
    @patch('semantic_core_kit.main.generate_keyword_clusters_with_ai', return_value=SAMPLE_INITIAL_CLUSTERS)
    @patch('semantic_core_kit.main.consolidate_clusters_with_ai', return_value=SAMPLE_CONSOLIDATED_CLUSTERS) 
    @patch('semantic_core_kit.main.generate_article_ideas_from_clusters_with_ai', return_value=[]) # No ideas generated
    def test_process_keywords_no_article_ideas_generated(self, mock_gen_ideas, mock_consolidate, mock_gen_clusters, MockOpenAIClient, mock_load_keywords):
        result = process_keywords("dummy.csv")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()

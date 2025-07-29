import json
import os
import unittest
from unittest.mock import MagicMock, patch, call

from semantic_core_kit.ai_processor import (
    AIClientInterface,
    OpenAIClient,
    generate_article_ideas_from_clusters_with_ai,
    generate_keyword_clusters_with_ai,
    consolidate_clusters_with_ai,
    _extract_json_from_markdown,
)


class TestOpenAIClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.model_name = "test_model"
        # Set env vars for default initialization path testing
        os.environ["OPENAI_API_KEY"] = self.api_key
        os.environ["OPENAI_MODEL_NAME"] = self.model_name

    def tearDown(self):
        # Clean up env vars
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        if "OPENAI_MODEL_NAME" in os.environ:
            del os.environ["OPENAI_MODEL_NAME"]

    def test_openai_client_init_with_params(self):
        # Test with model_name param, API key from env
        os.environ["OPENAI_API_KEY"] = "param_test_key"
        client = OpenAIClient(model_name="param_model")
        self.assertEqual(client.api_key, "param_test_key")
        self.assertEqual(client.model_name, "param_model")
        self.assertIsNotNone(client.client)
        del os.environ["OPENAI_API_KEY"]

    def test_openai_client_init_with_env_vars(self):
        # API key and model name from env vars (set in setUp)
        client = OpenAIClient()
        self.assertEqual(client.api_key, self.api_key)
        self.assertEqual(client.model_name, self.model_name)
        self.assertIsNotNone(client.client)

    def test_openai_client_init_missing_api_key(self):
        if "OPENAI_API_KEY" in os.environ: # Ensure it is not set
            del os.environ["OPENAI_API_KEY"]
        with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY environment variable not set"):
            OpenAIClient()

    def test_openai_client_init_default_model(self):
        if "OPENAI_MODEL_NAME" in os.environ:
            del os.environ["OPENAI_MODEL_NAME"]
        os.environ["OPENAI_API_KEY"] = "some_key_for_default_model_test" # Needs API key
        client = OpenAIClient()
        self.assertEqual(client.model_name, "gpt-3.5-turbo") # Default model
        del os.environ["OPENAI_API_KEY"]

    @patch('semantic_core_kit.ai_processor.OpenAI') # Target where OpenAI is used
    def test_generate_success(self, MockOpenAISDK):
        # Configure the mock SDK client and its methods
        mock_sdk_instance = MockOpenAISDK.return_value
        mock_chat_completion = MagicMock()
        mock_chat_completion.choices = [MagicMock()]
        mock_chat_completion.choices[0].message = MagicMock()
        mock_chat_completion.choices[0].message.content = " Mock AI Response "
        mock_sdk_instance.chat.completions.create.return_value = mock_chat_completion

        # Client now relies on env vars set in setUp for API key
        client = OpenAIClient(model_name=self.model_name)
        prompt = "Test prompt"
        response = client.generate(prompt)

        self.assertEqual(response, "Mock AI Response")
        mock_sdk_instance.chat.completions.create.assert_called_once_with(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

    @patch('semantic_core_kit.ai_processor.OpenAI') # Target where OpenAI is used
    def test_generate_api_failure(self, MockOpenAISDK):
        mock_sdk_instance = MockOpenAISDK.return_value
        mock_sdk_instance.chat.completions.create.side_effect = Exception("API Error")

        client = OpenAIClient(model_name=self.model_name)
        # We expect the specific Exception "API Error" we set as side_effect
        # and for the print in our OpenAIClient.generate's except block to have occurred.
        with patch('builtins.print') as mock_print: 
            with self.assertRaisesRegex(Exception, "API Error"):
                client.generate("Test prompt")
            mock_print.assert_any_call("OpenAI API call failed: API Error")

    @patch('semantic_core_kit.ai_processor.OpenAI') # Target where OpenAI is used
    def test_generate_empty_content(self, MockOpenAISDK):
        mock_sdk_instance = MockOpenAISDK.return_value
        mock_chat_completion = MagicMock()
        mock_chat_completion.choices = [MagicMock()]
        mock_chat_completion.choices[0].message = MagicMock()
        mock_chat_completion.choices[0].message.content = None # Simulate empty content
        mock_sdk_instance.chat.completions.create.return_value = mock_chat_completion

        client = OpenAIClient(model_name=self.model_name)
        with self.assertRaisesRegex(ValueError, "OpenAI API returned an empty message content."):
            client.generate("Test prompt")


class TestAIProcessorFunctions(unittest.TestCase):
    # These tests focus on the data transformation logic within these functions,
    # assuming the AI client (now OpenAIClient, typically mocked at a higher level
    # or a simple MagicMock here) provides well-formed JSON strings.

    def setUp(self):
        self.keywords_data = [
            {"keyword": "organic fertilizer", "avg_monthly_searches": 500},
            {"keyword": "heirloom seeds", "avg_monthly_searches": 300},
            {"keyword": "indoor gardening", "avg_monthly_searches": 700}
        ]
        self.keyword_map = {kw["keyword"]: kw for kw in self.keywords_data}

    def test_generate_keyword_clusters_logic(self):
        mock_ai_client = MagicMock(spec=AIClientInterface)
        # Simulate AI returning a JSON string representing a list of clusters
        mock_ai_client.generate.return_value = json.dumps([
            {"cluster_name": "Gardening Basics", "keywords": ["organic fertilizer", "heirloom seeds"]}
        ])

        result = generate_keyword_clusters_with_ai(self.keywords_data, mock_ai_client, batch_size=3)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["cluster_name"], "Gardening Basics")
        self.assertEqual(len(result[0]["keywords"]), 2)
        self.assertIn(self.keyword_map["organic fertilizer"], result[0]["keywords"])
        mock_ai_client.generate.assert_called_once() # Ensure AI was called

    def test_generate_article_ideas_logic(self):
        mock_ai_client = MagicMock(spec=AIClientInterface)
        clusters = [
            {"cluster_name": "Gardening", "keywords": [self.keywords_data[0], self.keywords_data[1]]}
        ]
        # Simulate AI returning a JSON string for an article idea
        mock_ai_client.generate.return_value = json.dumps({"article_title": "Gardening Fun", "article_type": "guide"})

        result = generate_article_ideas_from_clusters_with_ai(clusters, mock_ai_client)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["article_title"], "Gardening Fun")
        self.assertEqual(result[0]["article_type"], "guide")
        self.assertEqual(result[0]["primary_keyword"], self.keywords_data[0]) # organic fertilizer
        mock_ai_client.generate.assert_called_once()


class TestExtractJsonFromMarkdown(unittest.TestCase):
    def test_with_json_fence(self):
        text = "```json\n{\"key\": \"value\"}\n```"
        self.assertEqual(_extract_json_from_markdown(text), '{\"key\": \"value\"}')

    def test_with_backtick_fence_only(self):
        text = "```\n{\"key\": \"value\"}\n```"
        self.assertEqual(_extract_json_from_markdown(text), '{\"key\": \"value\"}')

    def test_no_fence(self):
        text = '{\"key\": \"value\"}'
        self.assertEqual(_extract_json_from_markdown(text), '{\"key\": \"value\"}')

    def test_text_before_and_after_fence(self):
        text = "Some text before\n```json\n{\"key\": \"value\"}\n```\nSome text after"
        self.assertEqual(_extract_json_from_markdown(text), '{\"key\": \"value\"}')

    def test_empty_string(self):
        self.assertEqual(_extract_json_from_markdown(""), "")

    def test_string_with_only_whitespace(self):
        self.assertEqual(_extract_json_from_markdown("   \n  "), "")
    
    def test_malformed_fence_no_json(self):
        text = "```json\nThis is not json\n```"
        self.assertEqual(_extract_json_from_markdown(text), "This is not json")

    def test_no_fence_just_text(self):
        text = "This is not json"
        self.assertEqual(_extract_json_from_markdown(text), "This is not json")


class TestAIProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_ai_client = MagicMock(spec=AIClientInterface)
        self.sample_keywords = [
            {"keyword": "apple pie recipe", "avg_monthly_searches": 1000, "competition_indexed_value": 60, "competition": "Medium"},
            {"keyword": "easy apple pie", "avg_monthly_searches": 800, "competition_indexed_value": 50, "competition": "Medium"},
            {"keyword": "banana bread recipe", "avg_monthly_searches": 1200, "competition_indexed_value": 70, "competition": "High"},
            {"keyword": "chocolate cake recipe", "avg_monthly_searches": 1500, "competition_indexed_value": 65, "competition": "High"},
            {"keyword": "best chocolate cake", "avg_monthly_searches": 900, "competition_indexed_value": 55, "competition": "Medium"},
        ]
        self.sample_keyword_map = {kw["keyword"]: kw for kw in self.sample_keywords}

    # Tests for generate_keyword_clusters_with_ai
    def test_generate_keyword_clusters_basic(self):
        # AI returns a list of clusters
        ai_response = '[{"cluster_name": "Fruit Desserts", "keywords": ["apple pie recipe", "easy apple pie"]}]'
        self.mock_ai_client.generate.return_value = f"```json\n{ai_response}\n```"
        
        # Use a subset of keywords that fits into one batch for this basic test
        test_specific_keywords = self.sample_keywords[:2]
        clusters = generate_keyword_clusters_with_ai(test_specific_keywords, self.mock_ai_client, batch_size=2)
        
        self.assertEqual(len(clusters), 1)
        self.assertEqual(clusters[0]["cluster_name"], "Fruit Desserts")
        self.assertEqual(len(clusters[0]["keywords"]), 2)
        self.assertIn(self.sample_keyword_map["apple pie recipe"], clusters[0]["keywords"])
        self.assertIn(self.sample_keyword_map["easy apple pie"], clusters[0]["keywords"])

    def test_generate_keyword_clusters_ai_returns_single_object(self):
        # AI returns a single cluster object instead of a list
        ai_response = '{"cluster_name": "Cakes", "keywords": ["chocolate cake recipe", "best chocolate cake"]}'
        self.mock_ai_client.generate.return_value = ai_response # Test without markdown fence too
        
        # Use keywords that would go into one batch for this test
        cake_keywords = [kw for kw in self.sample_keywords if "cake" in kw["keyword"]]
        clusters = generate_keyword_clusters_with_ai(cake_keywords, self.mock_ai_client, batch_size=5)
        
        self.assertEqual(len(clusters), 1)
        self.assertEqual(clusters[0]["cluster_name"], "Cakes")

    def test_generate_keyword_clusters_malformed_json(self):
        # The string content should represent malformed JSON, but the string assignment itself must be valid Python.
        # Original: "```json\n[{"cluster_name": "Malformed", keywords: ["bad"]}\n```"
        # Corrected to ensure `keywords: ["bad"]` is treated as part of the string literal:
        malformed_json_text = '[{"cluster_name": "Malformed", "keywords": ["bad"]}' # This would be valid JSON if keys were quoted
        # To make it represent malformed JSON as intended (e.g. unquoted key 'keywords'):
        malformed_json_ai_response = '```json\n[{"cluster_name": "Malformed", keywords: ["bad"]}]\n```'
        self.mock_ai_client.generate.return_value = malformed_json_ai_response
        clusters = generate_keyword_clusters_with_ai(self.sample_keywords, self.mock_ai_client, batch_size=2)
        self.assertEqual(len(clusters), 0) # Should skip malformed batch

    def test_generate_keyword_clusters_ai_returns_non_list_or_dict(self):
        self.mock_ai_client.generate.return_value = """json\n"Not a list or dict"\n"""
        clusters = generate_keyword_clusters_with_ai(self.sample_keywords, self.mock_ai_client, batch_size=2)
        self.assertEqual(len(clusters), 0)

    # Tests for generate_article_ideas_from_clusters_with_ai
    def test_generate_article_ideas_basic(self):
        sample_clusters = [
            {"cluster_name": "Apple Pies", "keywords": [self.sample_keyword_map["apple pie recipe"], self.sample_keyword_map["easy apple pie"]]}
        ]
        ai_response = '{"article_title": "Best Apple Pie Guide", "article_type": "guide"}'
        self.mock_ai_client.generate.return_value = f"```json\n{ai_response}\n```"

        ideas = generate_article_ideas_from_clusters_with_ai(sample_clusters, self.mock_ai_client)
        self.assertEqual(len(ideas), 1)
        self.assertEqual(ideas[0]["article_title"], "Best Apple Pie Guide")
        self.assertEqual(ideas[0]["article_type"], "guide")
        self.assertEqual(ideas[0]["primary_keyword"]["keyword"], "apple pie recipe") # Max searches

    # Tests for consolidate_clusters_with_ai
    def test_consolidate_clusters_should_merge(self):
        initial_clusters = [
            {"cluster_name": "Gardening Tips", "keywords": [{"keyword": "organic gardening", "avg_monthly_searches": 100}]},
            {"cluster_name": "Soil Health", "keywords": [{"keyword": "composting", "avg_monthly_searches": 200}]}
        ]
        ai_response_merge = '{"should_merge": true, "merged_cluster_name": "Organic Soil Management"}'
        self.mock_ai_client.generate.return_value = f"```json\n{ai_response_merge}\n```"

        final_clusters = consolidate_clusters_with_ai(initial_clusters, self.mock_ai_client, min_keywords_for_merge_check=0)
        self.assertEqual(len(final_clusters), 1)
        self.assertEqual(final_clusters[0]["cluster_name"], "Organic Soil Management")
        self.assertEqual(len(final_clusters[0]["keywords"]), 2)
        self.assertIn({"keyword": "organic gardening", "avg_monthly_searches": 100}, final_clusters[0]["keywords"])
        self.assertIn({"keyword": "composting", "avg_monthly_searches": 200}, final_clusters[0]["keywords"])

    def test_consolidate_clusters_should_not_merge(self):
        initial_clusters = [
            {"cluster_name": "Tech Reviews", "keywords": [{"keyword": "new smartphone", "avg_monthly_searches": 100}]},
            {"cluster_name": "Baking Recipes", "keywords": [{"keyword": "sourdough bread", "avg_monthly_searches": 200}]}
        ]
        ai_response_no_merge = '{"should_merge": false, "merged_cluster_name": null}'
        self.mock_ai_client.generate.return_value = f"```json\n{ai_response_no_merge}\n```"

        final_clusters = consolidate_clusters_with_ai(initial_clusters, self.mock_ai_client, min_keywords_for_merge_check=0)
        self.assertEqual(len(final_clusters), 2)

    def test_consolidate_clusters_ai_malformed_json(self):
        initial_clusters = [{"cluster_name": "A", "keywords": [{"keyword": "kwA"}]}, {"cluster_name": "B", "keywords": [{"keyword": "kwB"}]}]
        self.mock_ai_client.generate.return_value = "```json\n{\"should_merge\": true, \"merged_cluster_name\": \"Oops no closing brace\n```"
        final_clusters = consolidate_clusters_with_ai(initial_clusters, self.mock_ai_client, min_keywords_for_merge_check=0)
        self.assertEqual(len(final_clusters), 2) # Should skip merge on error

    def test_consolidate_clusters_ai_empty_response(self):
        initial_clusters = [{"cluster_name": "A", "keywords": [{"keyword": "kwA"}]}, {"cluster_name": "B", "keywords": [{"keyword": "kwB"}]}]
        self.mock_ai_client.generate.return_value = "" # Empty string
        final_clusters = consolidate_clusters_with_ai(initial_clusters, self.mock_ai_client, min_keywords_for_merge_check=0)
        self.assertEqual(len(final_clusters), 2) # Should skip merge

    def test_consolidate_clusters_merge_no_valid_new_name(self):
        initial_clusters = [
            {"cluster_name": "Cluster One", "keywords": [{"keyword": "kw1"}]},
            {"cluster_name": "Cluster Two", "keywords": [{"keyword": "kw2"}]}
        ]
        # AI says merge but new name is null or not a string
        ai_response = '{"should_merge": true, "merged_cluster_name": null}'
        self.mock_ai_client.generate.return_value = f"```json\n{ai_response}\n```"
        final_clusters = consolidate_clusters_with_ai(initial_clusters, self.mock_ai_client, min_keywords_for_merge_check=0)
        self.assertEqual(len(final_clusters), 1)
        self.assertEqual(final_clusters[0]["cluster_name"], "Cluster One") # Defaults to Cluster A's name

    def test_consolidate_clusters_less_than_two_clusters(self):
        initial_clusters = [{"cluster_name": "Solo Cluster", "keywords": [{"keyword": "kwA"}]}]
        final_clusters = consolidate_clusters_with_ai(initial_clusters, self.mock_ai_client)
        self.assertEqual(len(final_clusters), 1)
        self.assertEqual(final_clusters, initial_clusters) # Should return original
        self.mock_ai_client.generate.assert_not_called()

    def test_consolidate_clusters_empty_initial_list(self):
        final_clusters = consolidate_clusters_with_ai([], self.mock_ai_client)
        self.assertEqual(len(final_clusters), 0)
        self.mock_ai_client.generate.assert_not_called()
        
    def test_consolidate_min_keywords_for_merge_check(self):
        initial_clusters = [
            {"cluster_name": "Big Cluster", "keywords": [{"keyword": "kwA"}, {"keyword": "kwB"}, {"keyword": "kwC"}]},
            {"cluster_name": "Small Cluster", "keywords": [{"keyword": "kwD"}]}, # Too small to initiate merge check against others if its turn comes
            {"cluster_name": "Medium Cluster", "keywords": [{"keyword": "kwE"}, {"keyword": "kwF"}, {"keyword": "kwG"}]}
        ]
        # Mock AI to suggest no merge if called, to isolate min_keywords_for_merge_check logic
        ai_response_no_merge = '{"should_merge": false, "merged_cluster_name": null}'
        self.mock_ai_client.generate.return_value = f"```json\n{ai_response_no_merge}\n```"

        # min_keywords_for_merge_check is 3 (default)
        # "Big Cluster" vs "Small Cluster" -> Small Cluster too small, generate not called for B
        # "Big Cluster" vs "Medium Cluster" -> generate called
        # "Small Cluster" vs "Medium Cluster" -> Small Cluster (A) too small, generate not called for A
        # "Medium Cluster" is last, no more j loops
        
        consolidate_clusters_with_ai(initial_clusters, self.mock_ai_client, min_keywords_for_merge_check=2)
        
        # Expected calls:
        # Big (3) vs Small (1) -> Small is < 2, so B is skipped, A vs B not called (inner loop skip)
        # Big (3) vs Medium (3) -> A vs B called
        # Small (1) vs Medium (3) -> Small is < 2, so A is skipped, A vs B not called (outer loop skip on A)
        
        # Let's re-evaluate logic. cluster_A and cluster_B must *both* meet min_keywords_for_merge_check
        # With min_keywords_for_merge_check = 2
        # A=Big(3), B=Small(1) -> Skip (B too small)
        # A=Big(3), B=Medium(3) -> Called
        # A=Small(1) -> Skip (A too small for outer loop)

        # Re-run with min_keywords_for_merge_check=1 (effectively all clusters checked)
        self.mock_ai_client.reset_mock()
        consolidate_clusters_with_ai(initial_clusters, self.mock_ai_client, min_keywords_for_merge_check=1)
        self.assertEqual(self.mock_ai_client.generate.call_count, 3) # A-B, A-C, B-C

        self.mock_ai_client.reset_mock()
        consolidate_clusters_with_ai(initial_clusters, self.mock_ai_client, min_keywords_for_merge_check=3)
        # Big(3) vs Small(1) (skip B)
        # Big(3) vs Medium(3) (called)
        # Small(1) vs ... (skip A)
        self.assertEqual(self.mock_ai_client.generate.call_count, 1)


    def test_consolidate_clusters_keyword_deduplication(self):
        kw1 = {"keyword": "organic gardening", "avg_monthly_searches": 100}
        kw2 = {"keyword": "composting", "avg_monthly_searches": 200}
        # kw1 is also in the second cluster intentionally for dedup test
        initial_clusters = [
            {"cluster_name": "Gardening", "keywords": [kw1]},
            {"cluster_name": "Soil", "keywords": [kw2, kw1]} 
        ]
        ai_response_merge = '{"should_merge": true, "merged_cluster_name": "Organic Soil"}'
        self.mock_ai_client.generate.return_value = f"```json\n{ai_response_merge}\n```"

        final_clusters = consolidate_clusters_with_ai(initial_clusters, self.mock_ai_client, min_keywords_for_merge_check=0)
        self.assertEqual(len(final_clusters), 1)
        self.assertEqual(final_clusters[0]["cluster_name"], "Organic Soil")
        self.assertEqual(len(final_clusters[0]["keywords"]), 2) # kw1 should not be duplicated
        self.assertIn(kw1, final_clusters[0]["keywords"])
        self.assertIn(kw2, final_clusters[0]["keywords"])

    # Tests for OpenAIClient (mocking the actual OpenAI API call)
    @patch('semantic_core_kit.ai_processor.OpenAI')
    def test_openai_client_init_success(self, MockOpenAI):
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key', 'OPENAI_MODEL_NAME': 'test_model'}):
            client = OpenAIClient()
            self.assertEqual(client.api_key, 'test_key')
            self.assertEqual(client.model_name, 'test_model')
            MockOpenAI.assert_called_once_with(api_key='test_key')

    @patch('semantic_core_kit.ai_processor.OpenAI')
    def test_openai_client_init_custom_model(self, MockOpenAI):
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
            client = OpenAIClient(model_name="custom_model_provided")
            self.assertEqual(client.model_name, 'custom_model_provided')
            MockOpenAI.assert_called_once_with(api_key='test_key')

    def test_openai_client_init_no_api_key(self):
        with patch.dict('os.environ', {}, clear=True): # Ensure OPENAI_API_KEY is not set
            with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY environment variable not set"):
                OpenAIClient()

    @patch('semantic_core_kit.ai_processor.OpenAI')
    def test_openai_client_generate_success(self, MockOpenAI):
        mock_openai_instance = MockOpenAI.return_value
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content=" AI response "))]
        mock_openai_instance.chat.completions.create.return_value = mock_completion

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
            client = OpenAIClient(model_name="gpt-test")
            response = client.generate("test prompt")
            self.assertEqual(response, "AI response")
            mock_openai_instance.chat.completions.create.assert_called_once_with(
                model="gpt-test",
                messages=[{"role": "user", "content": "test prompt"}],
                temperature=0.7
            )

    @patch('semantic_core_kit.ai_processor.OpenAI')
    def test_openai_client_generate_api_error(self, MockOpenAI):
        mock_openai_instance = MockOpenAI.return_value
        mock_openai_instance.chat.completions.create.side_effect = Exception("API Error")

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
            client = OpenAIClient()
            with self.assertRaisesRegex(Exception, "API Error"):
                client.generate("test prompt")
                
    @patch('semantic_core_kit.ai_processor.OpenAI')
    def test_openai_client_generate_empty_content(self, MockOpenAI):
        mock_openai_instance = MockOpenAI.return_value
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content=None))] # API returns None content
        mock_openai_instance.chat.completions.create.return_value = mock_completion

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
            client = OpenAIClient(model_name="gpt-test")
            with self.assertRaisesRegex(ValueError, "OpenAI API returned an empty message content."):
                client.generate("test prompt")


if __name__ == '__main__':
    unittest.main()

import os
import unittest

from semantic_core_kit.utils import save_article_ideas_to_markdown


class TestUtils(unittest.TestCase):
    test_md_file = "test_article_ideas.md"

    def tearDown(self):
        if os.path.exists(self.test_md_file):
            os.remove(self.test_md_file)

    def test_save_article_ideas_to_markdown_basic(self):
        article_ideas = [
            {
                "theme": "Test Cluster 1",
                "article_title": "Awesome Title 1",
                "primary_keyword": {"keyword": "primary kw1", "avg_monthly_searches": 1000},
                "supporting_keywords": [
                    {"keyword": "support kw1a", "avg_monthly_searches": 100},
                    {"keyword": "support kw1b", "avg_monthly_searches": 150},
                ],
                "article_type": "guide",
            },
            {
                "theme": "Test Cluster 2",
                "article_title": "Another Great Title 2",
                "primary_keyword": {"keyword": "primary kw2", "avg_monthly_searches": 2000},
                "supporting_keywords": [],
                "article_type": "review",
            },
        ]
        save_article_ideas_to_markdown(article_ideas, self.test_md_file)

        self.assertTrue(os.path.exists(self.test_md_file))

        with open(self.test_md_file, encoding="utf-8") as f:
            content = f.read()

        self.assertIn("# Generated Article Ideas", content)
        self.assertIn("## Idea 1: Awesome Title 1", content)
        self.assertIn("- **Theme/Cluster:** Test Cluster 1", content)
        self.assertIn("- **Article Type:** Guide", content)
        self.assertIn("- **Primary Keyword:** primary kw1 (Avg. Searches: 1000)", content)
        self.assertIn("- **Supporting Keywords:**", content)
        self.assertIn("  - support kw1a (Avg. Searches: 100)", content)
        self.assertIn("  - support kw1b (Avg. Searches: 150)", content)
        self.assertIn("---", content)
        self.assertIn("## Idea 2: Another Great Title 2", content)
        self.assertIn("- **Theme/Cluster:** Test Cluster 2", content)
        self.assertIn("- **Article Type:** Review", content)
        self.assertIn("- **Primary Keyword:** primary kw2 (Avg. Searches: 2000)", content)
        self.assertIn("- **Supporting Keywords:** None", content)

    def test_save_empty_list(self):
        article_ideas = []
        save_article_ideas_to_markdown(article_ideas, self.test_md_file)
        self.assertTrue(os.path.exists(self.test_md_file))
        with open(self.test_md_file, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("# Generated Article Ideas", content)
        self.assertIn("No article ideas were generated.", content)

    def test_missing_fields_in_idea(self):
        article_ideas = [
            {
                "article_title": "Title with missing parts",
                # Missing theme, primary_keyword, supporting_keywords, article_type
            }
        ]
        save_article_ideas_to_markdown(article_ideas, self.test_md_file)
        self.assertTrue(os.path.exists(self.test_md_file))
        with open(self.test_md_file, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("## Idea 1: Title with missing parts", content)
        self.assertIn("- **Theme/Cluster:** N/A", content)  # Handled by .get()
        self.assertIn("- **Article Type:** N/A", content)
        self.assertIn("- **Primary Keyword:** N/A (Avg. Searches: N/A)", content)
        self.assertIn("- **Supporting Keywords:** None", content)


if __name__ == "__main__":
    unittest.main()

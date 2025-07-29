import csv
import os
import unittest

from semantic_core_kit.loader import load_and_clean_keywords


# Helper function to create a temporary CSV for testing
def create_test_csv(filepath, data):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter='\t')
        for row in data:
            writer.writerow(row)


class TestLoader(unittest.TestCase):
    test_csv_file = "test_keywords.csv"

    @classmethod
    def tearDownClass(cls):
        # Clean up the test CSV file if it exists
        if os.path.exists(cls.test_csv_file):
            os.remove(cls.test_csv_file)

    def tearDown(self):
        # Clean up the test CSV file if it exists after each test (optional, if tests modify it)
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)

    def test_load_and_clean_keywords_basic(self):
        # Test with a basic valid CSV
        csv_data = [
            ["Header1"],  # Skipped
            ["Header2"],  # Skipped
            [
                "Keyword",
                "Avg. monthly searches",
                "Competition (indexed value)",
                "Competition",
                "Extra Column",
            ],  # Headers
            ["Test Keyword 1", "1,000", "10", "Low", "extra1"],
            ["test keyword 2", "500.0", "20", "Medium", "extra2"],
            [" Test Keyword 3 ", "invalid_searches", "30", "High", "extra3"],  # Invalid searches, should default to 0
            ["", "100", "5", "Low", "empty_kw"],  # Empty keyword, should be skipped
            ["Test Keyword 1", "2000", "15", "Medium", "duplicate_higher_search"],  # Duplicate, higher search
        ]
        create_test_csv(self.test_csv_file, csv_data)

        expected_output = [
            {
                "keyword": "test keyword 1",
                "avg_monthly_searches": 2000,
                "competition_indexed_value": 15,
                "competition": "Medium",
                "original_avg_monthly_searches": "2000",
                "original_competition_indexed_value": "15",
                "original_competition": "Medium",
            },
            {
                "keyword": "test keyword 2",
                "avg_monthly_searches": 500,
                "competition_indexed_value": 20,
                "competition": "Medium",
                "original_avg_monthly_searches": "500.0",
                "original_competition_indexed_value": "20",
                "original_competition": "Medium",
            },
            {
                "keyword": "test keyword 3",
                "avg_monthly_searches": 0,
                "competition_indexed_value": 30,
                "competition": "High",
                "original_avg_monthly_searches": "invalid_searches",
                "original_competition_indexed_value": "30",
                "original_competition": "High",
            },
        ]

        result = load_and_clean_keywords(self.test_csv_file)
        # Sort by keyword for consistent comparison
        self.assertEqual(
            sorted(result, key=lambda x: x["keyword"]), sorted(expected_output, key=lambda x: x["keyword"])
        )

    def test_empty_csv(self):
        csv_data = [
            ["Header1"],
            ["Header2"],
            ["Keyword", "Avg. monthly searches", "Competition (indexed value)", "Competition"],
        ]
        create_test_csv(self.test_csv_file, csv_data)
        result = load_and_clean_keywords(self.test_csv_file)
        self.assertEqual(result, [])

    def test_file_not_found(self):
        result = load_and_clean_keywords("non_existent_file.csv")
        self.assertEqual(result, [])  # Expect an empty list and an error message printed

    def test_duplicate_handling(self):
        csv_data = [
            ["H1"],
            ["H2"],
            ["Keyword", "Avg. monthly searches", "Competition (indexed value)", "Competition"],
            ["keyword A", "100", "10", "Low"],
            ["Keyword B", "200", "20", "Medium"],
            ["keyword a", "50", "5", "Very Low"],  # Duplicate of "keyword A", lower search volume
        ]
        create_test_csv(self.test_csv_file, csv_data)
        expected_output = [
            {
                "keyword": "keyword a",
                "avg_monthly_searches": 100,
                "competition_indexed_value": 10,
                "competition": "Low",
                "original_avg_monthly_searches": "100",
                "original_competition_indexed_value": "10",
                "original_competition": "Low",
            },
            {
                "keyword": "keyword b",
                "avg_monthly_searches": 200,
                "competition_indexed_value": 20,
                "competition": "Medium",
                "original_avg_monthly_searches": "200",
                "original_competition_indexed_value": "20",
                "original_competition": "Medium",
            },
        ]
        result = load_and_clean_keywords(self.test_csv_file)
        self.assertEqual(
            sorted(result, key=lambda x: x["keyword"]), sorted(expected_output, key=lambda x: x["keyword"])
        )


if __name__ == "__main__":
    unittest.main()

import unittest
from utils.scraper import get_reviews

class TestIMDBScraper(unittest.TestCase):

    def test_review_fetching(self):
        """Test if reviews are fetched successfully for a known movie"""
        movie_name = "Interstellar"
        reviews = get_reviews(movie_name, max_reviews=5)

        # Check that we get a non-empty list
        self.assertIsInstance(reviews, list)
        self.assertGreater(len(reviews), 0, "No reviews were fetched.")
        self.assertLessEqual(len(reviews), 5)

        # Check that each review is a non-empty string
        for review in reviews:
            self.assertIsInstance(review, str)
            self.assertGreater(len(review.strip()), 0)

    def test_invalid_movie_name(self):
        """Test that invalid movie names return an empty list"""
        reviews = get_reviews("asdkjasdljkasdjklasjdklas", max_reviews=5)
        self.assertIsInstance(reviews, list)
        self.assertEqual(len(reviews), 0)

    def test_max_reviews_limit(self):
        """Test that the max_reviews parameter is respected"""
        movie_name = "Inception"
        reviews = get_reviews(movie_name, max_reviews=3)
        self.assertLessEqual(len(reviews), 3)

if __name__ == "__main__":
    unittest.main()

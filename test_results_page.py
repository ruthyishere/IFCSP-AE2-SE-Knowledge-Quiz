import unittest # importing testing framework
from unittest.mock import Mock #to mock and abstract functionality
import pandas as pd
from results_page import ResultsWindow # import code to test

class SmokeTest(unittest.TestCase):
    """
    Smoke test to make sure unittest is working properly
    """
    def test_ut_works_equals(self):
        self.assertEqual(1+1, 2)
        self.assertNotEqual(5, -99)

    def test_ut_works_bool(self):
        self.assertTrue(True)
        self.assertFalse(False)

class ResultsWindowTest(unittest.TestCase):
    """
    Test suite to test functionality of results_page.ResultsWindow
    """

    def test_calculate_score_percent(self):

        # Mock the question frames
        mock_qfs = []
        for i in range(3):
            mock = Mock()
            mock.selected_value.get.return_value = 1
            mock_qfs.append(mock)

        # Mock the correct answers
        mock_correct_answers = pd.Series([1]*3)

        # Check the score results -- it should be 100
        score_percent = ResultsWindow.calculate_score(self=Mock(), question_set=mock_qfs, correct_answers=mock_correct_answers)
        self.assertEqual(score_percent, 100)
    
    def test_calculate_score_raw(self):
            # Mock the question frames
            mock_qfs = []
            for i in range(3):
                mock = Mock()
                mock.selected_value.get.return_value = 1
                mock_qfs.append(mock)

            # Mock the correct answers
            mock_correct_answers = pd.Series([1]*3)

            # Check the score results -- it should be 3
            score_raw = ResultsWindow.calculate_score(self=Mock(), question_set=mock_qfs, correct_answers=mock_correct_answers, percent=False)
            self.assertEqual(score_raw, 3)

    def test_load_relevant_sources(self):
        # Mock the set of resources that would be a dataframe loaded from CSV file data
        mock_resource_set = pd.DataFrame({"question_id": [1,2,1,3],
                                          "resource_url": ["url1", "url2", "url1", "url3"]})

        # Invoke function that extract the relevant urls for each question from the resource set

        result = list(ResultsWindow.load_relevant_resources(self=Mock(), resource_set=mock_resource_set, question_id=1))

        self.assertEqual(result, ["url1", "url1"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
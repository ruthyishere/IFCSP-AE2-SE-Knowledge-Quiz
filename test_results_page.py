import unittest # importing testing framework
from unittest.mock import Mock
import pandas as pd
from results_page import ResultsWindow

class SmokeTest(unittest.TestCase):
    def test_ut_works_equals(self):
        self.assertEqual(1+1, 2)
        self.assertNotEqual(5, -99)

    def test_ut_works_bool(self):
        self.assertTrue(True)
        self.assertFalse(False)

class ResultsWindowTest(unittest.TestCase):

    def test_calculate_score_percent(self):
        mock_qfs = []
        for i in range(3):
            mock = Mock()
            mock.selected_value.get.return_value = 1
            mock_qfs.append(mock)

        mock_correct_answers = pd.Series([1]*3)

        score_percent = ResultsWindow.calculate_score(self=Mock(), question_set=mock_qfs, correct_answers=mock_correct_answers)
        self.assertEqual(score_percent, 100)
    
    def test_calculate_score_raw(self):
            mock_qfs = []
            for i in range(3):
                mock = Mock()
                mock.selected_value.get.return_value = 1
                mock_qfs.append(mock)
    
            mock_correct_answers = pd.Series([1]*3)

            score_raw = ResultsWindow.calculate_score(self=Mock(), question_set=mock_qfs, correct_answers=mock_correct_answers, percent=False)
            self.assertEqual(score_raw, 3)

    def test_load_relevant_sources(self):
        mock_resource_set = pd.DataFrame({"question_id": [1,2,1,3],
                                          "resource_url": ["url1", "url2", "url1", "url3"]})

        result = list(ResultsWindow.load_relevant_resources(self=Mock(), resource_set=mock_resource_set, question_id=1))

        self.assertEqual(result, ["url1", "url1"])
        
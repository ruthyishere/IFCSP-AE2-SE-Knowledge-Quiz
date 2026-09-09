import unittest # importing testing framework
from unittest.mock import patch, Mock, MagicMock
import pandas as pd
from quiz_page import SolAreaQuiz # import code to test
from main import MainQuizApp

class SmokeTest(unittest.TestCase):
    def test_ut_works_equals(self):
        self.assertEqual(1+1, 2)
        self.assertNotEqual(5, -99)

    def test_ut_works_bool(self):
        self.assertTrue(True)
        self.assertFalse(False)

class SolAreaQuizTest(unittest.TestCase):

    def setUp(self):
        self.parent = MainQuizApp()
        self.quiz_window = SolAreaQuiz(self.parent, "Data", '#d1fdf9', '#5ac5b3')

    @patch('quiz_page.SolAreaQuiz.load_csv')
    @patch('quiz_page.QuestionFrame')
    def test_load_questions(self, mock_qf, mock_load_csv):
        mock_questions = pd.DataFrame({
                    "question_id": [1, 2, 3],
                    "solution_area": "Data SE",
                    "domain": "Operational & transactional databases",
                    "subdomain": "OLTP fundamentals",
                    "question_type": "neutral_theory",
                    "level":200,
                    "question_text":"In a transactional (OLTP) database, the ACID properties guarantee reliable transaction processing. What does the 'D' in ACID stand for?",
                    "option_a": "Deduplication - duplicate rows are removed on commit",
                    "option_b": "Denormalization - tables are flattened for faster reads",
                    "option_c": "Durability - once a transaction is committed, its changes survive a system failure",
                    "option_d": "Distribution - data is automatically sharded across nodes"
        
                })_
        mock_load_csv = Mock(return_value=mock_questions)
        
        
        

    def test_load_csv(self):
        pass

    def test_display_current_question_frame(self):
        pass

    def test_change_question_frame(self):
        pass

    def test_submit(self):
        pass



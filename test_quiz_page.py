import unittest # importing testing framework
from unittest.mock import patch, Mock
import pandas as pd
from quiz_page import SolAreaQuiz # import code to test
import os
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
        self.mock_questions = pd.DataFrame({
                            "question_id": [1, 2, 3],
                            "solution_area": ["Data SE", "Data SE", "Data SE"],
                            "domain": ["Operational & transactional databases", "Operational & transactional databases", "Operational & transactional databases"],
                            "subdomain": ["OLTP fundamentals", "Azure SQL deployment options", "Cosmos DB consistency"],
                            "question_type": ["neutral_theory", "ms_theory", "ms_theory"],
                            "level":[200, 200, 300],
                            "question_text":["In a transactional (OLTP) database, the ACID properties guarantee reliable transaction processing. What does the 'D' in ACID stand for?", "A customer wants to lift-and-shift an on-premises SQL Server database to a fully managed PaaS service with the highest SQL Server feature and surface-area compatibility (e.g. SQL Agent, cross-database queries). Which option fits best?", "Azure Cosmos DB offers five consistency levels. Which level provides the lowest latency and highest availability, but the weakest consistency guarantee?"],
                            "option_a": ["Deduplication - duplicate rows are removed on commit", "Azure Database for PostgreSQL", "Session"],
                            "option_b": ["Denormalization - tables are flattened for faster reads", "Azure SQL Database (single database)", "Bounded staleness"],
                            "option_c": ["Durability - once a transaction is committed, its changes survive a system failure", "Azure SQL Managed Instance", "Eventual"],
                            "option_d": ["Distribution - data is automatically sharded across nodes", "Azure Cosmos DB", "Strong"]
                        })
        self.mock_answers = pd.DataFrame({
            'answer_id':[1, 2, 3],
            'question_id': [1, 2, 3],
            'correct_option': ['C']*3,
            'correct_answer_text': ["Durability", "Azure", "Eventual"],
            'rationale': ["Durability guarantees that once a transaction commits, its effects persist through crashes/power loss, typically via write-ahead logging. ACID = Atomicity, Consistency, Isolation, Durability.",
                          "Managed Instance provides near-100% SQL Server surface-area compatibility (SQL Agent, cross-DB queries, CLR, etc.), making it the default PaaS target for lift-and-shift.",
                          "Eventual consistency gives the lowest latency, highest availability and highest throughput, at the cost of no ordering guarantee. Strong is the opposite end of the spectrum."]
                })

        self.mock_resources = pd.DataFrame({
            "resource_id": [1, 2, 3],
            "question_id": [1, 1, 2],
            "resource_title": ["OLTP - Azure Architecture Center", "Reliability - Azure Well-Architected Framework", "What is Azure SQL? IaaS vs PaaS overview"],
            "resource_url": ["https://learn.microsoft.com/en-us/azure/architecture/data-guide/relational-data/online-transaction-processing",
                             "https://learn.microsoft.com/en-us/azure/well-architected/reliability/",
                             "https://learn.microsoft.com/en-us/azure/azure-sql/azure-sql-iaas-vs-paas-what-is-overview"],
            "source_type": ["Azure Architecture Center", "Microsoft Docs", "Microsoft Docs"]
        })


        self.mock_answers.to_csv('question_bank/mock_answers.csv', index=False)
        self.mock_questions.to_csv('question_bank/mock_questions.csv', index=False)
        self.mock_resources.to_csv('question_bank/mock_resources.csv', index=False)

    def tearDown(self):
        os.remove('question_bank/mock_answers.csv')
        os.remove('question_bank/mock_questions.csv')
        os.remove('question_bank/mock_resources.csv')

    @patch('quiz_page.QuestionFrame')
    def test_load_questions(self, mock_qf):

        mock_qfs = []
        for i in range(3):
            qf = mock_qf.return_value
            qf.question_set.return_value = self.mock_questions.iloc[i]
            if i == 0:
                qf.is_first.attribute = True
                qf.is_last.attribute = False
            elif i == 1:
                qf.is_first.attribute = False
                qf.is_last.attribute = False
            else:
                qf.is_first.attribute = False
                qf.is_last.attribute = True
            mock_qfs.append(qf)

        test_questions = SolAreaQuiz.load_questions(self=Mock(), questions_df=self.mock_questions)

        self.assertEqual(test_questions, mock_qfs)


    def test_load_csv(self):
        test_questions_df = SolAreaQuiz.load_csv(self=Mock(), choice="mock", csv_type="questions")
        test_answers_df = SolAreaQuiz.load_csv(self=Mock(), choice="mock", csv_type="answers")
        test_resources_df = SolAreaQuiz.load_csv(self=Mock(), choice="mock", csv_type="resources")

        pd.testing.assert_frame_equal(test_answers_df, self.mock_answers)
        pd.testing.assert_frame_equal(test_questions_df, self.mock_questions)
        pd.testing.assert_frame_equal(test_resources_df, self.mock_resources)


    
    @patch('tkinter.Frame.tkraise')
    def test_display_current_question_frame(self, mock_tkraise):
        self.quiz_window.display_current_question_frame()

        mock_tkraise.assert_called()

        
    @patch('quiz_page.SolAreaQuiz.display_current_question_frame')
    def test_change_question_frame(self, mock_method):
        self.quiz_window.current_question_indx = 0
        self.quiz_window.change_question_frame(1)

        mock_method.assert_called()

        self.assertEqual(self.quiz_window.current_question_indx, 1)

        self.quiz_window.change_question_frame(-1)

        self.assertEqual(self.quiz_window.current_question_indx, 0)

    @patch('tkinter.Toplevel.destroy')
    @patch('main.MainQuizApp.open_results_window')
    @patch('tkinter.messagebox.askyesnocancel')
    def test_submit(self, mock_popup, mock_method1, mock_method2):
        result = self.quiz_window.submit()
        mock_popup.assert_called_with("Submit", "Are you sure you want to submit?")
        if mock_popup.return_value:
            mock_method1.assert_called()
            mock_method2.assert_called()
        self.assertTrue(result)


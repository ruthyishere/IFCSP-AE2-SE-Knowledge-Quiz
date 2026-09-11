import unittest # importing testing framework
from unittest.mock import patch, Mock #to mock and abstract functionality
import pandas as pd
from quiz_page import SolAreaQuiz # import code to test
import os
from main import MainQuizApp

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

class SolAreaQuizTest(unittest.TestCase):

    """
    Test suite for SolAreaQuiz
    """

    def setUp(self):
        """
        setUp method from unittest.TestCase to create resources that can be reused throughout test suite, such as the parent window,
        an instance of the quiz window to be tested, and some mock questions, answers and resources.
        
        """
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
        """
        This is automatically run at the end of the test suite to clear any temporary resources such as files
        """
        os.remove('question_bank/mock_answers.csv')
        os.remove('question_bank/mock_questions.csv')
        os.remove('question_bank/mock_resources.csv')

    @patch('quiz_page.QuestionFrame') # Mock the QuestionFrame class
    def test_load_questions(self, mock_qf):

        # Creation of mock QuestionFrames that mimic the real questions that will be displayed one by one on the quiz window
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

        # Testing load_questions and comparing it's output to the mock_qfs -- they should be equal for test to pass
        test_questions = SolAreaQuiz.load_questions(self=Mock(), questions_df=self.mock_questions)

        self.assertEqual(test_questions, mock_qfs)


    def test_load_csv(self):
        """
        Uses pd.testing;
        Loads the three types of csv files and compares them to the ground truth data formatted in setUp()
        """
        test_questions_df = SolAreaQuiz.load_csv(self=Mock(), choice="mock", csv_type="questions")
        test_answers_df = SolAreaQuiz.load_csv(self=Mock(), choice="mock", csv_type="answers")
        test_resources_df = SolAreaQuiz.load_csv(self=Mock(), choice="mock", csv_type="resources")

        pd.testing.assert_frame_equal(test_answers_df, self.mock_answers)
        pd.testing.assert_frame_equal(test_questions_df, self.mock_questions)
        pd.testing.assert_frame_equal(test_resources_df, self.mock_resources)


    
    @patch('tkinter.Frame.tkraise') # Mock the tkraise method
    def test_display_current_question_frame(self, mock_tkraise):
        #Tests if current question frame is at the top of the stack of frames, and thus visible to the user
        self.quiz_window.display_current_question_frame()

        mock_tkraise.assert_called()

        
    @patch('quiz_page.SolAreaQuiz.display_current_question_frame') # Mock the display_current_question_frame method
    def test_change_question_frame(self, mock_method):
        # Reset current question frame pointer and make it point to the second frame
        self.quiz_window.current_question_indx = 0
        self.quiz_window.change_question_frame(1)

        # check if mock display_current_question_frame has been called
        mock_method.assert_called()

        # check that the current question frame pointer is equal to 1 (the second frame)
        self.assertEqual(self.quiz_window.current_question_indx, 1)

        # Decrement the pointed
        self.quiz_window.change_question_frame(-1)

        # check if currently pointing to the first frame
        self.assertEqual(self.quiz_window.current_question_indx, 0)

    @patch('tkinter.Toplevel.destroy') # Mock the destroy method
    @patch('main.MainQuizApp.open_results_window') # Mock the open_results_window method
    @patch('tkinter.messagebox.askyesnocancel') # Mock the messagebox popup
    def test_submit(self, mock_popup, mock_method1, mock_method2):
        """
        Checks if pop up is invoked, if the method to open the results window is called, and if the
        quiz window is finally shut down, then see if submit returns True, which would indicate no errors
        """
        result = self.quiz_window.submit()
        mock_popup.assert_called_with("Submit", "Are you sure you want to submit?")
        if mock_popup.return_value:
            mock_method1.assert_called()
            mock_method2.assert_called()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main(verbosity=2)
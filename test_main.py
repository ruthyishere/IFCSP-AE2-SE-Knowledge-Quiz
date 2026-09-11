import unittest # importing testing framework
from unittest.mock import patch, Mock #to mock and abstract functionality
from main import MainQuizApp # import code to test

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

class MainQuizAppTest(unittest.TestCase):

    """
    Test suite for MainQuizApp
    """

    def setUp(self):
        # Set up the app so that it can be used and referenced throughout the test suite
        self.app = MainQuizApp()

    
    @patch('main.MainQuizApp.open_quiz_window') # Mock the open_quiz_window method
    @patch('tkinter.messagebox.askyesnocancel') # Mock the messagebox pop up window
    def test_confirm_quiz_choice(self, mock_popup, mock_method):
        # Test if confirm_quiz_choice is cakked and produces the pop up

        result = self.app.confirm_quiz_choice("Solution Area")
        mock_popup.assert_called_with("Confirm Choice: Solution Area", "Your chosen topic: Solution Area. Are you sure?")
        if mock_popup.return_value:
            mock_method.assert_called_with("Solution Area")
            self.assertTrue(result)
        else:
            self.assertFalse(result)

    @patch('main.SolAreaQuiz') # Mock the quiz window
    def test_open_quiz_window(self, mock_quiz_window):
        # Test open_quiz_window and if quiz window gets opened with the provided parameters passed
        # Test to see if window freezes other parts of app as it remains open

        mock_choice = "Data"
        mock_colours = self.app.colour_theme[mock_choice][1:]

        window = self.app.open_quiz_window(
            mock_choice
        )

        mock_quiz_window.assert_called_with(
            self.app,
            mock_choice,
            *mock_colours
        )

        mock_quiz_window.return_value.grab_set.assert_called()

        self.assertEqual(window, "OK")

    @patch('main.ResultsWindow') # Mock results window 
    def test_open_results_window(self, mock_result_window):

       # Provide mocked parameters
       mock_container = Mock()
       mock_question_set = Mock()
       mock_answer_set = Mock()
       mock_resource_set = Mock()
       mock_sol_area = "Solution Area"
       mock_colours = ("FFFFFF", "000000")

       # invoke method to be tested, sending in mocked parameters
       window = self.app.open_results_window(
           mock_container,
           mock_question_set,
           mock_answer_set,
           mock_resource_set,
           mock_sol_area,
           *mock_colours
       )

       # Check if method was called correctly with the provided params
       mock_result_window.assert_called_with(
           self.app,
           mock_container,
           mock_question_set,
           mock_answer_set,
           mock_resource_set,
           mock_sol_area,
           *mock_colours
       )

       # Check if mock window has been generated and is freezing the rest of the application as it opened
       mock_result_window.return_value.grab_set.assert_called()

       self.assertTrue(window) # check if method returned True with no errors



if __name__ == '__main__':
    unittest.main(verbosity=2)
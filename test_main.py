import unittest # importing testing framework#
from unittest.mock import patch, Mock
from main import MainQuizApp # import code to test

class SmokeTest(unittest.TestCase):
    def test_ut_works_equals(self):
        self.assertEqual(1+1, 2)
        self.assertNotEqual(5, -99)

    def test_ut_works_bool(self):
        self.assertTrue(True)
        self.assertFalse(False)

class MainQuizAppTest(unittest.TestCase):

    def setUp(self):
        self.app = MainQuizApp()

    
    @patch('main.MainQuizApp.open_quiz_window')
    @patch('tkinter.messagebox.askyesnocancel')
    def test_confirm_quiz_choice(self, mock_popup, mock_method):
        result = self.app.confirm_quiz_choice("Solution Area")
        mock_popup.assert_called_with("Confirm Choice: Solution Area", "Your chosen topic: Solution Area. Are you sure?")
        if mock_popup.return_value:
            mock_method.assert_called_with("Solution Area")
            self.assertTrue(result)
        else:
            self.assertFalse(result)

    @patch('main.SolAreaQuiz')
    def test_open_quiz_window(self, mock_quiz_window):
        # SolAreaQuiz(self, choice, *self.colour_theme[choice][1:])
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

    @patch('main.ResultsWindow')
    def test_open_results_window(self, mock_result_window):
       mock_container = Mock()
       mock_question_set = Mock()
       mock_answer_set = Mock()
       mock_resource_set = Mock()
       mock_sol_area = "Solution Area"
       mock_colours = ("FFFFFF", "000000")

       window = self.app.open_results_window(
           mock_container,
           mock_question_set,
           mock_answer_set,
           mock_resource_set,
           mock_sol_area,
           *mock_colours
       )

       mock_result_window.assert_called_with(
           self.app,
           mock_container,
           mock_question_set,
           mock_answer_set,
           mock_resource_set,
           mock_sol_area,
           *mock_colours
       )

       mock_result_window.return_value.grab_set.assert_called()

       self.assertTrue(window)



if __name__ == '__main__':
    unittest.main(verbosity=2)
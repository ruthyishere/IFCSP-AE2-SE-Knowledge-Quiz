import tkinter as tk # For GUI 
from tkinter import messagebox # For message pop ups
from quiz_page import SolAreaQuiz # For main quiz windpw
from results_page import ResultsWindow # For display of results 


class MainQuizApp(tk.Tk):
    """
    Main App Window that will display options for user
    Methods:
        confirm_choice
        open_window
    """
    def __init__(self):
        # Set up the Main App

        super().__init__()

        self.title("SE Knowledge Quiz App")           
        self.geometry("1000x800")
        self.bg_colour = "#E3E3E3"
        self.config(bg=self.bg_colour)
        self.colour_theme = {
            "AI/Apps":[ "#d7919d", "#f0cfd5", "#eb445a"],
            "Data": ["#8ad3cb", "#d1fdf9", "#5ac5b3"],
            "Infrastructure":[ "#99cde0", "#c7f1fd", "#5cc1e6"]
        }

        # Set up the main title for the window

        tk.Label(self, text="Welcome to the", bg=self.bg_colour, font=("Arial", 20)).pack()

        tk.Label(self, text="Cloud & AI Solution Engineering Knowledge Quiz!", bg=self.bg_colour, font=("Arial", 30, "bold")).pack()

        # Create instructions for the user

        instruction_text = "Choose a solution area to test your technical and consultative knowledge on! You will then be presented with a series of multiple choice questions to answer. At the end, your score will be presented to you and you will have the chance to see where you can improve and links to further help your upskilling."
        tk.Label(self, text=instruction_text, font=("Arial", 10), wraplength=500).pack(pady=10)

        tk.Label(self, text="Choose a Solution Area! 👇", font=("Arial", 30), bg=self.bg_colour, fg="#FFFFFF").pack(pady=40)

        # Create button options for different solution area options

        tk.Button(self,
                text="AI/Apps",
                bg=self.colour_theme["AI/Apps"][0],
                fg="white",
                font=('Arial', 20),
                width = 25,
                command=lambda: self.confirm_quiz_choice("AI/Apps")).pack(pady=10)

        tk.Button(self,
                text="Data",
                bg=self.colour_theme["Data"][0],
                fg="white",
                font=('Arial', 20),
                width = 25,
                command=lambda: self.confirm_quiz_choice("Data")).pack(pady=10)

        tk.Button(self,
                text="Infrastructure",
                bg=self.colour_theme["Infrastructure"][0],
                fg="white",
                font=('Arial', 20),
                width = 25,
                command=lambda: self.confirm_quiz_choice("Infrastructure")).pack(pady=10)

    def confirm_quiz_choice(self, choice):
        '''
        Produces message box to confirm if user has made the right choice, then triggers another method that opens another quiz app window.
        
        args:
            choice (str): the selected quiz topic as a string
        returns:
            True (bool): if there are no Exceptions thrown
            OR False if there are exceptions thrown
        '''
        result = messagebox.askyesnocancel(f"Confirm Choice: {choice}", f"Your chosen topic: {choice}. Are you sure?")
        try:
            if result:
                self.open_quiz_window(choice)
            return True
        except:
            return False

    def open_quiz_window(self, choice):
        """
        Creates seperate window to host quiz of user's choice

        args:
            choice (str): the selected quiz topic as a string
        returns:
            "OK" (str): if there are no Exceptions thrown
            OR e (Exception) if there are exceptions thrown
        """
        try:
            colours = self.colour_theme[choice][1:]
            window = SolAreaQuiz(self, choice, *colours)
            window.grab_set()
            return "OK"
        except Exception as e:
            return e

    def open_results_window(self, question_set, answer_set, resources_set, sol_area, *colours):
        """
        Creates seperate window to host display results of user's quiz

        args:
            question_set (QuestionFrame): list of questions in the form on tk.Frames, with the associated user answers
            answer_set (pandas.DataFrame): corresponding set of answers for the questions, loaded from csv file into a pandas df
            resource_set (pandas.DataFrame): corresponding set of documentation links for the questions and answers, loaded from csv file into a pandas df
            sol_area (str): the selected quiz topic as a string
            colours (tuple of str): colour theme for the results window as a tuple of two hex strings
        returns:
            True (bool): if there are no Exceptions thrown
            OR False if there are exceptions thrown
        
        """
        try:
            window = ResultsWindow(self, question_set, answer_set, resources_set, sol_area, *colours)
            window.grab_set()
            return True
        except:
            return False

    

    
        

if __name__ == "__main__":
    app = MainQuizApp()
    app.mainloop()


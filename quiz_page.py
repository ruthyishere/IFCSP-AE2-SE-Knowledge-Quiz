import tkinter as tk # For GUI
from tkinter import messagebox # For message popups
import pandas as pd # for importing structured data from csv


class SolAreaQuiz(tk.Toplevel):
    """
    Main quiz window for the application.

    It contains several tk.Frames (QuestionFrames) that display each question, and buttons that navigate to the next or previous question.
    
    It has a colour theme depending on the topic the user chooses.

    It imports the question, answer and resource data from CSVs and loads them into Pandas DataFrames and displays the first question.
    
    Methods:
        load_questions
        load_csv
        display_current_question_frame
        change_question_frame
        submit
    """
    def __init__(self, parent, sol_area, *colours):
        # Set up main quiz window 
        super().__init__(parent)

        self.geometry("800x800")
        self.title(f'{sol_area} Knowledge Quiz')
        self.bg_colour, self.bold_font_colour = colours
        self.config(bg=self.bg_colour)
        self.parent = parent
        self.sol_area = sol_area

        # Configure window such that widgets within the window render properly

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Load the CSV file data and set current frame pointer to 0

        sol_area_map = {"AI/Apps": "apps", "Data": "data", "Infrastructure": "infra"}

        try:
            self.questions_df = self.load_csv(sol_area_map[sol_area], "questions")
            self.answers_df = self.load_csv(sol_area_map[sol_area], "answers")
            self.resources_df = self.load_csv(sol_area_map[sol_area], "resources")
            self.question_frames = self.load_questions(self.questions_df)
        except Exception as e:
            tk.Label(self, text=f"Urmmmm... So yeah... this is awkward... 😅", bg=self.bg_colour, fg=self.bold_font_colour, font=("Arial", 20, 'bold')).pack()
            tk.Label(self, text=f"Something went wrong with loading the quiz data! --> {e}", bg=self.bg_colour, font=("Arial", 20), wraplength=500).pack()
        else:

            self.current_question_indx = 0

            # Set up title displayed on the window and display the first question

            frame_for_labels = tk.Frame(self)
            frame_for_labels.grid(row=0, column=0)

            tk.Label(frame_for_labels, text=f"{sol_area}", bg=self.bg_colour, fg=self.bold_font_colour, font=("Arial", 20, 'bold')).pack(side=tk.LEFT)
            tk.Label(frame_for_labels, text="Knowledge Quiz", bg=self.bg_colour, font=("Arial", 20)).pack(side=tk.LEFT)

            self.display_current_question_frame()

    def load_questions(self, questions_df):
        """
        Extracts question set from provided data frame and creates a list of QuestionFrame objects that will be used to display each question
                
        args:
            questions_df (pd.DataFrame): question set in a DataFrame
        returns:
            qfs (list[QuestionFrame]): a list of QuestionFrames
            OR False (bool) if there are exceptions thrown
        """
        try:
            size = len(questions_df)
            qfs = []
            for i in range(size):
                if i == 0:
                    first, last = True, False
                elif i == size - 1:
                    first, last = False, True
                else:
                    first, last = False, False
                qf = QuestionFrame(self, questions_df.iloc[i], first, last)
                qfs.append(qf)
                qf.grid(row=1, column=0, sticky='nswe')
            return qfs
        except Exception as e:
            return False


    def load_csv(self, choice, csv_type):
        """
        Extracts data from csv and loads them into a pandas DataFrame
                
        args:
            choice (str): the selected quiz topic as a string
            csv_type (str): whether the csv contains answer, questions, or resources for further reading, as a string
        returns:
            pandas DataFrame of chosen content
        """
        with open(f"question_bank/{choice}_{csv_type}.csv", "r") as file:
            return pd.read_csv(file)

    def display_current_question_frame(self):
        """
        Displays the chosen QuestionFrame on the main quiz window
                
        args:
            None
        returns:
            None
        """
        self.question_frames[self.current_question_indx].tkraise()

    def change_question_frame(self, direction):
        """
        Changes the QuestionFrame and invokes another method to display it
                
        args:
            None
        returns:
            None
        """
        self.current_question_indx += direction
        self.display_current_question_frame()

    def submit(self):
        """
        Submits the users answers by sending the list of question frames, and the associated answers, resources etc to a new window

        Destroys / shuts the current quiz window down.
                
        args:
            None
        returns:
            True (bool) if there are no exceptions thrown
            False (bool) if there is
        """
        try:
            result = messagebox.askyesnocancel(f"Submit", f"Are you sure you want to submit?")
            if result:
                self.destroy()
                self.parent.open_results_window(self.question_frames, self.answers_df, self.resources_df, self.sol_area, self.bg_colour, self.bold_font_colour)
            return True
        except Exception as e:
            return False

class QuestionFrame(tk.Frame):
    """
    A tk.Frame that will sit on the main quiz window. 

    This will display the question text and the answer options from which the user picks.

    It will present buttons to navigate to a new QuestionFrame, which the window will display

    It will save the user's answer selection - they can navigate back to the QuestionFrame and change their answer, which will also be saved

    The last QuestionFrame will have an option to submit the final set of answers (in the QuestionFrames), which quiz window will handle the request of.
    
    """
    def __init__(self, container, question_set, is_first = True, is_last=False):

        # Configure the QuestionFrame and it's appearance
        super().__init__(container)
        self.is_first = is_first
        self.is_last = is_last
        self.question_set = question_set
        self.question_id = int(self.question_set['question_id'])
        self.configure(bg=container.bg_colour)

        # Sub frame for text that displays the question

        frame_for_question = tk.Frame(self, bg=container.bg_colour)
        frame_for_question.pack(pady=10)

        tk.Label(frame_for_question, text=f"Question {self.question_id}: ", bg=container.bg_colour, font=("Arial", 20, 'bold')).pack(fill='x')
        tk.Label(frame_for_question, text=self.question_set.loc['question_text'], bg=container.bg_colour, font=("Arial", 20), wraplength=600).pack()

        # Sub frame that displays the four radio buttons, each with text that displays an answer the user can pick

        frame_for_options = tk.Frame(self, bg=container.bg_colour)
        frame_for_options.pack(pady=10)

        self.selected_value = tk.StringVar()
        cols = ['option_a', 'option_b', 'option_c', 'option_d']
        radio_button_vals = ['A', 'B', 'C', 'D']

        for i, col, rbv in zip(range(4), cols, radio_button_vals):
            tk.Radiobutton(frame_for_options, text=self.question_set.loc[col], variable=self.selected_value, value=rbv, bg=container.bg_colour, font=("Arial", 20), wraplength=1000).grid(row=i, column=0, sticky='w')

        # Sub frame that displays the buttons to navigate to the adjacent QuestionFrame

        frame_for_buttons = tk.Frame(self, bg=container.bg_colour)
        frame_for_buttons.pack(fill='x', pady=10)
        frame_for_buttons.config(bg=container.bg_colour)

        self.next_btn = tk.Button(frame_for_buttons,
                            text="Next",
                            font=('Arial', 20),
                            command=lambda: container.change_question_frame(1))
        self.prev_btn = tk.Button(frame_for_buttons,
                            text="Back",
                            font=('Arial', 20),
                            command=lambda: container.change_question_frame(-1))
        self.submit_btn = tk.Button(frame_for_buttons,
                            text="Submit",
                            font=('Arial', 20, "bold"),
                            command=container.submit)
        if self.is_first:
            self.next_btn.pack(side='right', padx=50)
        elif self.is_last:
            self.submit_btn.pack(side='right', padx=50)
            self.prev_btn.pack(side='left', padx=50)
        else:
            self.next_btn.pack(side='right', padx=50)
            self.prev_btn.pack(side='left', padx=50)

            

import tkinter as tk # For GUI
import webbrowser # For creation of clickable hyperlinks

class ResultsWindow(tk.Toplevel):
    """
    Main results window for the application that displays the results of each user answer one at a time.

    Displays tk.Frames (AnswerFrame) one at a time, with buttons to navigate to the next or previous answer breakdown
    
    It has a colour theme depending on the topic the user chooses.

    It assumes that the question set containing user answers, correct ground truth answer set, the set of documentation and resource links for further reading are already available
    
    Methods:
        calculate_score
        display_current_question_frame
        change_question_frame
        load_answer_frames
        load_relevant_resources
    """
    def __init__(self, parent, question_set, answer_set, resource_set, sol_area, *colours):

        # Set up the ResultsWindow 
        super().__init__(parent)

        self.geometry("800x800")
        self.title(f'Results Page')
        self.bg_colour, self.bold_font_colour = colours
        self.config(bg=self.bg_colour)

        self.question_set = question_set
        self.answer_set = answer_set
        self.correct_answers = self.answer_set.loc[:, 'correct_option']
        self.resource_set = resource_set
        self.sol_area = sol_area
        self.answer_frames = []
        self.current_question_indx = 0

        # Set up title displayed in the window

        frame_for_labels = tk.Frame(self, bg=self.bg_colour)
        frame_for_labels.grid(row=0, column=0)

        self.columnconfigure(0, weight=1)

        tk.Label(frame_for_labels, text=f"{self.sol_area}", bg=self.bg_colour, fg=self.bold_font_colour, font=("Arial", 20, 'bold')).pack(side=tk.LEFT)
        tk.Label(frame_for_labels, text="Knowledge Quiz", bg=self.bg_colour, font=("Arial", 20)).pack(side=tk.LEFT)

        # Set up and display the score

        frame_for_score = tk.Frame(self, bg=self.bg_colour)
        frame_for_score.grid(row=1, column=0) 

        tk.Label(frame_for_score, text="Your Score!", bg=self.bg_colour, font=("Arial", 20, 'bold')).pack(pady=30)
        tk.Label(frame_for_score, text=f"{self.calculate_score(self.question_set, self.correct_answers)}%", bg=self.bg_colour, font=("Arial", 40)).pack(pady=20)
        tk.Label(frame_for_score, text=f"{self.calculate_score(self.question_set, self.correct_answers, percent=False)}/{len(self.question_set)} answered correctly!", bg=self.bg_colour, font=("Arial", 30)).pack(pady=30)

        # Set up and display the button to navigate the different answers

        frame_for_btn = tk.Frame(self, bg=self.bg_colour)
        frame_for_btn.grid(row=2, column=0, sticky='e', padx=30)
        self.results_btn = tk.Button(frame_for_btn,
                    text="Get Results Breakdown",
                    font=('Arial', 20),
                    command=self.load_answer_frames)
        self.results_btn.pack()

    def calculate_score(self, question_set, correct_answers, percent=True):
        """
        Calculates score for the user.

        args:
            question_set (list[QuestionFrame]): question frame object list with the user selected answers for each one
            correct_answers (pd.DataFrame): ground truth correct answers for comparison
        returns:
            score (int): either as a percentage or the raw number

        """
        score = 0
        for i in range(len(question_set)):
            if question_set[i].selected_value.get() == correct_answers.iloc[i]:
                score += 1
        if percent:
            return int(score * 100 / len(question_set))
        else:
            return score

    def display_current_answer_frame(self):
        """
        Displays the chosen AnswerFrame on the main quiz window
                
        args:
            None
        returns:
            None
        """
        self.answer_frames[self.current_question_indx].tkraise()

    def change_answer_frame(self, direction):
        """
        Changes the AnswerFrame and invokes another method to display it
                
        args:
            None
        returns:
            None
        """
        self.current_question_indx += direction
        self.display_current_answer_frame()

    def load_answer_frames(self):
        """
        Extracts ground truth answer set from provided data frame and user answers and creates a list of AnswerFrame objects that will be used to display each answer breakdown
        Displays the first AnswerFrame and gets rid of a now redundant button.

        args:
            None
        returns:
            None
        """
        size = len(self.answer_set)
        for i in range(size):
            if i == 0:
                first, last = True, False
            elif i == size - 1:
                first, last = False, True
            else:
                first, last = False, False
            af = AnswerFrame(self, 
                             self.question_set[i], 
                             self.answer_set.iloc[i], 
                             self.load_relevant_resources(self.resource_set, self.question_set[i].question_id), 
                             self.question_set[i].selected_value.get() == self.correct_answers.iloc[i], 
                             first, 
                             last)
            self.answer_frames.append(af)
            af.grid(row=1, column=0, sticky='nswe')
        self.display_current_answer_frame()
        self.results_btn.destroy()

    def load_relevant_resources(self, resource_set, question_id):
        """
        Extracts ground truth answer set from provided data frame and creates a list of AnswerFrame objects that will be used to display each answer breakdown
        Displays the first AnswerFrame and gets rid of a now redundant button.

        args:
            resource_set (DataFrame)
            question_id (int)
        returns:
            subset of resource_set(DataFrame or Series)
        """
        return resource_set[resource_set['question_id'] == question_id].loc[:, 'resource_url']



class AnswerFrame(tk.Frame):

    """
        A tk.Frame that will sit on the results window. 
    
        This will display the question text, the user answer, the correct answer, the explanation behind the correct answer and hyperlinks to read further
    
        It will present buttons to navigate to a new AnswerFrame, which the window will display
    

        """
    def __init__(self, container, question, answer, resources, is_correct, is_first = True, is_last=False):

        # Set up the AnswerFrame. container will be the ResultsWindow. 
        super().__init__(container)
        self.is_first = is_first
        self.is_last = is_last
        self.question = question
        self.answer = answer
        self.resources = resources
        self.correct_text = "Correct! ✅" if is_correct else "Incorrect! ❌"
        self.configure(bg=container.bg_colour)

        #Set up sub frame to display the question

        frame_for_question = tk.Frame(self, bg=container.bg_colour)
        frame_for_question.pack(pady=10)

        tk.Label(frame_for_question, text=f"Question {self.question.question_id}: ", bg=container.bg_colour, font=("Arial", 20, 'bold')).pack(fill='x')
        tk.Label(frame_for_question, text=self.question.question_set.loc['question_text'], bg=container.bg_colour, font=("Arial", 20), wraplength=800).pack()
        tk.Label(frame_for_question, text=self.correct_text, bg=container.bg_colour, font=("Arial", 20)).pack()

        # Set up the subframe for to display the user answer and the correct answer
        frame_for_answers = tk.Frame(self, bg=container.bg_colour)
        frame_for_answers.pack(pady=10)

        option_dict = {'A':'option_a', 'B':'option_b', 'C':'option_c', 'D':'option_d'}

        try:
            user_answer = self.question.question_set.loc[option_dict[self.question.selected_value.get()]]
        except KeyError:
            user_answer = "No answer given"
        correct_answer = self.question.question_set.loc[option_dict[self.answer.loc['correct_option']]]

        tk.Label(frame_for_answers, text=f"Your answer: ", bg=container.bg_colour, font=("Arial", 20, 'bold')).pack()
        tk.Label(frame_for_answers, text=user_answer, bg=container.bg_colour, font=("Arial", 20), wraplength=800).pack()
        tk.Label(frame_for_answers, text=f"Correct answer: ", bg=container.bg_colour, font=("Arial", 20, 'bold')).pack()
        tk.Label(frame_for_answers, text=correct_answer, bg=container.bg_colour, font=("Arial", 20), wraplength=800).pack()

        # Set up the sub frame for the explanation of why the correct answer is correct

        frame_for_explanation = tk.Frame(self, bg=container.bg_colour)
        frame_for_explanation.pack(pady=10)
        tk.Label(frame_for_explanation, text=f"Explanation: {self.answer.loc['rationale']}", bg=container.bg_colour, font=("Arial", 20), wraplength=800).pack()

        # Set up frame to display the hyperlinks 

        frame_for_resources = tk.Frame(self)
        frame_for_resources.pack(pady=10)

        # Reference for hyperlink code --> https://stackoverflow.com/a/23482749
        tk.Label(frame_for_resources, text="Learn more by clicking on the following links:", font=("Arial", 20)).pack()

        for resource in resources:
            lbl = tk.Label(frame_for_resources, text=f" • {resource}", font=("Arial", 20, "underline"), fg='blue', cursor='hand2')
            lbl.pack()
            lbl.bind("<Button-1>", lambda e, resource=resource: webbrowser.open_new_tab(resource))

        # Create sub frames for buttons to navigate to adjacent frames

        frame_for_buttons = tk.Frame(self, bg=container.bg_colour)
        frame_for_buttons.pack(fill='x', pady=10)
        frame_for_buttons.config(bg=container.bg_colour)

        self.next_btn = tk.Button(frame_for_buttons,
                            text="Next",
                            font=('Arial', 20),
                            command=lambda: container.change_answer_frame(1))
        self.prev_btn = tk.Button(frame_for_buttons,
                            text="Back",
                            font=('Arial', 20),
                            command=lambda: container.change_answer_frame(-1))
        if self.is_first:
            self.next_btn.pack(side='right', padx=50)
        elif self.is_last:
            self.prev_btn.pack(side='left', padx=50)
        else:
            self.next_btn.pack(side='right', padx=50)
            self.prev_btn.pack(side='left', padx=50)

    
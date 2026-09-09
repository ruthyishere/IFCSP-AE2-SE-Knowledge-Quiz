import tkinter as tk
from tkinter import messagebox
import pandas as pd
import webbrowser

class ResultsWindow(tk.Toplevel):
    def __init__(self, parent, question_set, answer_set, resource_set, sol_area, *colours):
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
        self.score = self.calculate_score()

        frame_for_labels = tk.Frame(self, bg=self.bg_colour)
        frame_for_labels.grid(row=0, column=0)

        self.columnconfigure(0, weight=1)

        tk.Label(frame_for_labels, text=f"{self.sol_area}", bg=self.bg_colour, fg=self.bold_font_colour, font=("Arial", 20, 'bold')).pack(side=tk.LEFT)
        tk.Label(frame_for_labels, text="Knowledge Quiz", bg=self.bg_colour, font=("Arial", 20)).pack(side=tk.LEFT)

        frame_for_score = tk.Frame(self, bg=self.bg_colour)
        frame_for_score.grid(row=1, column=0) 

        tk.Label(frame_for_score, text="Your Score!", bg=self.bg_colour, font=("Arial", 20, 'bold')).pack(pady=30)
        tk.Label(frame_for_score, text=f"{self.score}%", bg=self.bg_colour, font=("Arial", 40)).pack(pady=20)
        tk.Label(frame_for_score, text=f"{self.calculate_score(percent=False)}/{len(self.question_set)} answered correctly!", bg=self.bg_colour, font=("Arial", 30)).pack(pady=30)


        frame_for_btn = tk.Frame(self, bg=self.bg_colour)
        frame_for_btn.grid(row=2, column=0, sticky='e', padx=30)
        self.results_btn = tk.Button(frame_for_btn,
                    text="Get Results Breakdown",
                    font=('Arial', 20),
                    command=self.load_answer_frames)
        self.results_btn.pack()

    def calculate_score(self, percent=True):
        score = 0
        for i in range(len(self.question_set)):
            if self.question_set[i].selected_value.get() == self.correct_answers.iloc[i]:
                score += 1
        if percent:
            return int(score * 100 / len(self.question_set))
        else:
            return score

    def display_current_question_frame(self):
        self.answer_frames[self.current_question_indx].tkraise()

    def reset_and_display_frame(self):
        self.current_question_indx = 0
        self.display_current_question_frame()

    def change_question_frame(self, direction):
        self.current_question_indx += direction
        self.display_current_question_frame()

    def load_answer_frames(self):
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
                             self.load_relevant_resources(self.question_set[i].question_id), 
                             self.question_set[i].selected_value.get() == self.correct_answers.iloc[i], 
                             first, 
                             last)
            self.answer_frames.append(af)
            af.grid(row=1, column=0, sticky='nswe')
        self.display_current_question_frame()
        self.results_btn.destroy()

    def load_relevant_resources(self, question_id):
        return self.resource_set[self.resource_set['question_id'] == question_id].loc[:, 'resource_url']



class AnswerFrame(tk.Frame):
    def __init__(self, container, question, answer, resources, is_correct, is_first = True, is_last=False):
        super().__init__(container)
        self.is_first = is_first
        self.is_last = is_last
        self.question = question
        self.answer = answer
        self.resources = resources
        self.correct_text = "Correct! ✅" if is_correct else "Incorrect! ❌"
        self.configure(bg=container.bg_colour)

        frame_for_question = tk.Frame(self, bg=container.bg_colour)
        frame_for_question.pack(pady=10)

        tk.Label(frame_for_question, text=f"Question {self.question.question_id}: ", bg=container.bg_colour, font=("Arial", 20, 'bold')).pack(fill='x')
        tk.Label(frame_for_question, text=self.question.question_set.loc['question_text'], bg=container.bg_colour, font=("Arial", 20), wraplength=800).pack()
        tk.Label(frame_for_question, text=self.correct_text, bg=container.bg_colour, font=("Arial", 20)).pack()


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

        frame_for_explanation = tk.Frame(self, bg=container.bg_colour)
        frame_for_explanation.pack(pady=10)
        tk.Label(frame_for_explanation, text=f"Explanation: {self.answer.loc['rationale']}", bg=container.bg_colour, font=("Arial", 20), wraplength=800).pack()

        frame_for_resources = tk.Frame(self)
        frame_for_resources.pack(pady=10)

        # Reference for hyperlink code --> https://stackoverflow.com/a/23482749
        tk.Label(frame_for_resources, text="Learn more by clicking on the following links:", font=("Arial", 20)).pack()

        for resource in resources:
            lbl = tk.Label(frame_for_resources, text=f" • {resource}", font=("Arial", 20, "underline"), fg='blue', cursor='hand2')
            lbl.pack()
            lbl.bind("<Button-1>", lambda e, resource=resource: webbrowser.open_new_tab(resource))


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
        if self.is_first:
            self.next_btn.pack(side='right', padx=50)
        elif self.is_last:
            self.prev_btn.pack(side='left', padx=50)
        else:
            self.next_btn.pack(side='right', padx=50)
            self.prev_btn.pack(side='left', padx=50)

    
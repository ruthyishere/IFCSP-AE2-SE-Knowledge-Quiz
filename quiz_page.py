import tkinter as tk
from tkinter import messagebox
import pandas as pd

class QuestionFrame(tk.Frame):
    def __init__(self, container, question_set, is_first = True, is_last=False): #question_set
        super().__init__(container)
        self.is_first = is_first
        self.is_last = is_last
        self.question_set = question_set
        self.question_id = int(self.question_set['question_id'])
        self.configure(bg=container.bg_colour)

        frame_for_question = tk.Frame(self, bg=container.bg_colour)
        frame_for_question.pack(pady=10)

        tk.Label(frame_for_question, text=f"Question {self.question_id}: ", bg=container.bg_colour, font=("Arial", 20, 'bold')).pack(fill='x')
        tk.Label(frame_for_question, text=self.question_set.loc['question_text'], bg=container.bg_colour, font=("Arial", 20), wraplength=600).pack()

        frame_for_options = tk.Frame(self, bg=container.bg_colour)
        frame_for_options.pack(pady=10)

        self.selected_value = tk.StringVar()
        cols = ['option_a', 'option_b', 'option_c', 'option_d']
        radio_button_vals = ['A', 'B', 'C', 'D']

        for i, col, rbv in zip(range(4), cols, radio_button_vals):
            tk.Radiobutton(frame_for_options, text=self.question_set.loc[col], variable=self.selected_value, value=rbv, bg=container.bg_colour, font=("Arial", 20), wraplength=1000).grid(row=i, column=0, sticky='w')

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

            

class SolAreaQuiz(tk.Toplevel):
    def __init__(self, parent, sol_area, *colours):
        super().__init__(parent)

        self.geometry("800x800")
        self.title(f'{sol_area} Knowledge Quiz')
        self.bg_colour, self.bold_font_colour = colours
        self.config(bg=self.bg_colour)
        self.parent = parent
        self.sol_area = sol_area

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        sol_area_map = {"AI/Apps": "apps", "Data": "data", "Infrastructure": "infra"}
        self.questions = self.load_csv(sol_area_map[sol_area], "questions")
        self.answers = self.load_csv(sol_area_map[sol_area], "answers")
        self.resources = self.load_csv(sol_area_map[sol_area], "resources")
        self.question_frames = []

        self.load_questions()

        self.current_question_indx = 0


        frame_for_labels = tk.Frame(self)
        frame_for_labels.grid(row=0, column=0)

        tk.Label(frame_for_labels, text=f"{sol_area}", bg=self.bg_colour, fg=self.bold_font_colour, font=("Arial", 20, 'bold')).pack(side=tk.LEFT)
        tk.Label(frame_for_labels, text="Knowledge Quiz", bg=self.bg_colour, font=("Arial", 20)).pack(side=tk.LEFT)

        self.display_current_question_frame()
        #self.question_frames[0].display_frame(self)
        #self.display_questions()

    def load_questions(self):
        #print(questions.iloc[0])

        size = len(self.questions)
        for i in range(size):
            if i == 0:
                first, last = True, False
            elif i == size - 1:
                first, last = False, True
            else:
                first, last = False, False
            qf = QuestionFrame(self, self.questions.iloc[i], first, last)
            self.question_frames.append(qf)
            qf.grid(row=1, column=0, sticky='nswe')


    def load_csv(self, choice, csv_type):
        with open(f"question_bank/{choice}_{csv_type}.csv", "r") as file:
            return pd.read_csv(file)

    def display_current_question_frame(self):
        self.question_frames[self.current_question_indx].tkraise()

    def change_question_frame(self, direction):
        self.current_question_indx += direction
        self.display_current_question_frame()

    def submit(self):
        result = messagebox.askyesnocancel(f"Submit", f"Are you sure you want to submit?")
        if result:
            # self.parent.questions = self.question_frames
            # self.parent.answers = self.answers
            # self.parent.resources = self.resources
            self.destroy()
            self.parent.open_results_window(self.question_frames, self.answers, self.resources, self.sol_area, self.bg_colour, self.bold_font_colour)
            #self.destroy()


    # def display_questions(self, question_set=""):
    #     question_frame = QuestionFrame(self, question_set)




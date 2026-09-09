import tkinter as tk

class Frame(tk.Frame):
    def __init__(self, container, question_set,  is_correct, answer_set="", resource_set="", is_first = True, is_last=False):
        super().__init__(container)

        self.is_first = is_first
        self.is_last = is_last
        self.question_set = question_set
        self.configure(bg=container.bg_colour)

        frame_for_question = tk.Frame(self, bg=container.bg_colour)
        frame_for_question.pack(pady=10)

        tk.Label(frame_for_question, text=f"Question {question id}: ", bg=container.bg_colour, font=("Arial", 20, 'bold')).pack(fill='x')
        tk.Label(frame_for_question, text=question text, bg=container.bg_colour, font=("Arial", 20), wraplength=600).pack()

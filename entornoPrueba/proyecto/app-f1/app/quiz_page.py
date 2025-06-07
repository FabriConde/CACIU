import customtkinter as ctk
import json
import random
from app.session_manager import SessionManager

class QuizPage(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username  # <-- Guarda el usuario actual
        self.score = 0
        self.index = 0
        self.load_questions()
        self.show_question()

    def load_questions(self):
        with open("data/quiz_data.json", "r") as f:
            self.questions = json.load(f)
        random.shuffle(self.questions)

    def show_question(self):
        if self.index < len(self.questions):
            self.clear_frame()
            q = self.questions[self.index]
            self.label = ctk.CTkLabel(self, text=q["question"])
            self.label.pack(pady=20)
            self.true_btn = ctk.CTkButton(self, text="Verdadero", command=lambda: self.check_answer(True))
            self.false_btn = ctk.CTkButton(self, text="Falso", command=lambda: self.check_answer(False))
            self.true_btn.pack(pady=10)
            self.false_btn.pack(pady=10)
        else:
            self.clear_frame()
            SessionManager.guardar_resultado_quiz(self.username, self.score, len(self.questions))
            from app.main_page import MainPage
            ctk.CTkLabel(self, text=f"Quiz terminado. Puntuación: {self.score}/{len(self.questions)}").pack(pady=20)
            ctk.CTkButton(self,text="Volver al inicio",command=lambda: self.master.switch_frame(MainPage, self.username)).pack()

    def check_answer(self, answer):
        if answer == self.questions[self.index]["answer"]:
            self.score += 1
        self.index += 1
        self.show_question()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
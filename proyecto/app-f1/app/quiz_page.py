import customtkinter as ctk
import json
import random
from app.session_manager import SessionManager
from app.base_page import BasePage
from .generate_questions import generate_questions

class QuizPage(BasePage):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username
        self.score = 0
        self.index = 0
        self.load_questions()
        self.show_question()

    def load_questions(self):
        with open("data/quiz_data.json", "r", encoding="utf-8") as f:
            all_questions = json.load(f)
        users = SessionManager.load_users()
        user_data = users.get(self.username, {})
        nivel = user_data.get("nivel")
        equipo = user_data.get("equipo_favorito")
        piloto = user_data.get("piloto_favorito")

        self.questions = generate_questions(all_questions, nivel, piloto, equipo)
    
        
    def show_question(self):
        self.clear_content()
        total = len(self.questions)
        if self.index < total:
            q = self.questions[self.index]
            ctk.CTkLabel(self.content, text=f"Pregunta {self.index + 1} de {total}", font=("Arial", 14, "bold")).pack(pady=(10, 5))
            self.label = ctk.CTkLabel(self.content, text=q["question"], font=("Arial", 14))
            self.label.pack(pady=20)
            self.true_btn = ctk.CTkButton(self.content, text="Verdadero", command=lambda: self.check_answer(True))
            self.false_btn = ctk.CTkButton(self.content, text="Falso", command=lambda: self.check_answer(False))
            self.true_btn.pack(pady=10)
            self.false_btn.pack(pady=10)
        else:
            SessionManager.guardar_resultado_quiz(self.username, self.score, total)
            from app.main_page import MainPage
            ctk.CTkLabel(self.content, text=f"Quiz terminado. Puntuación: {self.score}/{total}").pack(pady=20)
            ctk.CTkButton(self.content, text="Volver al inicio", fg_color="#e64467", hover_color="#aa324c", command=lambda: self.master.switch_frame(MainPage, self.username)).pack()

    def check_answer(self, answer):
        if answer == self.questions[self.index]["answer"]:
            self.score += 1
        self.index += 1
        self.show_question()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
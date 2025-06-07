import customtkinter as ctk
import json
import random
from app.session_manager import SessionManager
from app.base_page import BasePage

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
        with open("data/quiz_data.json", "r") as f:
            all_questions = json.load(f)
        users = SessionManager.load_users()
        user_data = users.get(self.username, {})
        nivel = user_data.get("nivel")
        equipo = user_data.get("equipo_favorito")
        piloto = user_data.get("piloto_favorito")

        filtered = [
            q for q in all_questions
            if (q.get("nivel") == nivel or
                q.get("equipo") == equipo or
                q.get("piloto") == piloto)
        ]
        random.shuffle(filtered)
        num_preguntas = min(10, len(filtered))
        self.questions = filtered[:num_preguntas]
        if len(self.questions) < 10:
            restantes = [q for q in all_questions if q not in self.questions]
            random.shuffle(restantes)
            self.questions += restantes[:10 - len(self.questions)]
        random.shuffle(self.questions)

    def show_question(self):
        self.clear_content()
        if self.index < len(self.questions):
            q = self.questions[self.index]
            self.label = ctk.CTkLabel(self.content, text=q["question"])
            self.label.pack(pady=20)
            self.true_btn = ctk.CTkButton(self.content, text="Verdadero", command=lambda: self.check_answer(True))
            self.false_btn = ctk.CTkButton(self.content, text="Falso", command=lambda: self.check_answer(False))
            self.true_btn.pack(pady=10)
            self.false_btn.pack(pady=10)
        else:
            SessionManager.guardar_resultado_quiz(self.username, self.score, len(self.questions))
            from app.main_page import MainPage
            ctk.CTkLabel(self.content, text=f"Quiz terminado. Puntuación: {self.score}/{len(self.questions)}").pack(pady=20)
            ctk.CTkButton(self.content, text="Volver al inicio", command=lambda: self.master.switch_frame(MainPage, self.username)).pack()

    def check_answer(self, answer):
        if answer == self.questions[self.index]["answer"]:
            self.score += 1
        self.index += 1
        self.show_question()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
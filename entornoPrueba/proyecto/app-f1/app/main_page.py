import customtkinter as ctk
from app.base_page import BasePage

class MainPage(BasePage):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username

        ctk.CTkLabel(self.content, text="Bienvenido a F1 AR", font=("Arial", 24)).pack(pady=20)
        ctk.CTkButton(self.content, text="Realidad Aumentada", command=self.launch_ar).pack(pady=10)
        ctk.CTkButton(self.content, text="Quiz F1", command=self.open_quiz).pack(pady=10)
        ctk.CTkButton(self.content, text="Puntuación Quiz", command=self.open_scoreQuiz).pack(pady=10)

    def launch_ar(self):
        print("Aquí irá la lógica de RA con OpenCV")

    def open_quiz(self):
        from app.quiz_page import QuizPage
        self.master.switch_frame(QuizPage, self.username)

    def open_scoreQuiz(self):
        from app.score_quiz_page import ScoreQuizPage
        self.master.switch_frame(ScoreQuizPage, self.username)
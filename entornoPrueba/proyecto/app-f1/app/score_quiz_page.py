import customtkinter as ctk
from app.session_manager import SessionManager
from app.main_page import MainPage
from app.base_page import BasePage

class ScoreQuizPage(BasePage):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username
        self.show_history()

    def show_history(self):
        self.clear_content()
        users = SessionManager.load_users()
        historial = users.get(self.username, {}).get("historial_quiz", [])
        total_intentos = len(historial)

        ctk.CTkLabel(self.content, text="Resumen de Quizzes").pack(pady=10)
        if historial:
            # Calcular media sobre 10
            media = sum((item["puntos"] / item["total"]) * 10 for item in historial) / total_intentos
            media_redondeada = round(media, 2)
            ctk.CTkLabel(
                self.content,
                text=f"Media de puntuación: {media_redondeada} / 10"
            ).pack(pady=10)

            # Mostrar estrellas (de 1 a 5)
            estrellas = int(round(media / 2))  # 10/2 = 5 estrellas
            estrellas_str = "★" * estrellas + "☆" * (5 - estrellas)
            ctk.CTkLabel(
                self.content,
                text=f"Valoración: {estrellas_str}"
            ).pack(pady=10)
        else:
            ctk.CTkLabel(self.content, text="No hay historial de quizzes.").pack(pady=10)

        ctk.CTkButton(self.content, text="Historial Quiz", command=self.open_historyQuiz).pack(pady=10)
        ctk.CTkButton(
            self.content,
            text="Volver al inicio",
            command=lambda: self.master.switch_frame(MainPage, self.username)
        ).pack(pady=10)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def open_historyQuiz(self):
        from app.history_quiz_page import HistoryQuizPage
        self.master.switch_frame(HistoryQuizPage, self.username)
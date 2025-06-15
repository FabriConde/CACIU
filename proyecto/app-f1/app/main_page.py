import customtkinter as ctk
from app.base_page import BasePage
import subprocess
import sys
from app.session_manager import SessionManager

class MainPage(BasePage):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username

        ctk.CTkLabel(
            self.content,
            text=f"Bienvenido a F1 AR, {self.username}",
            font=("Arial", 24)
        ).pack(pady=20)
        ctk.CTkButton(self.content, text="Realidad Aumentada", command=self.launch_ar).pack(pady=10)
        ctk.CTkButton(self.content, text="Quiz F1", command=self.open_quiz).pack(pady=10)
        ctk.CTkButton(self.content, text="Puntuación Quiz", command=self.open_scoreQuiz).pack(pady=10)
        # Botón para registrar reconocimiento facial
        ctk.CTkButton(
            self.content,
            text="Registrar Reconocimiento Facial",
            command=self.register_face
        ).pack(pady=10)

        ctk.CTkButton(
            self.content,
            text="Cerrar sesión",
            fg_color="red",
            hover_color="#a30000",
            command=self.logout
        ).pack(pady=20)

    def launch_ar(self):
        print("Aquí irá la lógica de RA con OpenCV")
        subprocess.Popen([sys.executable, "app/cars.py"])

    def open_quiz(self):
        from app.quiz_page import QuizPage
        self.master.switch_frame(QuizPage, self.username)

    def open_scoreQuiz(self):
        from app.score_quiz_page import ScoreQuizPage
        self.master.switch_frame(ScoreQuizPage, self.username)

    def register_face(self):
        # Recupera el ID numérico del usuario
        users = SessionManager.load_users()
        user_data = users.get(self.username)
        if user_data and "id" in user_data:
            user_id = user_data["id"]
            # Captura imágenes
            subprocess.run([sys.executable, "app/face-recognition/capture-images.py", str(user_id)])
            # Entrena el modelo automáticamente después de capturar
            subprocess.run([sys.executable, "app/face-recognition/train-model.py"])
        else:
            print("No se encontró el ID del usuario.")

    def logout(self):
        from app.login_page import LoginPage
        SessionManager.clear_session()
        self.master.switch_frame(LoginPage)

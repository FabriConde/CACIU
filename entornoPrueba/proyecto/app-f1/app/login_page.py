import customtkinter as ctk
from app.main_page import MainPage
from app.session_manager import SessionManager
from app.register_page import RegisterPage
from app.recognition_login_page import RecognitionLoginPage

class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.login_btn = ctk.CTkButton(self, text="Iniciar sesión", command=self.login)
        self.register_btn = ctk.CTkButton(self, text="Registrarse", command=self.go_to_register)
        self.recognition_btn = ctk.CTkButton(self, text="Reconocimiento facial", command=self.go_to_recognition)
        self.message_label = ctk.CTkLabel(self, text="", text_color="red")

        self.username_entry.pack(pady=10)
        self.password_entry.pack(pady=10)
        self.login_btn.pack(pady=10)
        self.register_btn.pack(pady=5)
        self.recognition_btn.pack(pady=5)
        self.message_label.pack(pady=5)

    def login(self):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()
        if not user or not pwd:
            self.message_label.configure(text="Por favor, completa usuario y contraseña.", text_color="red")
            return
        if SessionManager.login(user, pwd):
            self.message_label.configure(text="Inicio de sesión exitoso.", text_color="green")
            SessionManager.save_session(user)  # Guardar sesión
            self.master.switch_frame(MainPage, user)
        else:
            self.message_label.configure(text="Usuario o contraseña incorrectos.", text_color="red")


    def go_to_register(self):
        self.master.switch_frame(RegisterPage)

    def go_to_recognition(self):
        self.master.switch_frame(RecognitionLoginPage)
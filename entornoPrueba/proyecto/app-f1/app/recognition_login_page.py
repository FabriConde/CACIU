import customtkinter as ctk
from app.base_page import BasePage

class RecognitionLoginPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        ctk.CTkLabel(self.content, text="Login con reconocimiento (en desarrollo)", font=("Arial", 18)).pack(pady=20)
        ctk.CTkButton(self.content, text="Volver", command=self.go_back).pack(pady=10)

    def go_back(self):
        from app.login_page import LoginPage
        self.master.switch_frame(LoginPage)
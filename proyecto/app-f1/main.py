import customtkinter as ctk
from app.login_page import LoginPage
from app.session_manager import SessionManager
from app.main_page import MainPage
import tkinter as tk
import cv2
import sys

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("F1 REALIDAD AUMENTADA")
        self.geometry("800x400")
        self.resizable(False, False)
        self.configure(fg_color="white")
        self._frame = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        usuario_guardado = SessionManager.load_session()
        if usuario_guardado:
            self.switch_frame(MainPage, usuario_guardado)
        else:
            self.switch_frame(LoginPage)

    def switch_frame(self, frame_class, *args, **kwargs):
        new_frame = frame_class(self, *args, **kwargs)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

    def on_closing(self):
        try:
            cv2.destroyAllWindows()
        except:
            pass
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.mainloop()
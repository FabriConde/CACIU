import customtkinter as ctk
from app.login_page import LoginPage
from app.session_manager import SessionManager
from app.main_page import MainPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("F1 REALIDAD AUMENTADA")
        self.geometry("600x400")
        self.resizable(False, False)
        self._frame = None

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

if __name__ == "__main__":
    app = App()
    app.mainloop()
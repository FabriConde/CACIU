import customtkinter as ctk
from app.session_manager import SessionManager
from app.main_page import MainPage

class HistoryQuizPage(ctk.CTkFrame):
    ITEMS_PER_PAGE = 5

    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username
        self.current_page = 0
        self.show_history()

    def show_history(self):
        self.clear_frame()
        users = SessionManager.load_users()
        historial = users.get(self.username, {}).get("historial_quiz", [])
        historial = sorted(historial, key=lambda x: x.get("fecha", ""), reverse=True)
        total = len(historial)

        ctk.CTkLabel(self, text="Historial completo de Quizzes").pack(pady=10)

        if total == 0:
            ctk.CTkLabel(self, text="No hay historial de quizzes.").pack(pady=10)
        else:
            start = self.current_page * self.ITEMS_PER_PAGE
            end = start + self.ITEMS_PER_PAGE
            for idx, intento in enumerate(historial[start:end], start + 1):
                ctk.CTkLabel(
                    self,
                    text=f"{intento['fecha']} | Intento {idx}: {intento['puntos']} / {intento['total']}"
                ).pack()

            if total > self.ITEMS_PER_PAGE:
                nav_frame = ctk.CTkFrame(self)
                nav_frame.pack(pady=10)
                if self.current_page > 0:
                    ctk.CTkButton(nav_frame, text="Anterior", command=self.prev_page).pack(side="left", padx=5)
                if end < total:
                    ctk.CTkButton(nav_frame, text="Siguiente", command=self.next_page).pack(side="left", padx=5)


        ctk.CTkButton(
            self,
            text="Volver al inicio",
            command=lambda: self.master.switch_frame(MainPage, self.username)
        ).pack(pady=10)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_history()

    def next_page(self):
        self.current_page += 1
        self.show_history()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
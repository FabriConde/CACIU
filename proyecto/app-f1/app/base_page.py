import customtkinter as ctk

class BasePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Configura el grid para centrar el contenido
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        # Frame de contenido centrado y transparente
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew")
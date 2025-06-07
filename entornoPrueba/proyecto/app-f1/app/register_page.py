import customtkinter as ctk
from app.session_manager import SessionManager

class RegisterPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.age_entry = ctk.CTkEntry(self, placeholder_text="Edad")
        self.level_option = ctk.CTkOptionMenu(self, values=["Principiante", "Intermedio", "Avanzado", "Experto"])
        self.level_option.set("Principiante")
        self.team_option = ctk.CTkOptionMenu(
            self,
            values=[
                "Red Bull", "Mercedes", "Aston Martin", "Ferrari", "Alpine", "McLaren",
                "Alfa Romeo", "AlphaTauri", "Williams", "Haas", "Renault", "Sauber",
                "Force India", "Racing Point", "Toyota (WEC)", "Minardi", "Audi"
            ]
        )
        self.team_option.set("Red Bull")
        self.driver_option = ctk.CTkOptionMenu(
            self,
            values=[
                "Max Verstappen", "Lewis Hamilton", "Nico Rosberg", "Sebastian Vettel",
                "Charles Leclerc", "Fernando Alonso", "George Russell", "Daniel Ricciardo",
                "Kimi Räikkönen", "Pierre Gasly", "Carlos Sainz", "Valtteri Bottas",
                "Lando Norris", "Alexander Albon", "Romain Grosjean", "Logan Sargeant",
                "Oscar Piastri", "Mick Schumacher", "Jenson Button", "Yuki Tsunoda",
                "Esteban Ocon", "Nico Hülkenberg", "Lance Stroll"
            ]
        )
        self.driver_option.set("Max Verstappen")

        self.register_btn = ctk.CTkButton(self, text="Registrar", command=self.register)
        self.back_btn = ctk.CTkButton(self, text="Volver", command=self.go_back)
        self.message_label = ctk.CTkLabel(self, text="", text_color="red")

        self.username_entry.pack(pady=5)
        self.password_entry.pack(pady=5)
        self.age_entry.pack(pady=5)
        self.level_option.pack(pady=5)
        self.team_option.pack(pady=5)
        self.driver_option.pack(pady=5)
        self.register_btn.pack(pady=10)
        self.back_btn.pack(pady=5)
        self.message_label.pack(pady=5)

    def register(self):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()
        age = self.age_entry.get().strip()
        level = self.level_option.get()
        team = self.team_option.get()
        driver = self.driver_option.get()

        if not user or not pwd or not age or not team or not driver:
            self.message_label.configure(text="Por favor, completa todos los campos.", text_color="red")
            return
        if not age.isdigit() or int(age) < 10 or int(age) > 120:
            self.message_label.configure(text="Edad inválida.", text_color="red")
            return
        if SessionManager.user_exists(user):
            self.message_label.configure(text="El usuario ya existe.", text_color="red")
            return
        SessionManager.register(
            user, pwd,
            edad=int(age),
            nivel=level,
            equipo_favorito=team,
            piloto_favorito=driver
        )
        self.message_label.configure(text="Usuario registrado correctamente.", text_color="green")

    def go_back(self):
        from app.login_page import LoginPage
        self.master.switch_frame(LoginPage)
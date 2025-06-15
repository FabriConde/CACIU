import customtkinter as ctk
from app.session_manager import SessionManager
from app.base_page import BasePage

class RegisterPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Título
        self.title_label = ctk.CTkLabel(self.content, text="Registro de Usuario", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=(10, 10))

        # Usuario
        self.username_entry = ctk.CTkEntry(self.content, placeholder_text="Usuario", width=180)
        self.username_entry.pack(pady=5)

        # Contraseña
        self.password_entry = ctk.CTkEntry(self.content, placeholder_text="Contraseña", show="*", width=180)
        self.password_entry.pack(pady=5)

        # Edad
        self.age_entry = ctk.CTkEntry(self.content, placeholder_text="Edad", width=180)
        self.age_entry.pack(pady=5)
        vcmd = (self.content.register(self.validate_number), "%P")
        self.age_entry.configure(validate="key", validatecommand=vcmd)

        # Nivel
        self.level_option = ctk.CTkOptionMenu(self.content, values=["Principiante", "Intermedio", "Avanzado", "Experto"], width=180)
        self.level_option.set("Principiante")
        self.level_option.pack(pady=5)

        # Equipo favorito
        self.team_option = ctk.CTkOptionMenu(
            self.content,
            values=[
                "Red Bull", "Mercedes", "Aston Martin", "Ferrari", "Alpine", "McLaren",
                "Alfa Romeo", "AlphaTauri", "Williams", "Haas", "Renault", "Sauber",
                "Force India", "Racing Point", "Toyota (WEC)", "Minardi", "Audi"
            ],
            width=180
        )
        self.team_option.set("Red Bull")
        self.team_option.pack(pady=5)

        # Piloto favorito
        self.driver_option = ctk.CTkOptionMenu(
            self.content,
            values=[
                "Max Verstappen", "Lewis Hamilton", "Nico Rosberg", "Sebastian Vettel",
                "Charles Leclerc", "Fernando Alonso", "George Russell", "Daniel Ricciardo",
                "Kimi Räikkönen", "Pierre Gasly", "Carlos Sainz", "Valtteri Bottas",
                "Lando Norris", "Alexander Albon", "Romain Grosjean", "Logan Sargeant",
                "Oscar Piastri", "Mick Schumacher", "Jenson Button", "Yuki Tsunoda",
                "Esteban Ocon", "Nico Hülkenberg", "Lance Stroll"
            ],
            width=180
        )
        self.driver_option.set("Max Verstappen")
        self.driver_option.pack(pady=5)

        # Botones
        self.register_btn = ctk.CTkButton(self.content, text="Registrar", command=self.register, width=180, fg_color="#1abc9c", hover_color="#16a085")
        self.register_btn.pack(pady=(10, 5))
        self.back_btn = ctk.CTkButton(self.content, text="Volver", command=self.go_back, width=180, fg_color="#e64467", hover_color="#aa324c")
        self.back_btn.pack(pady=5)

        # Mensaje
        self.message_label = ctk.CTkLabel(self.content, text="", text_color="red")
        self.message_label.pack(pady=(8, 0))

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
        from app.login_page import LoginPage
        self.master.switch_frame(LoginPage)

    def go_back(self):
        from app.login_page import LoginPage
        self.master.switch_frame(LoginPage)

    def validate_number(self, value):
        return value.isdigit() or value == ""
class HomePage:
    def __init__(self):
        self.title = "Página Principal"
        self.buttons = {
            "login": "Iniciar Sesión",
            "register": "Registrarse"
        }

    def show(self):
        print(f"{self.title}")
        for key, value in self.buttons.items():
            print(f"[{key}] {value}")

    def handle_button_click(self, button_key):
        if button_key in self.buttons:
            print(f"Botón '{self.buttons[button_key]}' presionado.")
        else:
            print("Botón no reconocido.")
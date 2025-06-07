class Auth:
    def __init__(self, database):
        self.database = database

    def register(self, username, password):
        if self.database.get_user(username):
            return False  # El usuario ya existe
        self.database.save_user(username, password)
        return True  # Registro exitoso

    def login(self, username, password):
        user = self.database.get_user(username)
        if user and user['password'] == password:
            return True  # Inicio de sesión exitoso
        return False  # Credenciales incorrectas
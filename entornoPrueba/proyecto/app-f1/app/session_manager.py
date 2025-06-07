import json
import os
import hashlib
import secrets
import datetime

class SessionManager:
    path = "data/users.json"
    SESSION_PATH = "data/session.json"

    @classmethod
    def load_users(cls):
        if not os.path.exists(cls.path):
            return {}
        with open(cls.path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    @classmethod
    def save_users(cls, users):
        with open(cls.path, "w") as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def hash_password(password, salt):
        return hashlib.sha256((salt + password).encode()).hexdigest()

    @classmethod
    def user_exists(cls, username):
        users = cls.load_users()
        return username in users

    @classmethod
    def login(cls, username, password):
        users = cls.load_users()
        if username not in users:
            return False
        salt = users[username]["salt"]
        hashed = cls.hash_password(password, salt)
        return users[username]["password"] == hashed

    @classmethod
    def register(cls, username, password, edad, nivel, equipo_favorito, piloto_favorito):
        users = cls.load_users()
        salt = secrets.token_hex(16)
        hashed = cls.hash_password(password, salt)
        users[username] = {
            "password": hashed,
            "salt": salt,
            "edad": edad,
            "nivel": nivel,
            "equipo_favorito": equipo_favorito,
            "piloto_favorito": piloto_favorito
        }
        cls.save_users(users)
    
    @classmethod
    def guardar_resultado_quiz(cls, username, puntos, total):
        users = cls.load_users()
        if username in users:
            users[username].setdefault("historial_quiz", [])
            users[username]["historial_quiz"].append({
                "puntos": puntos,
                "total": total,
                "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            cls.save_users(users)

    @classmethod
    def save_session(cls, username):
        session_data = {
            "username": username,
            "timestamp": datetime.datetime.now().timestamp()
        }
        with open(cls.SESSION_PATH, "w") as f:
            json.dump(session_data, f)

    @classmethod
    def load_session(cls):
        if not os.path.exists(cls.SESSION_PATH):
            return None
        with open(cls.SESSION_PATH, "r") as f:
            try:
                session_data = json.load(f)
            except json.JSONDecodeError:
                return None
        timestamp = session_data.get("timestamp", 0)
        now = datetime.datetime.now().timestamp()
        # 5 minutos = 300 segundos
        if now - timestamp <= 300:
            return session_data.get("username")
        return None

    @classmethod
    def clear_session(cls):
        if os.path.exists(cls.SESSION_PATH):
            os.remove(cls.SESSION_PATH)
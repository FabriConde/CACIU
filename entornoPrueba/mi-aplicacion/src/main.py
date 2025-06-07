from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QInputDialog, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from database import save_user, get_user
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CACIU - Plataforma de Usuarios")
        self.setWindowIcon(QIcon("icon.png"))  # Asegúrate de tener un icono en tu proyecto
        self.setFixedSize(400, 280)
        self.setStyleSheet("""
            QWidget {
                background-color: #e1f5fe;
            }
            QPushButton {
                border-radius: 8px;
                padding: 8px 0;
            }
            QPushButton#registro {
                background-color: #4fc3f7;
                color: white;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton#login {
                background-color: #0288d1;
                color: white;
                font-size: 15px;
                font-weight: bold;
            }
            QLabel#titulo {
                font-size: 26px;
                font-weight: bold;
                color: #0277bd;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(25)

        titulo = QLabel("Bienvenido a CACIU")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(30)

        btn_registro = QPushButton("Registrar")
        btn_registro.setObjectName("registro")
        btn_registro.setCursor(Qt.PointingHandCursor)
        btn_registro.clicked.connect(self.registrar)
        botones_layout.addWidget(btn_registro)

        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setObjectName("login")
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.clicked.connect(self.iniciar_sesion)
        botones_layout.addWidget(btn_login)

        layout.addLayout(botones_layout)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def registrar(self):
        username, ok1 = QInputDialog.getText(self, "Registro de Usuario", "Ingrese un nombre de usuario:")
        password, ok2 = QInputDialog.getText(self, "Registro de Usuario", "Ingrese una contraseña:", echo=QInputDialog.Password)
        if ok1 and ok2 and username and password:
            if get_user(username):
                QMessageBox.critical(self, "Error de Registro", "El usuario ya existe. Intente con otro nombre.")
            else:
                save_user(username, password)
                QMessageBox.information(self, "Registro Exitoso", "Usuario registrado correctamente.")
        elif ok1 or ok2:
            QMessageBox.warning(self, "Registro Cancelado", "Debe completar ambos campos para registrarse.")

    def iniciar_sesion(self):
        username, ok1 = QInputDialog.getText(self, "Inicio de Sesión", "Usuario:")
        password, ok2 = QInputDialog.getText(self, "Inicio de Sesión", "Contraseña:", echo=QInputDialog.Password)
        user = get_user(username)
        if ok1 and ok2 and user and user.password == password:
            QMessageBox.information(self, "Bienvenido", f"¡Hola, {username}!\nHas iniciado sesión correctamente.")
        elif ok1 and ok2:
            QMessageBox.critical(self, "Error de Inicio de Sesión", "Usuario o contraseña incorrectos.")
        # Si el usuario cancela, no se muestra ningún mensaje

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
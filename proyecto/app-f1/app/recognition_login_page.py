import os
import customtkinter as ctk
import cv2
import threading
from app.session_manager import SessionManager
from app.main_page import MainPage
from app.base_page import BasePage
import time

class RecognitionLoginPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.camera_active = False

        self.start_button = ctk.CTkButton(self.content, text="Iniciar Reconocimiento", command=self.start_recognition)
        self.start_button.pack(pady=10)

        self.message_label = ctk.CTkLabel(self.content, text="")
        self.message_label.pack(pady=10)

        from app.login_page import LoginPage
        self.back_button = ctk.CTkButton(self.content, text="Volver", command=lambda: master.switch_frame(LoginPage))
        self.back_button.pack(pady=10)

    def start_recognition(self):
        if not self.camera_active:
            self.camera_active = True
            threading.Thread(target=self.recognize_face, daemon=True).start()

    def recognize_face(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        trainer_path = os.path.join(os.path.dirname(__file__), "face-recognition", "trainer", "trainer.yml")
        if not os.path.exists(trainer_path):
            self.message_label.configure(text="No se encontró el modelo entrenado. Entrena primero.", text_color="red")
            return
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(trainer_path)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        names = SessionManager.get_usernames_by_id()
        cam = cv2.VideoCapture(0)

        found_user = None

        while self.camera_active:
            ret, img = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                if confidence < 70:
                    found_user = names[id]
                    break

            cv2.imshow("Reconocimiento Facial (Presiona Q para salir)", img)
            if cv2.waitKey(10) & 0xFF == ord('q') or found_user:
                break

        cam.release()
        cv2.destroyAllWindows()
        time.sleep(0.1)
        self.camera_active = False

        if found_user:
            SessionManager.save_session(found_user)
            self.master.after(0, lambda: self.master.switch_frame(MainPage, found_user))
            return 
        else:
            self.message_label.configure(text="No se reconoció ningún rostro.", text_color="red")

    def destroy(self):
        self.camera_active = False
        try:
            cv2.destroyAllWindows()
        except:
            pass
        super().destroy()

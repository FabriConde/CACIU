import numpy as np
from PIL import Image
import os

import cv2
print(hasattr(cv2, 'face'))
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []

    for image_path in image_paths:
        PIL_img = Image.open(image_path).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(image_path)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)
    return face_samples, ids

print("\n[INFO] Entrenando rostros. Esto puede tardar unos segundos ...")
faces, ids = get_images_and_labels(path)
recognizer.train(faces, np.array(ids))
trainer_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trainer")
os.makedirs(trainer_dir, exist_ok=True)
trainer_path = os.path.join(trainer_dir, "trainer.yml")
recognizer.write(trainer_path)
print("Imágenes encontradas:", len(faces))
print("IDs encontrados:", set(ids))
print(f"\n[INFO] {len(np.unique(ids))} rostro(s) entrenado(s).")

import cv2
import os
import sys

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

if len(sys.argv) > 1:
    face_id = sys.argv[1]
else:
    face_id = input('\nIngrese un ID numérico del usuario y presione ENTER ==> ')

dataset_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
os.makedirs(dataset_dir, exist_ok=True)

print("\n[INFO] Inicializando la captura de rostro. Mire a la cámara y espere ...")

count = 0

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        count += 1
        cv2.imwrite(os.path.join(dataset_dir, f"User.{face_id}.{count}.jpg"), gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.imshow('image', img)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    elif count >= 30:
        break

print("\n[INFO] Exiting capture ...")
cam.release()
cv2.destroyAllWindows()
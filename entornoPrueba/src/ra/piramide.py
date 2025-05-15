import cv2
import numpy as np
import cuia

#Declaramos la cámara que usaremos
cam = 0
#Seleccionamos el mejor backend
bk = cuia.bestBackend(cam);

#Definimos un objeto de la clase myVideo para acceder a la cámara seleccionada
ar = cuia.myVideo(cam, bk)

diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
detector = cv2.aruco.ArucoDetector(diccionario)

def origen(TAM):
    return(np.array([[-TAM/2.0, -TAM/2.0, 0.0],
                     [-TAM/2.0,  TAM/2.0, 0.0],
                     [ TAM/2.0,  TAM/2.0, 0.0],
                     [ TAM/2.0, -TAM/2.0, 0.0]]))

try:
    import camara
    cameraMatrix = camara.cameraMatrix
    distCoeffs = camara.distCoeffs
except ImportError:
    # Si la cámara no estaba calibrada suponemos que no presenta distorsiones
    webcam = cv2.VideoCapture(cam,bk)
    ancho = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    webcam.release()
    cameraMatrix = np.array([[ 1000,    0, ancho/2],
                             [    0, 1000,  alto/2],
                             [    0,    0,       1]])
    distCoeffs = np.zeros((5, 1)) 

def proyeccion(puntos, rvec, tvec, cameraMatrix, distCoeffs):
    if isinstance(puntos, list):
        return(proyeccion(np.array(puntos, dtype=np.float32), rvec, tvec, cameraMatrix, distCoeffs))
    if isinstance(puntos, np.ndarray):
        if puntos.ndim == 1 and puntos.size == 3:
            res, _ = cv2.projectPoints(puntos.astype(np.float32), rvec, tvec, cameraMatrix, distCoeffs)
            return(res[0][0].astype(int))
        if puntos.ndim > 1:
            aux = proyeccion(puntos[0], rvec, tvec, cameraMatrix, distCoeffs)
            aux = np.expand_dims(aux, axis=0)
            for p in puntos[1:]:
                aux = np.append(aux, [proyeccion(p, rvec, tvec, cameraMatrix, distCoeffs)], axis=0)
            return(np.array(aux))

def piramide(frame):
    T = 0.19 #Tamaño (en metros) del lado del marcador
    a = [[0,0,0.15],
         [-T/2,-T/2,0],
         [T/2,-T/2,0],
         [T/2,T/2,0],
         [-T/2,T/2,0]]
    color = (0, 255, 255) #Color amarillo
    grosor = 2
    bboxs, ids, _ = detector.detectMarkers(frame)
    if ids is not None:
        for i in range(len(ids)):
            ret, rvec, tvec = cv2.solvePnP(origen(T), bboxs[i], cameraMatrix, distCoeffs) 
            if ret:
                p = proyeccion(a, rvec, tvec, cameraMatrix, distCoeffs)
                frame = cv2.line(frame, p[1], p[2], color, grosor)
                frame = cv2.line(frame, p[2], p[3], color, grosor)
                frame = cv2.line(frame, p[3], p[4], color, grosor)
                frame = cv2.line(frame, p[4], p[1], color, grosor)
                frame = cv2.line(frame, p[1], p[0], color, grosor)
                frame = cv2.line(frame, p[2], p[0], color, grosor)
                frame = cv2.line(frame, p[3], p[0], color, grosor)
                frame = cv2.line(frame, p[4], p[0], color, grosor)
    return(frame)

ar.process = piramide
try:
    ar.play("Pirámide", key=ord(' '))
finally:
    ar.release()

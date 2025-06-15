import asyncio
import cuia
import cv2
import numpy as np
import speech_recognition as sr
import threading
from dataclasses import dataclass, field

modelos_ruta = [
    'media/alpine_team.glb',
    'media/ferrari_2019_team.glb',
    'media/mclaren_2021_team.glb',
    'media/mclaren_2022_team.glb',
    'media/formula_1.glb',
    'media/renault_2019_team.glb',
    'media/mercedes_team.glb',
    'media/mercedes_2023_team.glb',
]

def escalar_modelo_a_maximo(modelo, max_metros=0.3):
    bbox_min, bbox_max = modelo.model_obj.get_world_bounding_box()
    size = np.abs(np.array(bbox_max) - np.array(bbox_min))
    max_dim = np.max(size)
    escala = 1.0 if max_dim == 0 else max_metros / max_dim
    modelo.escalar(escala)

def cargar_modelo(ruta):
    modelo = cuia.modeloGLTF(ruta)
    modelo.rotar((np.pi/2.0, 0, 0))
    escalar_modelo_a_maximo(modelo)
    modelo.flotar()
    anims = modelo.animaciones()
    if anims:
        modelo.animar(anims[0])
    return modelo

def fromOpencvToPygfx(rvec, tvec):
    pose = np.eye(4)
    pose[0:3,3] = tvec.T
    pose[0:3,0:3] = cv2.Rodrigues(rvec)[0]
    pose[1:3] *= -1
    return np.linalg.inv(pose)

def calcular_fov(cameraMatrix, ancho, alto):
    if ancho > alto:
        f = cameraMatrix[1, 1]
        fov_rad = 2 * np.arctan(alto / (2 * f))
    else:
        f = cameraMatrix[0, 0]
        fov_rad = 2 * np.arctan(ancho / (2 * f))
    return np.rad2deg(fov_rad)

@dataclass
class Estado(cuia.Store):
    indice: int = 0
    modelo: any = None
    escena: any = None
    ancho: int = 640
    alto: int = 480
    cameraMatrix: any = None
    distCoeffs: any = None
    marcador_size: float = 0.19
    cam: int = 0
    bk: str = field(default_factory=str)

async def update(store, msg):
    if msg == "siguiente":
        store.indice = (store.indice + 1) % len(modelos_ruta)
        modelo = cargar_modelo(modelos_ruta[store.indice])
        store.escena.limpiar_modelos()
        store.escena.agregar_modelo(modelo)
        store.escena.ilumina_modelo(modelo)
        store.modelo = modelo

    elif msg == "anterior":
        store.indice = (store.indice - 1) % len(modelos_ruta)
        modelo = cargar_modelo(modelos_ruta[store.indice])
        store.escena.limpiar_modelos()
        store.escena.agregar_modelo(modelo)
        store.escena.ilumina_modelo(modelo)
        store.modelo = modelo

    elif msg.startswith("rotar"):
        if store.modelo:
            if "horizontal" in msg:
                store.modelo.rotar((0, np.pi/4, 0))
            elif "vertical" in msg:
                store.modelo.rotar((np.pi/4, 0, 0))

    elif msg.startswith("buscar:"):
        nombre = msg.split("buscar:")[1].strip()
        for i, ruta in enumerate(modelos_ruta):
            if nombre.lower() in ruta.lower():
                store.indice = i
                modelo = cargar_modelo(modelos_ruta[store.indice])
                store.escena.limpiar_modelos()
                store.escena.agregar_modelo(modelo)
                store.escena.ilumina_modelo(modelo)
                store.modelo = modelo
      
def view(store):
    def realidad_mixta(frame):
        ret, pose = detectar_pose(frame, store)
        if ret and pose:
            first_id = next(iter(pose))
            rvec, tvec = pose[first_id]
            M = fromOpencvToPygfx(rvec, tvec)
            store.escena.actualizar_camara(M)
            render = store.escena.render()
            render_bgr = cv2.cvtColor(render, cv2.COLOR_RGBA2BGRA)
            return cuia.alphaBlending(render_bgr, frame)
        return frame
    return realidad_mixta

def detectar_pose(frame, store):
    diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
    detector = cv2.aruco.ArucoDetector(diccionario)
    bboxs, ids, _ = detector.detectMarkers(frame)
    if ids is not None:
        objPoints = np.array([[-store.marcador_size/2, store.marcador_size/2, 0],
                              [store.marcador_size/2, store.marcador_size/2, 0],
                              [store.marcador_size/2, -store.marcador_size/2, 0],
                              [-store.marcador_size/2, -store.marcador_size/2, 0]])
        resultado = {}
        for i in range(len(ids)):
            ret, rvec, tvec = cv2.solvePnP(objPoints, bboxs[i], store.cameraMatrix, store.distCoeffs)
            if ret:
                resultado[ids[i][0]] = (rvec, tvec)
        return True, resultado
    return False, None

async def escuchar(store, cola):
    recog = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recog.adjust_for_ambient_noise(source)
    while True:
        with mic as source:
            print("🎙️ Escuchando...")
            try:
                audio = recog.listen(source, timeout=5)
                comando = recog.recognize_google(audio, language="es-ES").lower()
                if "siguiente" in comando:
                    await cola.put("siguiente")
                elif "anterior" in comando:
                    await cola.put("anterior")
                elif "rotar horizontal" in comando:
                    await cola.put("rotar horizontal")
                elif "rotar vertical" in comando:
                    await cola.put("rotar vertical")
                elif "buscar" in comando:
                    partes = comando.split("buscar")
                    if len(partes) > 1:
                        nombre = partes[1].strip()
                        await cola.put(f"buscar:{nombre}")
            except Exception as e:
                print("❗ Voz no reconocida:", e)
        await asyncio.sleep(0.5)


def main():
    cam = None
    for i in range(5):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            cam = i
            cap.release()
            break
    if cam is None:
        raise RuntimeError("No se encontró cámara.")
    
    bk = cuia.bestBackend(cam)
    cap = cv2.VideoCapture(cam, bk)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    try:
        import camara
        cameraMatrix = camara.cameraMatrix
        distCoeffs = camara.distCoeffs
    except:
        cameraMatrix = np.array([[1000, 0, ancho/2], [0, 1000, alto/2], [0, 0, 1]])
        distCoeffs = np.zeros((5, 1))

    modelo = cargar_modelo(modelos_ruta[0])
    escena = cuia.escenaPYGFX(calcular_fov(cameraMatrix, ancho, alto), ancho, alto)
    escena.agregar_modelo(modelo)
    escena.ilumina_modelo(modelo)
    escena.iluminar()

    estado = Estado(modelo=modelo, escena=escena, ancho=ancho, alto=alto,
                    cameraMatrix=cameraMatrix, distCoeffs=distCoeffs,
                    cam=cam, bk=bk)

    cola = asyncio.Queue()

    def voz_thread():
        asyncio.run(escuchar(estado, cola))

    t = threading.Thread(target=voz_thread, daemon=True)
    t.start()

    view_fn = view(estado)
    cap = cv2.VideoCapture(estado.cam, estado.bk)

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            cv2.waitKey(10)
            continue
        frame = view_fn(frame)
        cv2.imshow("Realidad Aumentada", frame)
        # Salir si se pulsa ESC o si se cierra la ventana
        if cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("Realidad Aumentada", cv2.WND_PROP_VISIBLE) < 1:
            break
        try:
            msg = cola.get_nowait()
            asyncio.run(update(estado, msg))
        except asyncio.QueueEmpty:
            pass

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

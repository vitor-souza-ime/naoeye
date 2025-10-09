import qi
import cv2
import numpy as np
import mediapipe as mp
from scipy.spatial import distance
import time

# Configuração da sessão com o NAO
NAO_IP = "172.15.4.178"   # altere para o IP do seu NAO
NAO_PORT = 9559

session = qi.Session()
try:
    session.connect(f"tcp://{NAO_IP}:{NAO_PORT}")
    print("Conectado ao NAO!")
except RuntimeError:
    print("Erro: não foi possível conectar ao NAO.")
    exit(1)

# Serviços do NAO
video_service = session.service("ALVideoDevice")
tts_service = session.service("ALTextToSpeech")  # Serviço de fala
motion_service = session.service("ALMotion")

# Inscrição na câmera do NAO (640x480, RGB)
subscriber_id = video_service.subscribeCamera(
    "camera_test", 0, 1, 11, 30
)

# Inicializar MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Pontos dos olhos no FaceMesh
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# EAR: Eye Aspect Ratio
def eye_aspect_ratio(eye_points):
    A = distance.euclidean(eye_points[1], eye_points[5])
    B = distance.euclidean(eye_points[2], eye_points[4])
    C = distance.euclidean(eye_points[0], eye_points[3])
    return (A + B) / (2.0 * C)

frame_count = 0

print("Pressione 'q' para sair.")

# Deixar o corpo todo mole
motion_service.setStiffnesses("Body", 0.0)

while True:
    nao_image = video_service.getImageRemote(subscriber_id)
    if nao_image is None:
        continue

    frame_count += 1

    width, height = nao_image[0], nao_image[1]
    array = nao_image[6]

    try:
        frame = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))
    except:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    i = time.time()
    results = face_mesh.process(frame_rgb)
    f = time.time() - i

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            
            left_eye = [
                (int(face_landmarks.landmark[i].x * w),
                 int(face_landmarks.landmark[i].y * h))
                for i in LEFT_EYE
            ]

            right_eye = [
                (int(face_landmarks.landmark[i].x * w),
                 int(face_landmarks.landmark[i].y * h))
                for i in RIGHT_EYE
            ]

            # Desenha pontos nos olhos
            for x, y in left_eye + right_eye:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Calcula EAR
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            ear_avg = (left_ear + right_ear) / 2.0

            status = "EYES OPEN" if ear_avg >= 0.2 else "EYES CLOSED"
            cor = (0, 255, 0) if status == "EYES OPEN" else (0, 0, 255)

            # NAO fala o status dos olhos (descomente se quiser)
            # tts_service.say(status)
            print(f"{status} (EAR: {ear_avg:.2f}) t={f:.3f}s")

            cv2.putText(
                frame,
                f"{status} (EAR: {ear_avg:.2f})",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                cor,
                2
            )
    else:
        cv2.putText(frame, "No face detected", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Eye Detection - NAO", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Salvar imagem manualmente com nome específico
        filename = f"nao_eye_capture_{int(time.time())}.png"
        cv2.imwrite(filename, frame)
        print(f"Imagem salva: {filename}")

# Finalizar
video_service.unsubscribe(subscriber_id)
cv2.destroyAllWindows()
face_mesh.close()
print("Finalizado!")

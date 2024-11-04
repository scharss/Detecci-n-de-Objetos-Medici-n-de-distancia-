import cv2
import numpy as np
import serial
import time

# Configuración de la comunicación serial con la ESP32
serial_port = 'COM6'  # Cambia esto al puerto que corresponde en tu sistema
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)

# Cargar los archivos de YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Diccionario para traducir las clases de inglés a español
classes_es = {
    "person": "persona",
    "bicycle": "bicicleta",
    "car": "coche",
    "motorbike": "motocicleta",
    "aeroplane": "avión",
    "bus": "autobús",
    "train": "tren",
    "truck": "camión",
    "boat": "barco",
    "traffic light": "semáforo",
    "fire hydrant": "hidrante",
    "stop sign": "señal de alto",
    "parking meter": "parquímetro",
    "bench": "banco",
    "bird": "pájaro",
    "cat": "gato",
    "dog": "perro",
    "horse": "caballo",
    "sheep": "oveja",
    "cow": "vaca",
    "elephant": "elefante",
    "bear": "oso",
    "zebra": "cebra",
    "giraffe": "jirafa",
    "backpack": "mochila",
    "umbrella": "paraguas",
    "handbag": "bolso",
    "tie": "corbata",
    "suitcase": "maleta",
    "frisbee": "frisbee",
    "skis": "esquís",
    "snowboard": "tabla de snowboard",
    "sports ball": "pelota",
    "kite": "cometa",
    "banana": "banano",
    "baseball bat": "bate de béisbol",
    "baseball glove": "guante de béisbol",
    "skateboard": "patineta",
    "surfboard": "tabla de surf",
    "tennis racket": "raqueta de tenis",
    "bottle": "botella",
    "wine glass": "copa de vino",
    "cup": "taza",
    "fork": "tenedor",
    "knife": "cuchillo",
    "spoon": "cuchara",
    "bowl": "cuenco",
    "banana": "banana",
    "apple": "manzana",
    "sandwich": "sándwich",
    "orange": "naranja",
    "broccoli": "brócoli",
    "carrot": "zanahoria",
    "hot dog": "perrito caliente",
    "pizza": "pizza",
    "donut": "dona",
    "cake": "pastel",
    "chair": "silla",
    "sofa": "sofá",
    "pottedplant": "planta en maceta",
    "bed": "cama",
    "diningtable": "mesa de comedor",
    "toilet": "inodoro",
    "tvmonitor": "televisor",
    "laptop": "computadora portátil",
    "mouse": "ratón",
    "remote": "control remoto",
    "keyboard": "teclado",
    "cell phone": "smartphone",
    "microwave": "microondas",
    "oven": "horno",
    "toaster": "tostadora",
    "sink": "fregadero",
    "refrigerator": "refrigerador",
    "book": "libro",
    "clock": "reloj",
    "vase": "florero",
    "scissors": "tijeras",
    "teddy bear": "oso de peluche",
    "hair drier": "secador de pelo",
    "toothbrush": "cepillo de dientes",
    "screwdriver": "destornillador",
    "photographic camera": "camara fotografica"
}

# Configuración de la red para usar la GPU si está disponible
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # Cambia a DNN_TARGET_CUDA si tienes una GPU compatible

# Obtener las capas de salida de YOLO
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Iniciar la captura de video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Enviar solicitud para obtener la distancia
    ser.write(b'd')  # Enviar 'd' para solicitar la distancia
    distance = ser.readline().decode().strip()  # Leer la distancia desde la ESP32

    # Preparar la imagen para la red YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    detections = net.forward(output_layers)

    # Bandera para controlar que solo se detecte un objeto a la vez
    object_detected = False

    # Procesar cada detección
    for out in detections:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Verificar si la clase detectada es distinta de "persona" y la confianza es alta
            if confidence > 0.5 and classes[class_id] != "person" and not object_detected:
                # Coordenadas del objeto detectado
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])

                # Calcular las esquinas del cuadro delimitador
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Traducir el nombre del objeto al español
                label_es = classes_es.get(classes[class_id], classes[class_id])
                label = f"{label_es} - Distancia: {distance} cm"

                # Dibujar el cuadro delimitador y la etiqueta
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Establecer la bandera para indicar que ya se ha detectado un objeto
                object_detected = True
                break  # Salir del bucle interno para no detectar más objetos en este cuadro
        if object_detected:
            break  # Salir del bucle externo si ya se ha detectado un objeto

    # Mostrar el video con la detección y distancia
    cv2.imshow("Detección de Objetos con YOLO", frame)

    # Presiona 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
ser.close()

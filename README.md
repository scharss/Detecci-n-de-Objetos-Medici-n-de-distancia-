Proyecto de Detección de Objetos con YOLO y ESP32-WROOM-32D
Este proyecto combina la detección de objetos en tiempo real utilizando YOLO (You Only Look Once) en Python y OpenCV, junto con la medición de distancia a través de un sensor HC-SR04 conectado a una ESP32-WROOM-32D. Los objetos detectados son mostrados en pantalla con su nombre en español y la distancia a la que se encuentran.

Requisitos
Hardware
ESP32-WROOM-32D
Sensor de distancia HC-SR04
Cables de conexión
Software
Python 3.x
Arduino IDE
Librerías de Python:
opencv-python
numpy
pyserial
Conexión del Hardware
Conectar el sensor HC-SR04 a la ESP32-WROOM-32D:

VCC del HC-SR04 al pin 3.3V de la ESP32.

GND del HC-SR04 al pin GND de la ESP32.

Trig del HC-SR04 al pin GPIO 5 de la ESP32.

Echo del HC-SR04 al pin GPIO 18 de la ESP32.

Nota: La ESP32-WROOM-32D trabaja a 3.3V, por lo que es importante verificar que el sensor HC-SR04 funcione a este voltaje. Si tu sensor requiere 5V, podrías necesitar un divisor de voltaje para proteger la ESP32.

Cargar el código en la ESP32: Utiliza el archivo .ino para subir el código en la ESP32 desde el Arduino IDE. Este código permite que la ESP32 mida la distancia usando el sensor HC-SR04 y envíe los datos a través de Serial.

Configuración de YOLO en Python
Descargar los archivos de YOLO: Asegúrate de tener los siguientes archivos:

yolov3.weights: Descargar aquí: https://pjreddie.com/media/files/yolov3.weights
yolov3.cfg: Descargar aquí: https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg
coco.names: Descargar aquí: https://github.com/pjreddie/darknet/blob/master/data/coco.names
Guarda estos archivos en la misma carpeta que el script de Python.

Instalar las librerías de Python: Ejecuta el siguiente comando para instalar las librerías necesarias:

bash
Copiar código
pip install opencv-python numpy pyserial
Ejecutar el script de detección: Ejecuta el script de Python (identifica.py) para realizar la detección de objetos y mostrar la distancia proporcionada por el sensor. Este script detecta objetos (excluyendo personas) y muestra el nombre en español y la distancia a la que se encuentran. Solo un objeto es detectado a la vez para mejorar la legibilidad.

Resultados
Este proyecto permite identificar y medir la distancia de objetos en tiempo real, combinando visión artificial con un sensor de distancia a través de la ESP32. Es ideal para aplicaciones de detección y monitoreo en entornos donde es importante conocer la proximidad de objetos específicos.


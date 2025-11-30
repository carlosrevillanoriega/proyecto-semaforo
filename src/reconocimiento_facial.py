import cv2
import os
import serial
import time

def configurar_camara():
    camara = cv2.VideoCapture(0)
    if not camara.isOpened():
        raise Exception("No se pudo abrir la cámara")
    camara.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return camara

def configurar_reconocimiento():
    reconocedor = cv2.face.LBPHFaceRecognizer_create()
    modelo_path = r"E:\Documentos\Arduino\Semaforo\ModeloFaceFRontalData2025.xml"
    
    if os.path.exists(modelo_path):
        reconocedor.read(modelo_path)
    else:
        raise Exception(f"Modelo de reconocimiento no encontrado en {modelo_path}")
    
    clasificador = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    return reconocedor, clasificador

def configurar_arduino():
    try:
        arduino = serial.Serial('COM4', 9600, timeout=1)
        time.sleep(2)
        return arduino
    except Exception as e:
        raise Exception(f"Error al conectar con Arduino: {str(e)}")

class EstadoSemaforo:
    AMARILLO_FIJO = "AMARILLO_FIJO"
    VERDE = "VERDE"
    ROJO = "ROJO"

def main():
    try:
        camara = configurar_camara()
        reconocedor, clasificador = configurar_reconocimiento()
        arduino = configurar_arduino()
        
        estado_actual = None
        ultimo_cambio = time.time()
        debounce_time = 2  # Tiempo mínimo entre cambios de estado (segundos)
        umbral_reconocimiento = 70  # Ajusta este valor según tus pruebas
        
        # Estado inicial
        arduino.write(b'AMARILLO_FIJO\n')
        estado_actual = EstadoSemaforo.AMARILLO_FIJO
        print("Sistema iniciado. Estado inicial: AMARILLO_FIJO")
        
        while True:
            ret, frame = camara.read()
            if not ret:
                print("Error al capturar frame")
                break
            
            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rostros = clasificador.detectMultiScale(gris, 1.3, 5)
            
            if len(rostros) > 0:
                for (x, y, w, h) in rostros:
                    rostro = gris[y:y+h, x:x+w]
                    rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                    
                    id, confianza = reconocedor.predict(rostro)
                    print(f"Confianza: {confianza:.1f}")  # Para debug
                    
                    # Solo cambiar estado si ha pasado el tiempo de debounce
                    if time.time() - ultimo_cambio > debounce_time:
                        # Lógica CORREGIDA (mayor confianza = menor certeza)
                        if confianza > umbral_reconocimiento:  # Desconocido
                            if estado_actual != EstadoSemaforo.ROJO:
                                arduino.write(b'ROJO\n')
                                estado_actual = EstadoSemaforo.ROJO
                                ultimo_cambio = time.time()
                                print(f"Desconocido (Conf: {confianza:.1f}) - ROJO")
                        else:  # Reconocido
                            if estado_actual != EstadoSemaforo.VERDE:
                                arduino.write(b'VERDE\n')
                                estado_actual = EstadoSemaforo.VERDE
                                ultimo_cambio = time.time()
                                print(f"Reconocido (Conf: {confianza:.1f}) - VERDE")
                    
                    # Dibujar en pantalla
                    color = (0, 255, 0) if confianza <= umbral_reconocimiento else (0, 0, 255)
                    texto = "Carlos" if confianza <= umbral_reconocimiento else "Desconocido"
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, f"{texto} ({confianza:.1f})", 
                               (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            else:  # No hay rostros
                if estado_actual != EstadoSemaforo.AMARILLO_FIJO and time.time() - ultimo_cambio > debounce_time:
                    arduino.write(b'AMARILLO_FIJO\n')
                    estado_actual = EstadoSemaforo.AMARILLO_FIJO
                    ultimo_cambio = time.time()
                    print("No hay rostros - AMARILLO_FIJO")
            
            cv2.imshow('Reconocimiento Facial - [ESC para salir]', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        camara.release()
        cv2.destroyAllWindows()
        if 'arduino' in locals():
            arduino.write(b'AMARILLO_FIJO\n')  # Volver a estado inicial
            arduino.close()
        print("Sistema terminado")

if __name__ == "__main__":
    main()
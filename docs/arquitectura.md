# Arquitectura del Sistema

## Visión General
El sistema conecta Python (procesamiento de visión artificial) con Arduino (control físico del semáforo).

## Componentes
- **Reconocimiento Facial (Python + OpenCV)**
- **Modelo LBPH**
- **Arduino UNO – control de LEDs**
- **Comunicación Serial**

## Flujo
1. La cámara capta el rostro
2. OpenCV detecta y normaliza el rostro
3. El modelo LBPH clasifica al usuario
4. Python envía un comando serial (ROJO/VERDE/AMARILLO)
5. Arduino ejecuta el estado del semáforo

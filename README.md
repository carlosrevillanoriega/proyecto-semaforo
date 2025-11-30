Proyecto Semáforo con Reconocimiento Facial

Sistema híbrido IA + Arduino que controla un semáforo físico basado en reconocimiento facial en tiempo real.
Implementa visión artificial (OpenCV + LBPH) para identificar personas autorizadas y responder con señales luminosas.

🚦 Estados del Semáforo
Estado	Significado	Acción
🟡 Amarillo	Sin rostros detectados	Modo espera
🟢 Verde	Usuario reconocido	Acceso permitido
🔴 Rojo	Usuario desconocido	Acceso denegado
🧠 Tecnologías utilizadas:

Python

OpenCV

LBPH Face Recognizer

Arduino UNO

Comunicación Serial

Haar Cascades

IP Webcam / USB Cam

📂 Estructura del proyecto
src/                 # Scripts Python (entrenamiento, captura, reconocimiento)
modelo/              # Modelo LBPH entrenado
arduino/             # Código Arduino del semáforo
docs/                # Documentación técnica

🚀 Instalación y ejecución rápida
pip install -r requirements.txt
python src/reconocimiento_facial.py

🧩 Funcionamiento general

Captura de rostros

Entrenamiento del modelo

Reconocimiento en tiempo real

Arduino recibe comandos seriales

Cambia el estado del semáforo físico

🎯 Objetivo profesional

Este proyecto forma parte de mi portafolio orientado a IA aplicada, visión por computadora e integración de hardware.

Demuestra:

Diseño de soluciones completas (end-to-end)

Conexión entre software de IA y sistemas físicos

Gestión de modelos, entrenamiento, puesta en producción

Programación en Python + Arduino

👨‍💻 Autor

Carlos Revilla Noriega
Estudiante de Ingeniería en Sistemas — Enfoque en Ciberseguridad e IA

🌐 Redes

GitHub: https://github.com/carlosrevillanoriega
Linkedin: https://www.linkedin.com/in/revilla-noriega-carlos


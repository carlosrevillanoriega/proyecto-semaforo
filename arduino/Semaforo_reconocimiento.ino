// Protector de Batería - VERSIÓN FINAL FUNCIONAL
const int PIN_ROJO = 11;
const int PIN_AMARILLO = 10;
const int PIN_VERDE = 9;

void setup() {
  Serial.begin(9600);
  pinMode(PIN_ROJO, OUTPUT);
  pinMode(PIN_AMARILLO, OUTPUT);
  pinMode(PIN_VERDE, OUTPUT);
  
  // Iniciar todos apagados
  digitalWrite(PIN_ROJO, LOW);
  digitalWrite(PIN_AMARILLO, LOW);
  digitalWrite(PIN_VERDE, LOW);
  
  Serial.println("Sistema iniciado. Listo para recibir datos 0-100");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    
    if (input.length() > 0) {
      int porcentaje = input.toInt();
      
      // Forzar límites
      if (porcentaje < 0) porcentaje = 0;
      if (porcentaje > 100) porcentaje = 100;
      
      Serial.print("Porcentaje recibido: ");
      Serial.println(porcentaje);
      
      // APAGAR TODOS los LEDs primero
      digitalWrite(PIN_ROJO, LOW);
      digitalWrite(PIN_AMARILLO, LOW);
      digitalWrite(PIN_VERDE, LOW);
      
      delay(10); // Pequeña pausa para asegurar que se apaguen
      
      // Encender SOLO UN LED según el porcentaje
      if (porcentaje <= 12) {
        digitalWrite(PIN_ROJO, HIGH);
        Serial.println("LED: ROJO (0-12%)");
      }
      else if (porcentaje <= 15) {
        digitalWrite(PIN_AMARILLO, HIGH);
        Serial.println("LED: AMARILLO (13-15%)");
      }
      else if (porcentaje >= 95) {
        digitalWrite(PIN_ROJO, HIGH);
        Serial.println("LED: ROJO (95-100%)");
      }
      else if (porcentaje >= 88) {
        digitalWrite(PIN_AMARILLO, HIGH);
        Serial.println("LED: AMARILLO (88-94%)");
      }
      else {
        digitalWrite(PIN_VERDE, HIGH);
        Serial.println("LED: VERDE (16-87%)");
      }
    }
  }
}
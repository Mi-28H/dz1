#include <Arduino.h>

// Конфигурация пинов
const int RED_PIN = 8;
const int YELLOW_PIN = 9;
const int GREEN_PIN = 10;

// Тайминги светофора (в миллисекундах)
const unsigned long RED_TIME = 5000;      // Красный - 5 секунд
const unsigned long YELLOW_TIME = 2000;   // Желтый - 2 секунды
const unsigned long GREEN_TIME = 5000;    // Зеленый - 5 секунд

// Состояния светофора
enum TrafficLightState {
  RED,
  RED_YELLOW,
  GREEN,
  YELLOW
};

TrafficLightState currentState = RED;
unsigned long stateStartTime = 0;

void setup() {
  // Настройка пинов как выходов
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  
  // Начальное состояние - все выключено
  digitalWrite(RED_PIN, LOW);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);
  
  // Инициализация последовательного порта для отладки
  Serial.begin(9600);
  Serial.println("Traffic Light System Started");
  
  stateStartTime = millis();
}

void setLights(bool red, bool yellow, bool green) {
  digitalWrite(RED_PIN, red ? HIGH : LOW);
  digitalWrite(YELLOW_PIN, yellow ? HIGH : LOW);
  digitalWrite(GREEN_PIN, green ? HIGH : LOW);
}

void loop() {
  unsigned long currentTime = millis();
  unsigned long elapsedTime = currentTime - stateStartTime;
  
  switch(currentState) {
    case RED:
      setLights(true, false, false);
      
      if (elapsedTime >= RED_TIME) {
        currentState = RED_YELLOW;
        stateStartTime = currentTime;
        Serial.println("Switching to RED+YELLOW");
      }
      break;
      
    case RED_YELLOW:
      setLights(true, true, false);
      
      if (elapsedTime >= YELLOW_TIME) {
        currentState = GREEN;
        stateStartTime = currentTime;
        Serial.println("Switching to GREEN");
      }
      break;
      
    case GREEN:
      setLights(false, false, true);
      
      if (elapsedTime >= GREEN_TIME) {
        currentState = YELLOW;
        stateStartTime = currentTime;
        Serial.println("Switching to YELLOW");
      }
      break;
      
    case YELLOW:
      setLights(false, true, false);
      
      if (elapsedTime >= YELLOW_TIME) {
        currentState = RED;
        stateStartTime = currentTime;
        Serial.println("Switching to RED");
      }
      break;
  }
  
  // Небольшая задержка для стабильности
  delay(50);
}

#include <ESP32Servo.h>
// Board: ESP32 Dev Module

const int IN3 = 12;
const int IN4 = 27;
const int SERVO_PIN = 13;
const int LED_PIN = 14;

Servo myServo;

void setup() {
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  
  myServo.attach(SERVO_PIN);
  myServo.write(0);

  digitalWrite(LED_PIN, HIGH);

  Serial.begin(115200);
}

void dispense(int card_num){
  for(int i = 0; i < card_num; i++){
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    delay(100);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    delay(200);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    delay(500);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    delay(200);
  }
}

void turn(int angle){
  myServo.write(angle * 0.74444);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    //Serial.println(command);

    if (command == 'd'){
      int cards = Serial.parseInt();
      if (cards != 0){
        dispense(cards);
        //Serial.print("Dispense ");
        //Serial.println(cards);
      }
    }

    else if(command == 't'){
      int degs = Serial.parseInt();
      turn(degs);
      //Serial.print("Turn ");
      //Serial.println(degs);
    }   
  }
}

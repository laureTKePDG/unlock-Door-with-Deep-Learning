#include <Servo.h>

Servo myservo;
char d;
int pos;
int ledPin = 8;
unsigned long previousMillis = 0;
const long interval = 5000; 
// interval to keep the LED on (in milliseconds)

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  myservo.attach(9);
  myservo.write(0);
}

void loop() {
  if (Serial.available()) {
    d = Serial.read();
  }

  if (d == 'a') {
    Serial.print(d);
    delay(300);

    unsigned long currentMillis = millis();

    if (pos < 90) {
      digitalWrite(ledPin, HIGH);
      previousMillis = currentMillis;
    }

    while (pos < 90) {
      pos += 5;
      myservo.write(pos);
      delay(20);

      

      
    }

    if (pos >= 90) {
      delay(5000);

      while (pos > 0) {
        pos -= 5;
        myservo.write(pos);
        digitalWrite(ledPin, LOW);
        delay(20);
      }
    }
  }

  d="";
}

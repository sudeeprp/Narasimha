#include <Servo.h>

Servo kickservo;
Servo fangservo;

const int hitpin = 2;
const int crackpin = 3;
const int placepin = 4;
const int kickpin = 10;
const int fangpin = 9;

void setup() {
  Serial.begin(9600);
  Serial.println("v1.2 hitint crack place fang un kick");

  pinMode(kickpin, OUTPUT);
  kickservo.attach(kickpin);
  kickservo.write(45);
  pinMode(fangpin, OUTPUT);
  fangservo.attach(fangpin);
  fangservo.write(50);

  pinMode(crackpin, OUTPUT);
  digitalWrite(crackpin, HIGH);
  pinMode(hitpin, INPUT_PULLUP);
  pinMode(placepin, INPUT);
  // interrupt source: https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/
  attachInterrupt(digitalPinToInterrupt(hitpin), pillarHit, FALLING);
  // only pins 2 & 3 are interruptible, so not interrupting on placement
}

void printJson(const char* key, const char* value) {
  Serial.print("\"");
  Serial.print(key);
  Serial.print("\":\"");
  Serial.print(value);
  Serial.print("\"");
}

char* digitalPinAsJson(int pin, const char* key) {
  int value = digitalRead(pin);
  if (value == HIGH) {
    printJson(key, "H");
  } else {
    printJson(key, "L");
  }
}

int pulse = 0;

void loop() {
  while (Serial.available() > 0) {
    int incoming = Serial.read();
    if (incoming == 'K') {
      Serial.println("Kickout");
      kickservo.write(0);
    } else if (incoming == 'F') {
      Serial.println("Fang");
      fangservo.write(0);
    } else if (incoming == 'U') {
      Serial.println("Unfang");
      fangservo.write(50);
    } else if (incoming == 'C') {
      Serial.println("Crack");
      digitalWrite(crackpin, LOW);
    } else if (incoming == 'R') {
      Serial.println("Relax");
      kickservo.write(45);
      fangservo.write(50);
      digitalWrite(crackpin, HIGH);
    }
  }
  if (pulse == 0) {
    Serial.print("{");
    digitalPinAsJson(hitpin, "hit");
    Serial.print(", ");
    digitalPinAsJson(placepin, "placed");
    Serial.println("}");
  }
  pulse = (pulse + 1) % 4;
  delay(250);
}

void pillarHit() {
  Serial.println("{\"event\": \"CRACK\"}");
}

void hiranyaPlaced() {
  Serial.println("{\"event\": \"HIRANYA\"}");
}

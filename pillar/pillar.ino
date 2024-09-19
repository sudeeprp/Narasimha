const int hitPin = 2;

void setup() {
  Serial.begin(9600);
  Serial.println("v0.1 2in");
  pinMode(hitPin, INPUT_PULLUP);
  // interrupt source: https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/
  attachInterrupt(digitalPinToInterrupt(hitPin), pillarHit, FALLING);
}

void loop() {
  int hitValue = digitalRead(hitPin);
  if (hitValue == HIGH) {
    Serial.println('H');
  } else {
    Serial.println('L');
  }
  delay(250);
}

void pillarHit() {
  Serial.println("CRACK");
}

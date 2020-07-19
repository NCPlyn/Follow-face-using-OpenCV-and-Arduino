#include <Stepper.h>
#include <Servo.h>
Stepper myStepper = Stepper(2038, 8, 10, 9, 11);
Servo myservo;
int pos = 45;
String str1;
String str2;
String incStr;

void setup() {
  myservo.attach(6);
  myservo.write(pos);
  myStepper.setSpeed(10);
  Serial.begin(2000000);
}

void loop() {

  while (Serial.available()) { 
    if (Serial.available() >0) {
      char c = Serial.read();
      incStr += c;
    }
  }

  if (incStr.length() >1) {
    Serial.println("1");
    incStr = String(incStr.toInt());

    str1 = incStr.substring(1, 2);
    str2 = incStr.substring(2, 3);

    if(str2 == "1") {
      if(pos < 92) {
        pos -= 1;
        myservo.write(pos);
      }
    } else if (str2 == "2") {
      if(pos < 90) {
        pos += 1;
        myservo.write(pos);
      }
    }

    if(str1 == "1") {
      myStepper.step(10);
      sleepStepper();
    } else if (str1 == "2") {
      myStepper.step(-10);
      sleepStepper();
    }

    incStr="";
  }
  
}

void sleepStepper() {
    digitalWrite(8, LOW);
    digitalWrite(9, LOW);
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);
}

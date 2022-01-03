#include <Servo.h>
#include <LiquidCrystal.h>

int SERVO = 9;
String str;

Servo servo_9;

signed short minutes=5, seconds=0;
char timeline;

void setup()
{
  Serial.begin(9600);
  servo_9.attach(SERVO, 500, 2500);
}

void loop()
{
  if (Serial.available() > 0)
  {
    str = Serial.readStringUntil('\n');
    if(str == "blind"){
      sayMode();
      Serial.write("ok");
    }
    else if(str =="looking"){
      catchMode();
      Serial.write("ok");
    }
  }
}


void sayMode() { // 무궁화 꽃이 피었습니다 말하는 상태
  servo_9.write(0);
}

void catchMode() { // 고개 돌려서 움직이는 사람 잡는 상태
  servo_9.write(180);
}

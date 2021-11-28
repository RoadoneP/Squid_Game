const int RLED = 13;
const int GLED = 12;
const int BLED = 11;
String str;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(RLED, OUTPUT);
  pinMode(GLED, OUTPUT);
  pinMode(BLED, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if(Serial.available() > 0){
    str = Serial.readStringUntil('\n');
    if(str == "blind"){
      analogWrite(GLED, 0);
      analogWrite(RLED, 255);
      analogWrite(BLED, 255);
      Serial.write("ok");
    }
    else if(str == "speaking"){
      analogWrite(GLED, 255);
      analogWrite(RLED, 255);
      analogWrite(BLED, 0);
      Serial.write("ok");
    }
    else if(str =="looking"){
      analogWrite(GLED, 255);
      analogWrite(RLED, 0);
      analogWrite(BLED, 255);
      delay(1000);
      Serial.write("ok");
    }
    else{
      analogWrite(GLED, 255);
      analogWrite(RLED, 255);
      analogWrite(BLED, 255);
      Serial.write("wait");
    }
  }
}

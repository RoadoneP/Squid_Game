int Distance = 0; // 회전 스텝 수
int delaySpeed = 5000; // 회전 지연 (Microseconds)

const int laserPin = 5;
const int xPulse = 2; // CLK (회전 펄스)
const int xDirection = 3; // CW (회전 방향)
const int yPulse = 8; // CLK
const int yDirection = 9; // CW

void setup(){
  Serial.begin(9600);

  pinMode(laserPin, OUTPUT);
  pinMode(xPulse, OUTPUT);
  pinMode(yPulse, OUTPUT);
  pinMode(xDirection, OUTPUT);
  pinMode(yDirection, OUTPUT);
  
  digitalWrite(xPulse, LOW); // x축 회전 펅스
  digitalWrite(yPulse, LOW); // y축 회전 펄스 

  digitalWrite(laserPin, HIGH);
}

void loop() {
  // 시리얼 입력
  if (Serial.available() > 0) {
    float x_rotate = Serial.parseInt();
    float y_rotate = Serial.parseInt();
    
    // x축 방향 선택
    if (x_rotate >= 90)
      digitalWrite(xDirection, LOW); // 시계 방향
    else
      digitalWrite(xDirection, HIGH); // 반시계 방향

    // y축 방향 선택
    if (y_rotate >= 90)
      digitalWrite(yDirection, LOW); // 시계 방향
    else
      digitalWrite(yDirection, HIGH); // 반시계 방향

    // x축 회전 각도 계산
    float x_rotate_steps = abs(90.0 - x_rotate); // 90도 기준으로 계산
    x_rotate_steps = x_rotate_steps * 1600 / 360; // 기준 distance 값 계산
  

    // y축 회전 각도 계산
    float y_rotate_steps = abs(90.0 - y_rotate); // 90도 기준으로 계산
    y_rotate_steps = y_rotate_steps * 1600 / 360; // 기준 distance 값 계산

    // y축 회전 시작
    while(true) {
      digitalWrite(yPulse, HIGH);
      delayMicroseconds(delaySpeed);
      digitalWrite(yPulse, LOW);
      delayMicroseconds(delaySpeed);
  
      Distance = Distance + 1;

      // 회전 종료
      if (Distance >= y_rotate_steps) {
        Distance = 0;
        break;
      }
    }
    
    // x축 회전 시작
    while(true) {
      digitalWrite(xPulse, HIGH);
      delayMicroseconds(delaySpeed);
      digitalWrite(xPulse, LOW);
      delayMicroseconds(delaySpeed);
  
      Distance = Distance + 1;

      // 회전 종료
      if (Distance >= x_rotate_steps) {
        Distance = 0;
        break;
      }
    }
  }
}

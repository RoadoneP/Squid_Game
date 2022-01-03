import serial
import time


robot_status = 'blind'

def send_Younghee():
    younghee.write(robot_status.encode())
    time.sleep(0.5)
    msg = younghee.readline().decode('ascii')
    return msg

def start_blind():
    global robot_status
    robot_status = 'blind'
    msg = send_Younghee()
    # 영희 모터 회전 명령 led 녹색
    if msg == 'ok':
        print("blind end")
        start_speaking()

def start_speaking():
    global robot_status
    robot_status = 'speaking'
    msg = send_Younghee()
    if msg == 'ok':
        print("speaking end")
        start_looking()
    # 아두이노에 스피커 명령
    # 및 시간 돌리기

def start_looking():
    # 모터 회전
    global robot_status
    robot_status = 'looking'
    msg = send_Younghee()
    if msg == 'ok':
        print("looking end")
        start_blind()
    # 감지 시작

if __name__ == "__main__":
    younghee = serial.Serial('COM6', 9600)
    younghee.timeout = 10
    time.sleep(5) # 연결 시간을 기다려줘야 함
    start_blind() 

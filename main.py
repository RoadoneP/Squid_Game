import cv2
import numpy as np
import serial
import time
import threading
import random
from playsound import playsound

# 영희의 상태
robot_status = 'blind' # (blind, speaking, looking)
# 플레이어의 상태
player_status ='alive' # (alive, dead)
MOVE_THRESHOLD = 2000

# 아두이노(영희) 메시지
def send_Younghee():
    younghee.write(robot_status.encode())
    time.sleep(0.2)
    msg = younghee.readline().decode('ascii')
    return msg

# 아두이노(레이저) 메시지 좌표값 전달
def send_laser():
    pass

# 영희 모터 회전 명령 led 녹색
def start_blind():
    global robot_status
    robot_status = 'blind'
    msg = send_Younghee()
    if msg == 'ok':
        print("blind end")
        start_speaking()

# 스피커 작동 명령
def start_speaking():
    global robot_status
    robot_status = 'speaking'
    rand_sound = random.randint(1, 6)
    sound_path = "./sound/squid_game_" + str(rand_sound) + ".mp3" 
    playsound(sound_path)
    print("speaking end")
    start_looking()


# 영희 모터 회전 및 감지시작
def start_looking():
    global robot_status
    robot_status = 'looking'
    msg = send_Younghee()
    # 아두이노의 응답 & player가 살아있는 경우
    if msg == 'ok' and player_status == 'alive':
        print("looking end")
        start_blind()
    # 아두이노의 응답 & player가 죽은 경우    
    elif msg =='ok' and player_status == 'dead':
        robot_status = 'game over'
        return

# 웹캠 및 움직임 감지
def Webcam():
    global player_status

    cap = cv2.VideoCapture(0)
    sub = cv2.createBackgroundSubtractorKNN(history=1, dist2Threshold=5000, detectShadows=False)
    
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        mask = sub.apply(img)
        # print(f"mask_max1: {np.unique(mask)}")
        # mask = np.expand_dims(mask, axis=2).repeat(3, axis=2)
        # mask = img * mask
        # print(f"mask_max2: {np.unique(mask)}")
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # mask = cv2.dilate(mask, kernel, iterations=2)
        # mask의 값 0 or 255의 값을  0 or 1로 바꾸고 합치기
        diff = (mask.astype('float') / 255.).sum()
        if robot_status == 'looking' and diff > MOVE_THRESHOLD:
            player_status = 'dead'

        cv2.putText(mask, text=robot_status, org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,255,255), thickness=2)
        cv2.putText(mask, text=player_status, org=(560, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,255,255), thickness=2)

        cv2.imshow('mask', mask)
        cv2.imshow('image', img)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == "__main__":
    younghee = serial.Serial('COM6', 9600)
    younghee.timeout = 1
    time.sleep(5) # 연결 시간을 기다려줘야 함

    t = threading.Thread(target=Webcam)
    t.start()
    start_blind()

    
    


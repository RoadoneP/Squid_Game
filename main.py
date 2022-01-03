#-*-coding:utf-8-*-
import cv2
import numpy as np
import jetson.inference
import jetson.utils
import serial
import time
import threading
import random
from playsound import playsound
import keyboard
import math

# 영희의 상태
robot_status = 'blind' # (blind, speaking, looking)
# 플레이어의 상태
player_status ='alive' # (alive, dead)
MOVE_THRESHOLD = 500
cx = 0
cy = 0
flag = True
P1 = 320
P2 = 240
ALPHA = 20
BETA = 15

# 아두이노(영희) 메시지
def send_Younghee():
    pass
    # younghee.write(robot_status.encode())
    # time.sleep(0.2)
    # msg = younghee.readline().decode('ascii')
    # return msg

def y_degree(cy_fix):
    accel = abs(cy_fix-P2)//15
    if cy_fix < P2 - BETA:
        return 91 + accel
    elif cy_fix > P2 + BETA:
        return 89 - accel
    else:
        return 90
        
# 아두이노(레이저) 메시지 좌표값 전달
def send_laser():
    while True:
        cx_fix, cy_fix = int(cx), int(cy)
        # x좌표
        if cx_fix != 0 and cy_fix !=0:
            accel = abs(cx_fix - P1)//20
            if P1 - ALPHA > cx_fix:
                angle = str(88-accel) + ' ' + str(y_degree(cy_fix))
                motor.write(angle.encode())
                print(angle)
                time.sleep(3)
                # msg = motor.readline().decode('ascii')
                
            elif P1 + ALPHA < cx_fix: 
                angle = str(92+accel) + ' ' + str(y_degree(cy_fix))
                motor.write(angle.encode())
                print(angle)
                time.sleep(3)
                # msg = motor.readline().decode('ascii')
                
            else:
                if y_degree(cy_fix) == 90:
                    time.sleep(3)
                else:
                    angle = str(90) + ' ' + str(y_degree(cy_fix))
                    motor.write(angle.encode())
                    print(angle)
                    time.sleep(3)
                    # msg = motor.readline().decode('ascii')
                    

    # msg_gun = motor.readline().decode('ascii')
    # if msg_gun == 'ok':
    #     playsound('./sound/gun_sound.mp3')
    #     return
    

# 영희 모터 회전 명령 led 녹색
def start_blind():
    global robot_status
    robot_status = 'blind'
    time.sleep(2)
    # msg = send_Younghee()
    # if msg == 'ok':
    #     # print("blind end")
    start_speaking()

# 스피커 작동 명령
def start_speaking():
    global robot_status
    robot_status = 'speaking'
    time.sleep(3)
    # rand_sound = random.randint(1, 6)
    # sound_path = "./sound/squid_game_" + str(rand_sound) + ".mp3" 
    # playsound(sound_path)
    # # print("speaking end")
    start_looking()


# 영희 모터 회전 및 감지시작
def start_looking():
    global robot_status
    robot_status = 'looking'
    send_laser()
    # msg = send_Younghee()
    # # 아두이노의 응답 & player가 살아있는 경우
    # time.sleep(3)
    # if msg == 'ok' and player_status == 'alive':
    #     # print("looking end")
    #     start_blind()
    # # 아두이노의 응답 & player가 죽은 경우    
    # elif msg =='ok' and player_status == 'dead':
    #     robot_status = 'game over'
    #     send_laser()
        

# 웹캠 및 움직임 감지
def Webcam():
    global cx, cy
    global player_status
    net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
    # camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
    camera = jetson.utils.videoSource("/dev/video0", ["--input-width=640","--input-height=320"])
    display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
    sub = cv2.createBackgroundSubtractorKNN(history=1, dist2Threshold=500, detectShadows=False)

    while display.IsStreaming():
        img = camera.Capture()
        frame = camera.Capture()
        detections = net.Detect(img)
        img = jetson.utils.cudaToNumpy(img, 640, 320, 4)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        frame = jetson.utils.cudaToNumpy(frame, 640, 320, 4)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB).astype(np.uint8)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # bounding box complete
        mask = sub.apply(frame)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        xpoint = int(frame.shape[1] / 2)
        ypoint = int(frame.shape[0] / 2)
        img = cv2.line(img, (xpoint, ypoint - 20), (xpoint, ypoint + 20), (0, 0, 255), 2)
        img = cv2.line(img, (xpoint - 20, ypoint), (xpoint + 20, ypoint), (0, 0, 255), 2)
        img = cv2.line(img, (xpoint, ypoint), (xpoint, ypoint), (0, 255, 0), 10)
        img = cv2.circle(img, (xpoint, ypoint), 30, (0, 255, 0), 2)

        bbox = np.zeros_like(img)
        if len(detections) > 0:
            xidx = [int(detections[0].Left),int(detections[0].Right)]
            yidx = [int(detections[0].Top),int(detections[0].Bottom)]
            f_cx, f_cy = detections[0].Center
            cx, cy = int(f_cx), int(f_cy)
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            bbox[yidx[0]+1:yidx[1]-1,xidx[0]+1:xidx[1]-1] = mask[yidx[0]+1:yidx[1]-1,xidx[0]+1:xidx[1]-1]		
            img = cv2.circle(img,(cx, cy), 10, (0, 255, 0), -1, cv2.LINE_AA)
            diff = (bbox.astype('float') / 255.).sum()
            if robot_status == 'looking' and diff > MOVE_THRESHOLD:
                player_status = 'dead'
            
        else:
            cx = 0
            cy = 0

        cv2.putText(bbox, text=robot_status, org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,255,255), thickness=2)
        cv2.putText(bbox, text=player_status, org=(560, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,255,255), thickness=2)
        cv2.imshow("Detection",img)
        cv2.imshow("mask", bbox)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

if __name__ == "__main__":
    t = threading.Thread(target=Webcam)
    t.start()

    # younghee = serial.Serial('/dev/ttyACM1', 9600)
    # younghee.timeout = 1
    motor = serial.Serial('/dev/ttyACM0', 9600)
    motor.timeout = 5
    time.sleep(5) # 연결 시간을 기다려줘야 함

    start_blind()
